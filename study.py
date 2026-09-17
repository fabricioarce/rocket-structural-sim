"""Evaluación paramétrica y selección discreta del estudio de flutter."""

from dataclasses import asdict, dataclass
from itertools import product

import numpy as np

from flutter import Fin, flutter_history, required_thickness
from materials import get_material
from simulation import Design, build_flight


@dataclass(frozen=True)
class Limits:
    flutter_ratio: float = 1.25
    stability_cal: float = 1.0
    rail_speed_m_s: float = 20.0
    loaded_aoa_deg: float = 10.0
    mach: float = 1.5

    def __post_init__(self):
        if not all(np.isfinite(v) and v > 0 for v in asdict(self).values()):
            raise ValueError("Los límites deben ser positivos y finitos")


def _fin(design):
    g = design.fin_geometry
    return Fin(g["root"], g["tip"], g["span"], g["sweep"], design.fin_thickness_m, design.fin_shear_pa)


def _time_grid(flight, samples):
    if type(samples) is not int or samples < 2:
        raise ValueError("samples debe ser un entero mayor o igual que 2")
    start, stop = flight.out_of_rail_time + 1e-5, flight.apogee_time
    events = [flight.max_dynamic_pressure_time, flight.max_speed_time]
    burnout = flight.rocket.motor.burn_out_time
    events.extend((burnout - 1e-5, burnout + 1e-5))
    points = np.linspace(start, stop, samples)
    events = np.clip(np.asarray(events, float), start, stop)
    return np.unique(np.sort(np.r_[points, events]))


def evaluate_case(design, samples=180, max_time_step=0.12, target_ratio=1.25):
    flight = build_flight(design, max_time_step=max_time_step)
    time = _time_grid(flight, samples)
    z = np.asarray([flight.z(t) for t in time], float)
    air = np.asarray([flight.free_stream_speed(t) for t in time], float)
    speed = np.asarray([flight.speed(t) for t in time], float)
    q = np.asarray([flight.dynamic_pressure(t) for t in time], float)
    alpha = np.asarray([flight.angle_of_attack(t) for t in time], float)
    mach = np.asarray([flight.mach_number(t) for t in time], float)
    stability = np.asarray([flight.stability_margin(t) for t in time], float)
    density = np.asarray([flight.env.density(h) for h in z], float)
    pressure = np.asarray([flight.env.pressure(h) for h in z], float)
    sound = np.asarray([flight.env.speed_of_sound(h) for h in z], float)
    history = flutter_history(_fin(design), pressure, sound, air)
    vf, ratios = history["flutter_speed"], history["ratio"]
    required = required_thickness(_fin(design), pressure, sound, target_ratio * np.maximum(air, 1e-9))
    arrays = (time, z, air, speed, q, alpha, mach, stability, density, pressure, sound, vf, ratios, required)
    if not all(np.all(np.isfinite(value)) for value in arrays):
        raise ValueError("La simulación produjo datos no finitos")
    flutter_index = history["critical_index"]
    loaded = q >= 500
    summary = {
        **asdict(design),
        "apogee_agl_m": float(flight.apogee - flight.env.elevation),
        "apogee_asl_m": float(flight.apogee),
        "apogee_time_s": float(flight.apogee_time),
        "max_speed_m_s": float(flight.max_speed),
        "max_speed_time_s": float(flight.max_speed_time),
        "max_airspeed_m_s": float(air.max()),
        "max_q_pa": float(flight.max_dynamic_pressure),
        "max_q_time_s": float(flight.max_dynamic_pressure_time),
        "rail_exit_s": float(flight.out_of_rail_time),
        "rail_speed_m_s": float(flight.out_of_rail_velocity),
        "min_flutter_ratio": float(ratios.min()),
        "flutter_time_s": float(time[flutter_index]),
        "flutter_altitude_asl_m": float(z[flutter_index]),
        "flutter_speed_at_min_m_s": float(vf[flutter_index]),
        "airspeed_at_min_m_s": float(air[flutter_index]),
        "ratio_at_max_q": float(np.interp(flight.max_dynamic_pressure_time, time, ratios)),
        "ratio_at_max_speed": float(np.interp(flight.max_speed_time, time, ratios)),
        "required_thickness_mm": float(required.max() * 1000),
        "min_stability_cal": float(stability.min()),
        "max_mach": float(mach.max()),
        "loaded_aoa_deg": float(alpha[loaded].max()) if np.any(loaded) else 0.0,
        "samples": len(time),
    }
    trace = {
        "time_s": time,
        "altitude_agl_m": z - flight.env.elevation,
        "altitude_asl_m": z,
        "airspeed_m_s": air,
        "speed_m_s": speed,
        "q_pa": q,
        "aoa_deg": alpha,
        "mach": mach,
        "stability_cal": stability,
        "density_kg_m3": density,
        "pressure_pa": pressure,
        "sound_speed_m_s": sound,
        "flutter_speed_m_s": vf,
        "flutter_ratio": ratios,
    }
    return {"summary": summary, "trace": trace}


