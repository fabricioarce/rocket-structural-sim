"""Evaluación paramétrica y selección discreta; no optimización global."""

from dataclasses import asdict, dataclass
from itertools import product

import numpy as np

from flutter import Fin, flutter_speed
from simulation import Design, NOSE, TAIL, build_flight
from structural_loads import TubeSection, find_critical_time, get_surface_stations


@dataclass(frozen=True)
class Limits:
    stress_mpa: float = 4.0
    flutter_ratio: float = 1.25
    stability_cal: float = 1.0
    rail_speed_m_s: float = 20.0
    loaded_aoa_deg: float = 10.0
    mach: float = 1.5

    def __post_init__(self):
        if not all(np.isfinite(v) and v > 0 for v in asdict(self).values()):
            raise ValueError("Los límites deben ser positivos y finitos")


def evaluate_case(design, section, samples=180, mass_nodes=32, max_time_step=0.12):
    flight = build_flight(design, mass_nodes=mass_nodes, max_time_step=max_time_step)
    critical, results = find_critical_time(flight, get_surface_stations(flight.rocket),
                                          NOSE-TAIL, section, n_samples=samples)
    time = np.array([r["t"] for r in results])
    z = np.array([flight.z(t) for t in time])
    air = np.array([flight.free_stream_speed(t) for t in time])
    q = np.array([flight.dynamic_pressure(t) for t in time])
    alpha = np.array([flight.angle_of_attack(t) for t in time])
    mach = np.array([flight.mach_number(t) for t in time])
    stability = np.array([flight.stability_margin(t) for t in time])
    p = np.array([flight.env.pressure(h) for h in z])
    sound = np.array([flight.env.speed_of_sound(h) for h in z])
    g = design.fin_geometry
    fin = Fin(g["root"], g["tip"], g["span"], g["sweep"], design.fin_thickness_m, design.fin_shear_pa)
    vf = flutter_speed(fin, p, sound)
    ratios = vf / np.maximum(air, 1e-9)
    stress = np.array([r["combined_stress"]/1e6 for r in results])
    force_residual = max(np.linalg.norm(r["diagram"]["residual_force"]) for r in results)
    moment_residual = max(np.linalg.norm(r["diagram"]["residual_moment"]) for r in results)
    if not all(np.all(np.isfinite(a)) for a in (time, z, air, q, alpha, mach, stability, vf, stress)):
        raise ValueError("La simulación produjo datos no finitos")
    if force_residual > 1e-7 or moment_residual > 1e-7:
        raise ValueError("Falló el cierre de equilibrio del modelo de viga")
    flutter_index = int(np.argmin(ratios))
    loaded = q >= 500
    summary = {
        **asdict(design), "apogee_agl_m": float(flight.apogee-flight.env.elevation),
        "apogee_asl_m": float(flight.apogee), "apogee_time_s": float(flight.apogee_time),
        "max_speed_m_s": float(flight.max_speed), "max_airspeed_m_s": float(air.max()),
        "max_q_pa": float(flight.max_dynamic_pressure), "max_q_time_s": float(flight.max_dynamic_pressure_time),
        "rail_exit_s": float(flight.out_of_rail_time), "rail_speed_m_s": float(flight.out_of_rail_velocity),
        "stress_mpa": float(stress.max()), "critical_time_s": critical["t"],
        "critical_station_m": critical["critical_station"],
        "max_moment_nm": max(r["max_moment"] for r in results),
        "min_flutter_ratio": float(ratios.min()), "flutter_time_s": float(time[flutter_index]),
        "flutter_altitude_asl_m": float(z[flutter_index]),
        "min_stability_cal": float(stability.min()), "max_mach": float(mach.max()),
        "loaded_aoa_deg": float(alpha[loaded].max()) if np.any(loaded) else 0.0,
        "force_residual_n": float(force_residual), "moment_residual_nm": float(moment_residual),
        "samples": len(time), "mass_nodes_per_group": mass_nodes,
    }
    trace = {
        "time_s": time, "altitude_agl_m": z-flight.env.elevation, "altitude_asl_m": z,
        "airspeed_m_s": air, "speed_m_s": np.array([flight.speed(t) for t in time]),
        "q_pa": q, "aoa_deg": alpha, "mach": mach, "stability_cal": stability,
        "density_kg_m3": np.array([flight.env.density(h) for h in z]), "pressure_pa": p,
        "stress_mpa": stress, "max_moment_nm": np.array([r["max_moment"] for r in results]),
        "max_axial_n": np.array([np.max(r["diagram"]["axial"]) for r in results]),
        "flutter_speed_m_s": vf, "flutter_ratio": ratios,
    }
    heat_stations = np.linspace(TAIL, NOSE, 101)
    heatmap = np.array([np.interp(heat_stations, r["diagram"]["stations"], r["stress"])/1e6 for r in results])
    diagram = {"station_m": critical["diagram"]["stations"],
               "axial_n": critical["diagram"]["axial"],
               "shear_n": critical["diagram"]["shear"],
               "moment_nm": critical["diagram"]["moment"], "stress_mpa": critical["stress"]/1e6}
    return {"summary": summary, "trace": trace, "critical_diagram": diagram,
            "heat_stations": heat_stations, "heatmap": heatmap}


def rejection_reasons(summary, limits):
    metrics = ("stress_mpa", "min_flutter_ratio", "min_stability_cal", "rail_speed_m_s",
               "loaded_aoa_deg", "max_mach", "apogee_agl_m")
    if not all(np.isfinite(summary[k]) for k in metrics):
        return ["resultado no finito"]
    checks = (
        (summary["stress_mpa"] > limits.stress_mpa, "esfuerzo"),
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
        ranked.append({"payload_kg": payload, "fin_scale": scale,
                       "worst_apogee_agl_m": min(case["apogee_agl_m"] for case in group),
                       "worst_stress_mpa": max(case["stress_mpa"] for case in group),
                       "min_flutter_ratio": min(case["min_flutter_ratio"] for case in group),
                       "reasons": reasons, "admissible": not reasons})
    ranked.sort(key=lambda r: (-r["worst_apogee_agl_m"], r["payload_kg"], r["fin_scale"]))
    best = next((r for r in ranked if r["admissible"]), None)
    return best, ranked


def grid_designs(base, payloads, scales, winds):
    if not all(len(v) > 0 and len(v) == len(set(v)) for v in (payloads, scales, winds)):
        raise ValueError("Las listas del barrido deben ser no vacías y sin duplicados")
    if len(payloads)*len(scales)*len(winds) > 100:
        raise ValueError("La demo admite hasta 100 casos por ejecución")
    return [Design(**{**asdict(base), "payload_kg": p, "fin_scale": s, "wind_m_s": w})
            for p, s, w in product(payloads, scales, winds)]
