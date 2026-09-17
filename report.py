"""Informe HTML sin servicios externos y figuras PNG reproducibles."""

import csv
import html
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from flutter import Fin, flutter_speed
from materials import MATERIALS
from simulation import Design

ROOT = Path(__file__).resolve().parent
COLORS = ("#007f86", "#e4763a", "#5266a6", "#bb425a", "#7a5c9e")


def save(fig, output, filename):
    fig.tight_layout(pad=1.8)
    fig.savefig(output / filename, dpi=155, facecolor="white")
    plt.close(fig)


def _fin(design, thickness=None, shear=None, scale=None):
    g = design.fin_geometry if scale is None else Design(**{**design.__dict__, "fin_scale": scale}).fin_geometry
    return Fin(g["root"], g["tip"], g["span"], g["sweep"],
               design.fin_thickness_m if thickness is None else thickness,
               design.fin_shear_pa if shear is None else shear)


def _markers(axis, summary):
    for key, label, color in (("max_q_time_s", "Max-Q", COLORS[1]),
                              ("max_speed_time_s", "Máx. velocidad", COLORS[2])):
        if key in summary:
            axis.axvline(summary[key], color=color, linestyle=":", label=label)
    axis.axvline(3.9, color=COLORS[3], linestyle="--", label="Burnout")


