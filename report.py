"""Informe HTML sin servicios externos y figuras PNG reproducibles."""

import csv
import html
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
COLORS = ("#007f86", "#e4763a", "#5266a6", "#bb425a")


def save(fig, output, filename):
    fig.tight_layout(pad=1.8)
    fig.savefig(output / filename, dpi=155, facecolor="white")
    plt.close(fig)


def plot_reports(output, data, base, thin, drag_cases):
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
    ax[0, 1].set(title="La velocidad relevante depende del análisis", ylabel="Velocidad [m/s]")
    ax[0, 1].legend()
    ax[1, 0].plot(t, trace["q_pa"]/1000, color=COLORS[0])
    ax[1, 0].axvline(s["max_q_time_s"], color=COLORS[1], linestyle="--", label="Max-Q")
    ax[1, 0].set(title="Presión dinámica: q = ½ ρ V² relativa", ylabel="q [kPa]")
    ax[1, 0].legend()
    ax[1, 1].plot(t, trace["stability_cal"], color=COLORS[0])
    ax[1, 1].axhline(limits["stability_cal"], color=COLORS[1], linestyle="--", label="Límite de cribado")
    ax[1, 1].set(title="Margen estático dependiente de Mach", ylabel="Calibres")
    ax[1, 1].legend()
    for axis in ax.flat:
        axis.set_xlabel("Tiempo desde ignición [s]")
    fig.suptitle("Caso base · ascenso libre (después de abandonar el riel)", fontsize=14)
    save(fig, output, "01-flight.png")

    fig, ax = plt.subplots(3, 1, figsize=(12, 9), sharex=True)
    ax[0].plot(t, trace["stress_mpa"], color=COLORS[0])
    ax[0].axhline(limits["stress_mpa"], color=COLORS[3], linestyle=":", label="Límite de estudio supuesto")
    ax[0].set(ylabel="Máx. |σ| [MPa]", title="Esfuerzo longitudinal combinado máximo, calculado sección por sección")
    ax[1].plot(t, trace["max_moment_nm"], color=COLORS[0])
    ax[1].set(ylabel="Máx. |M| [N·m]", title="Flexión resultante en dos planos")
    ax[2].plot(t, trace["max_axial_n"], color=COLORS[0])
    ax[2].set(ylabel="Máx. N [N]", title="Compresión axial interna", xlabel="Tiempo desde ignición [s]")
    for axis in ax:
        axis.axvline(s["critical_time_s"], color=COLORS[1], linestyle="--", label="Máximo esfuerzo")
        axis.axvline(s["max_q_time_s"], color=COLORS[2], linestyle=":", label="Max-Q")
        axis.legend(loc="upper right", ncol=3, fontsize=8)
    save(fig, output, "02-load-history.png")

    d = base["critical_diagram"]
    fig, ax = plt.subplots(2, 2, figsize=(12, 7))
    for axis, key, title, unit in zip(ax.flat,
            ("axial_n", "shear_n", "moment_nm", "stress_mpa"),
            ("Carga axial (+ compresión)", "Cortante resultante", "Momento flector resultante", "Esfuerzo combinado"),
            ("N", "N", "N·m", "MPa"), strict=True):
        axis.plot(d["station_m"], d[key], color=COLORS[0])
        axis.set(title=title, ylabel=unit, xlabel="Estación axial [m], +z hacia la nariz")
    fig.suptitle(f"Cortes en t = {s['critical_time_s']:.3f} s · no es una viga empotrada", fontsize=14)
    save(fig, output, "03-section-diagrams.png")

    fig, axis = plt.subplots(figsize=(12, 5))
    image = axis.pcolormesh(t, base["heat_stations"], base["heatmap"].T, shading="auto", cmap="magma")
    axis.plot(s["critical_time_s"], s["critical_station_m"], "o", color="cyan", markersize=6, label="Sección crítica")
    axis.set(xlabel="Tiempo desde ignición [s]", ylabel="Estación axial [m]", title="Mapa de esfuerzo longitudinal combinado (interpolación visual)")
    axis.legend()
    fig.colorbar(image, ax=axis, label="MPa")
    save(fig, output, "04-stress-map.png")

    fig, ax = plt.subplots(2, 2, figsize=(12, 8))
    ax[0, 0].plot(t, trace["airspeed_m_s"], color=COLORS[0], label="Velocidad relativa")
    ax[0, 0].plot(t, trace["flutter_speed_m_s"], color=COLORS[2], label="Frontera de flutter base")
    ax[0, 0].plot(thin["trace"]["time_s"], thin["trace"]["flutter_speed_m_s"], color=COLORS[3], linestyle="--", label="Frontera con espesor ×0.4")
    ax[0, 0].plot(thin["trace"]["time_s"], thin["trace"]["airspeed_m_s"], color=COLORS[1], linestyle=":", label="Velocidad con espesor ×0.4")
    ax[0, 0].set(title="Velocidad real frente a frontera empírica", xlabel="Tiempo [s]", ylabel="Velocidad [m/s]")
    ax[0, 0].legend(fontsize=8)
    ax[0, 1].plot(t, trace["flutter_ratio"], color=COLORS[0], label="Base")
    ax[0, 1].plot(thin["trace"]["time_s"], thin["trace"]["flutter_ratio"], color=COLORS[3], label="Aletas delgadas")
    ax[0, 1].axhline(1, color="black", linestyle=":", label="Frontera Vf/V = 1")
    ax[0, 1].axhline(limits["flutter_ratio"], color=COLORS[1], linestyle="--", label="Límite elegido")
    ax[0, 1].set(ylim=(0, min(6, max(3, trace["flutter_ratio"].min()*2))), title="Margen a lo largo del ascenso", xlabel="Tiempo [s]", ylabel="Vf / V relativa")
    ax[0, 1].legend(fontsize=8)
    ax[1, 0].plot(trace["altitude_asl_m"], trace["airspeed_m_s"], color=COLORS[0], label="Velocidad relativa")
    ax[1, 0].plot(trace["altitude_asl_m"], trace["flutter_speed_m_s"], color=COLORS[2], label="Vf calculada localmente")
    ax[1, 0].set(title="La altitud atmosférica es ASL, no AGL", xlabel="Altitud sobre el mar [m]", ylabel="Velocidad [m/s]")
    ax[1, 0].legend(fontsize=8)
    ax[1, 1].plot(trace["altitude_asl_m"], trace["density_kg_m3"], color=COLORS[0])
    ax[1, 1].set(title="Densidad local de la atmósfera estándar", xlabel="Altitud sobre el mar [m]", ylabel="Densidad [kg/m³]")
    fig.suptitle("Flutter: cribado flexión-torsión, no simulación de vibración ni rotura", fontsize=14)
    save(fig, output, "05-flutter.png")

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    rows = data["cases"]
    for idx, scale in enumerate(sorted({r["fin_scale"] for r in rows})):
        subset = sorted([r for r in rows if r["fin_scale"] == scale and r["wind_m_s"] == s["wind_m_s"]], key=lambda r: r["payload_kg"])
        ax[0].plot([r["payload_kg"] for r in subset], [r["apogee_agl_m"] for r in subset], "o-", color=COLORS[idx % len(COLORS)], label=f"Aletas ×{scale:g}")
    ax[0].set(title=f"Altura con viento de {s['wind_m_s']:g} m/s", xlabel="Carga útil añadida [kg]", ylabel="Apogeo AGL [m]")
    ax[0].legend()
    for admissible, color, marker, label in ((True, COLORS[0], "o", "Cumple cribado"), (False, COLORS[3], "x", "Incumple algún criterio")):
        subset = [r for r in rows if r["admissible"] == admissible]
        ax[1].scatter([r["stress_mpa"] for r in subset], [r["apogee_agl_m"] for r in subset], color=color, marker=marker, label=label)
    ax[1].axvline(limits["stress_mpa"], color=COLORS[1], linestyle="--")
    ax[1].set(title="Altura frente al máximo esfuerzo (todos los vientos)", xlabel="Máximo esfuerzo [MPa]", ylabel="Apogeo AGL [m]")
    ax[1].legend(fontsize=8)
    save(fig, output, "06-design-space.png")

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for idx, result in enumerate([drag_cases[0], base, drag_cases[1]]):
        a, b = result["trace"], result["summary"]
        label = f"Cd ×{b['drag_factor']:.2f}"
        ax[0].plot(a["time_s"], a["altitude_agl_m"], color=COLORS[idx], label=label)
        ax[1].plot(a["time_s"], a["stress_mpa"], color=COLORS[idx], label=label)
    ax[0].set(title="Sensibilidad al arrastre: no es una variable de diseño", xlabel="Tiempo [s]", ylabel="Altura AGL [m]")
    ax[1].set(title="Esfuerzo con Cd variable", xlabel="Tiempo [s]", ylabel="Máx. esfuerzo [MPa]")
    for axis in ax:
        axis.legend()
    save(fig, output, "07-drag-sensitivity.png")


