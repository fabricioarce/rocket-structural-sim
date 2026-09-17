"""Ejecutar: .venv/bin/python run_demo.py --open. No necesita conexión a internet."""

import argparse
import csv
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import subprocess
import sys
import webbrowser

import numpy as np

from simulation import DATA, Design, RADIUS
from structural_loads import TubeSection
from study import Limits, evaluate_case, grid_designs, rejection_reasons, select_best

ROOT = Path(__file__).resolve().parent


def jsonable(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"No serializable: {type(value)}")


def write_json(path, value):
    path.write_text(json.dumps(value, default=jsonable, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")


def write_columns(path, columns):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow(columns)
        writer.writerows(zip(*columns.values(), strict=True))


def load_config(path):
    config = json.loads(path.read_text(encoding="utf-8"))
    allowed = {"base", "section", "limits", "payloads_kg", "fin_scales", "winds_m_s", "samples", "mass_nodes"}
    if not isinstance(config, dict) or set(config) != allowed:
        raise ValueError(f"La configuración requiere exactamente estos campos: {sorted(allowed)}")
    base, section, limits = Design(**config["base"]), TubeSection(**config["section"]), Limits(**config["limits"])
    if abs(section.outer_radius-RADIUS) > 1e-10:
        raise ValueError("El radio de la sección debe coincidir con Calisto (0.0635 m)")
    for key, lower, upper in (("samples", 30, 3000), ("mass_nodes", 8, 128)):
        if type(config[key]) is not int or not lower <= config[key] <= upper:
            raise ValueError(f"{key} debe ser un entero entre {lower} y {upper}")
    grid_designs(base, config["payloads_kg"], config["fin_scales"], config["winds_m_s"])
    if base.wind_m_s not in config["winds_m_s"]:
        raise ValueError("El viento del caso base debe estar incluido en winds_m_s")
    return config, base, section, limits


def run(config_path, output, quick=False):
    config, base, section, limits = load_config(config_path)
    output.mkdir(parents=True, exist_ok=True)
    check = subprocess.run([sys.executable, "-m", "unittest", "discover", "-v"], cwd=ROOT,
                           text=True, capture_output=True)
    (output / "tests.txt").write_text(check.stdout + check.stderr, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(f"Fallaron las pruebas; consulte {output / 'tests.txt'}")
    if quick:
        config["payloads_kg"], config["fin_scales"] = [base.payload_kg], [base.fin_scale]
    designs = grid_designs(base, config["payloads_kg"], config["fin_scales"], config["winds_m_s"])
    rows, summaries = [], []
    baseline = None
    for index, design in enumerate(designs, 1):
        print(f"[{index}/{len(designs)}] carga útil +{design.payload_kg:g} kg | aletas ×{design.fin_scale:g} | viento {design.wind_m_s:g} m/s", flush=True)
        result = evaluate_case(design, section, config["samples"], config["mass_nodes"])
        case_id = f"case-{index:03d}"
        summary = {"case_id": case_id, **result["summary"]}
        reasons = rejection_reasons(summary, limits)
        summary.update(admissible=not reasons, reasons=reasons)
        summaries.append(summary)
        rows.append({**summary, "reasons": "; ".join(reasons)})
        write_columns(output / f"{case_id}.csv", result["trace"])
        if design == base:
            baseline = result
    if baseline is None:
        baseline = evaluate_case(base, section, config["samples"], config["mass_nodes"])
    print("Chequeando aletas delgadas y sensibilidad al arrastre...", flush=True)
    thin = evaluate_case(replace(base, fin_thickness_m=base.fin_thickness_m*0.4), section,
                         config["samples"], config["mass_nodes"])
    drag_cases = [evaluate_case(replace(base, drag_factor=base.drag_factor*factor), section,
                               config["samples"], config["mass_nodes"]) for factor in (0.85, 1.15)]
    print("Comprobando refinamiento temporal y de distribución de masas...", flush=True)
    refined = evaluate_case(base, section, config["samples"]*2, config["mass_nodes"]*2, max_time_step=0.06)
    b, r = baseline["summary"], refined["summary"]
    convergence = {key: {"base": b[key], "refined": r[key],
                          "relative_change": abs(r[key]-b[key])/max(abs(r[key]), 1e-12)}
                   for key in ("stress_mpa", "max_moment_nm", "apogee_agl_m", "min_flutter_ratio")}
    convergence_ok = all(v["relative_change"] < 0.05 for v in convergence.values())
    best, ranked = select_best(summaries, limits, len(config["winds_m_s"]))
    sources = [
        {"name": "RocketPy: ejemplo oficial y datos Calisto", "url": "https://docs.rocketpy.org/en/latest/user/first_simulation.html", "retrieved": "2026-09-15"},
        {"name": "RocketPy: Flight, coordenadas y velocidad relativa", "url": "https://docs.rocketpy.org/en/latest/reference/classes/Flight.html", "retrieved": "2026-09-15"},
        {"name": "Bennett (2023): flutter corregido y ejemplo de 1425 ft/s", "url": "https://www.nakka-rocketry.net/articles/Calculating_Fin_Flutter_Velocity_Bennett-12-23.pdf", "retrieved": "2026-09-15"},
        {"name": "OpenRocket: no incluye análisis de flutter", "url": "https://wiki.openrocket.info/Third-Party_Compatibility", "retrieved": "2026-09-15"},
    ]
    manifest = {str(p.relative_to(DATA)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(DATA.rglob("*")) if p.is_file()}
    checks = {"unit_tests_passed": True,
              "unit_test_count": int(re.search(r"Ran (\d+) tests", check.stderr).group(1)),
              "refinement_below_5_percent": convergence_ok,
              "experimental_validation": False, "independent_fea_validation": False}
    result = {
        "generated_utc": datetime.now(timezone.utc).isoformat(), "mode": "demo preliminar",
        "versions": {name: importlib.metadata.version(name) for name in ("rocketpy", "numpy", "scipy", "matplotlib")},
        "python": sys.version.split()[0], "config": config, "checks": checks,
        "baseline": b, "baseline_reasons": rejection_reasons(b, limits), "thin_fin": thin["summary"],
        "drag_sensitivity": [c["summary"] for c in drag_cases], "cases": summaries,
        "best_sampled_design": best, "ranked_designs": ranked, "convergence": convergence,
        "sources": sources, "data_sha256": manifest,
    }
    write_json(output / "results.json", result)
    write_json(output / "effective-config.json", config)
    with (output / "cases.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    write_columns(output / "baseline.csv", baseline["trace"])
    write_columns(output / "critical-diagram.csv", baseline["critical_diagram"])
    write_columns(output / "thin-fin.csv", thin["trace"])
    from report import generate_report
    generate_report(output, result, baseline, thin, drag_cases)
    print(f"\nInforme: {(output / 'index.html').resolve()}")
    print(f"Pruebas: {checks['unit_test_count']} OK. Refinamiento <5%: {convergence_ok}.")
    print("Mejor diseño muestreado:", best if best else "Ninguno cumple todas las restricciones.")
    if not convergence_ok:
        raise RuntimeError("El refinamiento supera 5%; consulte el informe antes de interpretar resultados")
    return output / "index.html"


def main():
    parser = argparse.ArgumentParser(description="Demo Calisto: vuelo, cargas, flutter, barrido y gráficas offline")
    parser.add_argument("--config", type=Path, default=ROOT / "demo.json", help="Configuración JSON en SI")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs", help="Carpeta de resultados regenerables")
    parser.add_argument("--quick", action="store_true", help="Solo el diseño base en los escenarios de viento; sin barrido geométrico")
    parser.add_argument("--open", action="store_true", help="Abrir el informe local en el navegador")
    args = parser.parse_args()
    try:
        report = run(args.config, args.output, args.quick)
    except (ValueError, TypeError, KeyError, OSError, RuntimeError) as error:
        parser.exit(1, f"Error: {error}\n")
    if args.open:
        webbrowser.open(report.resolve().as_uri())


if __name__ == "__main__":
    main()