def _trace_csv(output, case_id):
    with (output / f"{case_id}.csv").open(encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    return {key: np.asarray([float(row[key]) for row in rows]) for key in rows[0]}


def plot_reports(output, data, base, thin, drag_cases, sweeps):
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.grid": True, "grid.alpha": 0.16, "axes.titleweight": "bold"})
    s, trace = base["summary"], base["trace"]
    t = trace["time_s"]
    limits = data["config"]["limits"]
    fig, ax = plt.subplots(2, 2, figsize=(12, 7))
    ax[0, 0].plot(t, trace["altitude_agl_m"], color=COLORS[0])
    ax[0, 0].set(title="Altura sobre el lanzamiento (AGL)", ylabel="Altura [m]")
    ax[0, 1].plot(t, trace["airspeed_m_s"], color=COLORS[0], label="Respecto al aire")
    ax[0, 1].plot(t, trace["speed_m_s"], color=COLORS[1], linestyle="--", label="Respecto al suelo")
    ax[0, 1].set(title="Velocidades de vuelo", ylabel="Velocidad [m/s]")
    ax[0, 1].legend()
    ax[1, 0].plot(t, trace["q_pa"] / 1000, color=COLORS[0])
    ax[1, 0].axvline(s["max_q_time_s"], color=COLORS[1], linestyle="--", label="Max-Q")
    ax[1, 0].set(title="Presión dinámica", ylabel="q [kPa]")
    ax[1, 0].legend()
    ax[1, 1].plot(t, trace["stability_cal"], color=COLORS[0])
    ax[1, 1].axhline(limits["stability_cal"], color=COLORS[1], linestyle="--", label="Límite")
    ax[1, 1].set(title="Margen estático", ylabel="Calibres")
    ax[1, 1].legend()
    for axis in ax.flat:
        axis.set_xlabel("Tiempo desde ignición [s]")
    fig.suptitle("Caso base · vuelo RocketPy después de abandonar el riel", fontsize=14)
    save(fig, output, "01-flight.png")

    fig, ax = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    ax[0].plot(t, trace["flutter_speed_m_s"], color=COLORS[2], label="Vf")
    ax[0].plot(t, trace["airspeed_m_s"], color=COLORS[0], label="V relativa")
    _markers(ax[0], s)
    ax[0].set_ylabel("Velocidad [m/s]")
    ax[0].set_title("Frontera de flutter frente a velocidad relativa")
    ax[0].legend(loc="center right", ncol=2, fontsize=8)
    ax[1].plot(t, trace["flutter_ratio"], color=COLORS[0])
    ax[1].axhline(limits["flutter_ratio"], color=COLORS[1], linestyle="--", label="Límite")
    index = int(np.argmin(trace["flutter_ratio"]))
    ax[1].plot(t[index], trace["flutter_ratio"][index], "o", color=COLORS[3], label="Mínimo")
    ax[1].set_ylabel("Vf / V")
    ax[1].legend()
    pressure_axis = ax[2]
    sound_axis = pressure_axis.twinx()
    pressure_axis.plot(t, trace["pressure_pa"] / 1000, color=COLORS[0], label="p")
    sound_axis.plot(t, trace["sound_speed_m_s"], color=COLORS[2], label="a")
    pressure_axis.set_ylabel("Presión [kPa]")
    sound_axis.set_ylabel("Sonido [m/s]")
    pressure_axis.set_xlabel("Tiempo desde ignición [s]")
    pressure_axis.set_title("La presión baja y Vf aumenta con la altitud")
    _markers(pressure_axis, s)
    save(fig, output, "02-flutter-history.png")

    atmosphere = base["atmosphere"]
    altitude, p, a, rho = (atmosphere[k] for k in ("altitude_asl_m", "pressure_pa", "sound_speed_m_s", "density_kg_m3"))
    base_alt_vf = flutter_speed(_fin(Design(**{k: s[k] for k in Design.__dataclass_fields__})), p, a)
    thin_summary = thin["summary"]
    thin_design = Design(**{**{k: thin_summary[k] for k in Design.__dataclass_fields__}})
    thin_alt_vf = flutter_speed(_fin(thin_design), p, a)
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].plot(base_alt_vf, altitude / 1000, label="Aleta base", color=COLORS[0])
    ax[0].plot(thin_alt_vf, altitude / 1000, label="Aleta delgada", color=COLORS[3])
    flown = (atmosphere["launch_asl_m"] / 1000, s["apogee_asl_m"] / 1000)
    for axis in ax:
        axis.axhspan(*flown, color=COLORS[1], alpha=0.12, label="Tramo volado (base)")
    ax[0].set(xlabel="Vf [m/s]", ylabel="Altitud ASL [km]", title="Vf frente a altitud (atmósfera del modelo)")
    ax[0].legend()
    norm = lambda values: values / values[0]
    ax[1].plot(norm(p), altitude / 1000, label="p/p₀", color=COLORS[0])
    ax[1].plot(norm(rho), altitude / 1000, label="ρ/ρ₀", color=COLORS[1])
    ax[1].plot(norm(a), altitude / 1000, label="a/a₀", color=COLORS[2])
    ax[1].set(xlabel="Normalizado al nivel del mar (0 m ASL)", ylabel="Altitud ASL [km]", title="Atmósfera del modelo")
    ax[1].legend()
    save(fig, output, "03-altitude.png")

    thickness = np.asarray([row["thickness_m"] for row in sweeps["thickness"]])
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for index, slug in enumerate(data["config"]["materials"]):
        material = MATERIALS[slug]
        ratios = [row["min_ratio"] for row in sweeps["thickness_by_material"][slug]]
        ax[0].plot(thickness * 1000, ratios, "o-", color=COLORS[index], label=material["nombre"])
    ax[0].axhline(limits["flutter_ratio"], color=COLORS[3], linestyle="--", label="Límite")
    ax[0].axvline(s["fin_thickness_m"] * 1000, color="black", linestyle=":", label="Base")
    ax[0].set(xlabel="Espesor [mm]", ylabel="Mínimo Vf/V", title="Barrido de espesor")
    ax[0].legend(fontsize=8)
    material_rows = sweeps["materials"]
    ax[1].bar([row["nombre"] for row in material_rows],
              [row["required_thickness_mm"] for row in material_rows], color=COLORS[:len(material_rows)])
    ax[1].set(title="Espesor requerido en la trayectoria base", ylabel="Espesor [mm]")
    ax[1].tick_params(axis="x", rotation=35)
    save(fig, output, "04-thickness-sweep.png")

    scales = sorted({row["fin_scale"] for row in data["cases"]})
    scale_thickness = thickness * 1000
    matrix = []
    for scale in scales:
        case = next(row for row in data["cases"] if row["fin_scale"] == scale
                    and row["payload_kg"] == s["payload_kg"] and row["wind_m_s"] == s["wind_m_s"])
        case_trace = _trace_csv(output, case["case_id"])
        design = Design(**{k: case[k] for k in Design.__dataclass_fields__})
        matrix.append([
            np.min(flutter_speed(_fin(design, thickness=value / 1000), case_trace["pressure_pa"],
                                 case_trace["sound_speed_m_s"]) /
                   np.maximum(case_trace["airspeed_m_s"], 1e-9))
            for value in scale_thickness
        ])
    fig, axis = plt.subplots(figsize=(9, 5))
    image = axis.pcolormesh(scale_thickness, scales, np.asarray(matrix), shading="auto", cmap="viridis")
    axis.contour(scale_thickness, scales, np.asarray(matrix),
                 levels=[limits["flutter_ratio"]], colors="white")
    axis.set(xlabel="Espesor [mm]", ylabel="Escala de planta", title="Mapa geométrico · mínimo Vf/V")
    axis.text(0.02, 0.02, "Escala uniforme: solo cambia t/cr", transform=axis.transAxes, color="white")
    fig.colorbar(image, ax=axis, label="Mínimo Vf/V")
    axis.legend(handles=[
        Line2D([], [], color="white", label=f"Límite Vf/V = {limits['flutter_ratio']:g}"),
    ], loc="upper right")
    save(fig, output, "05-geometry-map.png")

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for index, scale in enumerate(scales):
        subset = sorted([row for row in data["cases"] if row["fin_scale"] == scale and row["wind_m_s"] == s["wind_m_s"]],
                        key=lambda row: row["payload_kg"])
        ax[0].plot([row["payload_kg"] for row in subset], [row["apogee_agl_m"] for row in subset],
                   "o-", color=COLORS[index], label=f"Aletas ×{scale:g}")
    ax[0].set(title="Apogeo con viento base", xlabel="Carga útil [kg]", ylabel="Apogeo AGL [m]")
    ax[0].legend()
    for admissible, color, marker, label in ((True, COLORS[0], "o", "Admisible"), (False, COLORS[3], "x", "No admisible")):
        subset = [row for row in data["cases"] if row["admissible"] == admissible]
        ax[1].scatter([row["min_flutter_ratio"] for row in subset], [row["apogee_agl_m"] for row in subset],
                      color=color, marker=marker, label=label)
    ax[1].axvline(limits["flutter_ratio"], color=COLORS[1], linestyle="--")
    ax[1].set(title="Apogeo frente a mínimo Vf/V", xlabel="Mínimo Vf/V", ylabel="Apogeo AGL [m]")
    ax[1].legend()
    save(fig, output, "06-design-space.png")

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for index, result in enumerate([drag_cases[0], base, drag_cases[1]]):
        a, summary = result["trace"], result["summary"]
        label = f"Cd ×{summary['drag_factor']:.2f}"
        ax[0].plot(a["time_s"], a["altitude_agl_m"], color=COLORS[index], label=label)
        ax[1].plot(a["time_s"], a["flutter_ratio"], color=COLORS[index], label=label)
    ax[0].set(title="Sensibilidad al arrastre", xlabel="Tiempo [s]", ylabel="Altura AGL [m]")
    ax[1].set(title="Sensibilidad del margen de flutter", xlabel="Tiempo [s]", ylabel="Vf/V")
    for axis in ax:
        axis.legend()
    save(fig, output, "07-drag-sensitivity.png")