def _postprocess(result, fin):
    trace = result["trace"]
    history = flutter_history(fin, trace["pressure_pa"], trace["sound_speed_m_s"], trace["airspeed_m_s"])
    return {
        "min_ratio": float(np.min(history["ratio"])),
        "flutter_speed_m_s": history["flutter_speed"],
        "ratio": history["ratio"],
    }


def thickness_sweep(result, thicknesses_m, shear_pa=None):
    """Recalcula flutter algebraicamente; ignora el cambio de masa de la aleta."""
    if not thicknesses_m:
        raise ValueError("Se necesita al menos un espesor")
    design = Design(**{key: result["summary"][key] for key in asdict(Design())})
    values = []
    for thickness in thicknesses_m:
        if not np.isfinite(thickness) or thickness <= 0:
            raise ValueError("Los espesores deben ser positivos y finitos")
        candidate = _fin(Design(**{**asdict(design), "fin_thickness_m": thickness,
                                   **({"fin_shear_pa": shear_pa} if shear_pa is not None else {})}))
        values.append({"thickness_m": float(thickness), "min_ratio": _postprocess(result, candidate)["min_ratio"]})
    return values


def material_sweep(result, slugs, target_ratio=1.25):
    """Recalcula flutter algebraicamente; ignora el cambio de masa de la aleta."""
    if not slugs:
        raise ValueError("Se necesita al menos un material")
    design = Design(**{key: result["summary"][key] for key in asdict(Design())})
    values = []
    for slug in slugs:
        material = get_material(slug)
        candidate = _fin(Design(**{**asdict(design), "fin_shear_pa": material["shear_pa"],
                                     "fin_density_kg_m3": material["density_kg_m3"]}))
        required = required_thickness(
            candidate, result["trace"]["pressure_pa"], result["trace"]["sound_speed_m_s"],
            target_ratio * np.maximum(result["trace"]["airspeed_m_s"], 1e-9),
        )
        values.append({"slug": slug, "nombre": material["nombre"],
                       "min_ratio": _postprocess(result, candidate)["min_ratio"],
                       "required_thickness_mm": float(required.max() * 1000),
                       "shear_pa": material["shear_pa"], "density_kg_m3": material["density_kg_m3"]})
    return values


def rejection_reasons(summary, limits):
    metrics = ("min_flutter_ratio", "min_stability_cal", "rail_speed_m_s", "loaded_aoa_deg",
               "max_mach", "apogee_agl_m")
    if not all(np.isfinite(summary[k]) for k in metrics):
        return ["resultado no finito"]
    checks = (
        (summary["min_flutter_ratio"] < limits.flutter_ratio, "flutter"),
        (summary["min_stability_cal"] < limits.stability_cal, "estabilidad estática"),
        (summary["rail_speed_m_s"] < limits.rail_speed_m_s, "salida del riel"),
        (summary["loaded_aoa_deg"] > limits.loaded_aoa_deg, "ángulo de ataque fuera del alcance"),
        (summary["max_mach"] > limits.mach, "Mach fuera del alcance"),
    )
    return [reason for rejected, reason in checks if rejected]


def select_best(cases, limits, scenario_count):
    """Máximo del apogeo mínimo en todos los escenarios de viento previstos."""
    if scenario_count < 1:
        raise ValueError("Se necesita al menos un escenario")
    groups = {}
    for case in cases:
        key = (case["payload_kg"], case["fin_scale"])
        groups.setdefault(key, []).append(case)
    ranked = []
    for (payload, scale), group in groups.items():
        winds = {case["wind_m_s"] for case in group}
        reasons = sorted({reason for case in group for reason in rejection_reasons(case, limits)})
        if len(group) != scenario_count or len(winds) != scenario_count:
            reasons.append("faltan escenarios o hay duplicados")
        ranked.append({
            "payload_kg": payload, "fin_scale": scale,
            "worst_apogee_agl_m": min(case["apogee_agl_m"] for case in group),
            "min_flutter_ratio": min(case["min_flutter_ratio"] for case in group),
            "reasons": reasons, "admissible": not reasons,
        })
    ranked.sort(key=lambda r: (-r["worst_apogee_agl_m"], r["payload_kg"], r["fin_scale"]))
    best = next((r for r in ranked if r["admissible"]), None)
    return best, ranked


def grid_designs(base, payloads, scales, winds):
    if not all(len(v) > 0 and len(v) == len(set(v)) for v in (payloads, scales, winds)):
        raise ValueError("Las listas del barrido deben ser no vacías y sin duplicados")
    if len(payloads) * len(scales) * len(winds) > 100:
        raise ValueError("La demo admite hasta 100 casos por ejecución")
    return [Design(**{**asdict(base), "payload_kg": p, "fin_scale": s, "wind_m_s": w})
            for p, s, w in product(payloads, scales, winds)]