def generate_report(output, data, base, thin, drag_cases):
    plot_reports(output, data, base, thin, drag_cases)
    payload = {"cases": data["cases"], "limits": data["config"]["limits"],
               "winds": data["config"]["winds_m_s"], "traces": {}}
    for case in data["cases"]:
        with (output / f"{case['case_id']}.csv").open(encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        indices = np.unique(np.linspace(0, len(rows)-1, min(240, len(rows)), dtype=int))
        payload["traces"][case["case_id"]] = {
            key: [round(float(rows[i][key]), 5) for i in indices]
            for key in ("time_s", "altitude_agl_m", "airspeed_m_s", "stress_mpa", "flutter_ratio")}
    template = (ROOT / "report_template.html").read_text(encoding="utf-8")
    s = base["summary"]
    sources = "".join(f'<li><a href="{html.escape(item["url"], quote=True)}">{html.escape(item["name"])}</a> · consultado {item["retrieved"]}</li>' for item in data["sources"])
    convergence_rows = "".join(f'<tr><td>{html.escape(key)}</td><td>{v["base"]:.5g}</td><td>{v["refined"]:.5g}</td><td>{v["relative_change"]*100:.3f}%</td></tr>' for key, v in data["convergence"].items())
    reasons = data["baseline_reasons"]
    values = {
        "PAYLOAD": json.dumps(payload, ensure_ascii=False, allow_nan=False).replace("<", "\\u003c"),
        "APOGEE": f'{s["apogee_agl_m"]:,.0f}', "STRESS": f'{s["stress_mpa"]:.2f}',
        "FLUTTER": f'{s["min_flutter_ratio"]:.2f}', "CASES": str(len(data["cases"])),
        "CRITICAL": f'{s["critical_time_s"]:.3f}', "MAXQ": f'{s["max_q_time_s"]:.3f}',
        "STATION": f'{s["critical_station_m"]:.3f}', "RAIL": f'{s["rail_exit_s"]:.3f}',
        "WIND": f'{s["wind_m_s"]:g}', "THIN": f'{thin["summary"]["fin_thickness_m"]*1000:.2f}',
        "THIN_RATIO": f'{thin["summary"]["min_flutter_ratio"]:.2f}',
        "BASE_STATUS": "No cumple cribado: " + "; ".join(reasons) if reasons else "Cumple los criterios numéricos de esta demo; no certifica seguridad",
        "TESTS": str(data["checks"]["unit_test_count"]), "SOURCES": sources,
        "CONVERGENCE": convergence_rows, "CLOSURE": f'{s["force_residual_n"]:.2e} N / {s["moment_residual_nm"]:.2e} N·m',
        "GENERATED": html.escape(data["generated_utc"]), "CONFIG": html.escape(json.dumps(data["config"], indent=2, ensure_ascii=False)),
        "REFINEMENT": "Comprobación numérica superada (<5%)" if data["checks"]["refinement_below_5_percent"] else "ATENCIÓN: refinamiento mayor al 5%",
    }
    for key, value in values.items():
        template = template.replace("@@"+key+"@@", value)
    (output / "index.html").write_text(template, encoding="utf-8")