def generate_report(output, data, base, thin, drag_cases, sweeps):
    plot_reports(output, data, base, thin, drag_cases, sweeps)
    payload = {"cases": data["cases"], "limits": data["config"]["limits"],
               "winds": data["config"]["winds_m_s"], "traces": {}}
    for case in data["cases"]:
        rows = _trace_csv(output, case["case_id"])
        indices = np.unique(np.linspace(0, len(rows["time_s"]) - 1, min(240, len(rows["time_s"])), dtype=int))
        payload["traces"][case["case_id"]] = {
            key: [round(float(rows[key][i]), 5) for i in indices]
            for key in ("time_s", "altitude_agl_m", "airspeed_m_s", "flutter_speed_m_s", "flutter_ratio")}
    template = (ROOT / "report_template.html").read_text(encoding="utf-8")
    s = base["summary"]
    sources = "".join(f'<li><a href="{html.escape(item["url"], quote=True)}">{html.escape(item["name"])}</a> · consultado {item["retrieved"]}</li>' for item in data["sources"])
    convergence_rows = "".join(f'<tr><td>{html.escape(key)}</td><td>{v["base"]:.5g}</td><td>{v["refined"]:.5g}</td><td>{v["relative_change"] * 100:.3f}%</td></tr>' for key, v in data["convergence"].items())
    values = {
        "PAYLOAD": json.dumps(payload, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c"),
        "APOGEE": f'{s["apogee_agl_m"]:,.0f}', "MAX_AIRSPEED": f'{s["max_airspeed_m_s"]:.1f}',
        "FLUTTER": f'{s["min_flutter_ratio"]:.2f}', "CASES": str(len(data["cases"])),
        "RAIL": f'{s["rail_exit_s"]:.3f}', "WIND": f'{s["wind_m_s"]:g}',
        "THIN": f'{thin["summary"]["fin_thickness_m"] * 1000:.2f}',
        "THIN_RATIO": f'{thin["summary"]["min_flutter_ratio"]:.2f}',
        "REQUIRED": f'{s["required_thickness_mm"]:.2f}',
        "MAXQ_RATIO": f'{s["ratio_at_max_q"]:.2f}', "MAXSPEED_RATIO": f'{s["ratio_at_max_speed"]:.2f}',
        "ALGEBRAIC": f'{data["thin_algebraic_min_ratio"]:.2f}',
        "ALGEBRAIC_DIFF": f'{data["thin_algebraic_relative_difference"] * 100:.2f}%',
        "BASE_STATUS": "No cumple cribado: " + "; ".join(data["baseline_reasons"]) if data["baseline_reasons"] else "Cumple los criterios numéricos de esta demo; no certifica seguridad",
        "TESTS": str(data["checks"]["unit_test_count"]), "SOURCES": sources,
        "CONVERGENCE": convergence_rows,
        "GENERATED": html.escape(data["generated_utc"]),
        "CONFIG": html.escape(json.dumps(data["config"], indent=2, ensure_ascii=False)),
        "REFINEMENT": "Comprobación numérica superada (<5%)" if data["checks"]["refinement_below_5_percent"] else "ATENCIÓN: refinamiento mayor al 5%",
    }
    for key, value in values.items():
        template = template.replace("@@" + key + "@@", value)
    (output / "index.html").write_text(template, encoding="utf-8")
