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

from materials import MATERIALS
from simulation import DATA, Design
from study import Limits, evaluate_case, grid_designs, material_sweep, rejection_reasons, select_best, thickness_sweep

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
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(zip(*columns.values(), strict=True))


def load_config(path):
    config = json.loads(path.read_text(encoding="utf-8"))
    allowed = {"base", "limits", "payloads_kg", "fin_scales", "winds_m_s", "samples",
               "thickness_sweep_mm", "materials"}
    if not isinstance(config, dict) or set(config) != allowed:
        raise ValueError(f"La configuración requiere exactamente estos campos: {sorted(allowed)}")
    base, limits = Design(**config["base"]), Limits(**config["limits"])
    if type(config["samples"]) is not int or not 30 <= config["samples"] <= 3000:
        raise ValueError("samples debe ser un entero entre 30 y 3000")
    if not config["thickness_sweep_mm"] or not all(float(v) > 0 for v in config["thickness_sweep_mm"]):
        raise ValueError("thickness_sweep_mm debe ser una lista positiva")
    if not config["materials"] or any(slug not in MATERIALS for slug in config["materials"]):
        raise ValueError("materials contiene un slug desconocido o está vacío")
    grid_designs(base, config["payloads_kg"], config["fin_scales"], config["winds_m_s"])
    if base.wind_m_s not in config["winds_m_s"]:
        raise ValueError("El viento del caso base debe estar incluido en winds_m_s")
    return config, base, limits


def run(config_path, output, quick=False):
    config, base, limits = load_config(config_path)
    output.mkdir(parents=True, exist_ok=True)
    for path in output.iterdir():
        if path.is_file():
            path.unlink()
    check = subprocess.run([sys.executable, "-m", "unittest", "discover", "-v"], cwd=ROOT,
                           text=True, capture_output=True)
    (output / "tests.txt").write_text(check.stdout + check.stderr, encoding="utf-8")
    if check.returncode:
        raise RuntimeError(f"Fallaron las pruebas; consulte {output / 'tests.txt'}")
    if quick:
        config = {**config, "payloads_kg": [base.payload_kg], "fin_scales": [base.fin_scale]}
    designs = grid_designs(base, config["payloads_kg"], config["fin_scales"], config["winds_m_s"])
    rows, summaries = [], []
    baseline = None
    for index, design in enumerate(designs, 1):
        print(f"[{index}/{len(designs)}] carga útil +{design.payload_kg:g} kg | aletas ×{design.fin_scale:g} | viento {design.wind_m_s:g} m/s", flush=True)
        result = evaluate_case(design, config["samples"], target_ratio=limits.flutter_ratio)
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
        baseline = evaluate_case(base, config["samples"], target_ratio=limits.flutter_ratio)
    print("Chequeando aletas delgadas, materiales y sensibilidad al arrastre...", flush=True)
    thin_design = replace(base, fin_thickness_m=base.fin_thickness_m * 0.4)
    thin = evaluate_case(thin_design, config["samples"], target_ratio=limits.flutter_ratio)
    drag_cases = [
        evaluate_case(replace(base, drag_factor=base.drag_factor * factor), config["samples"],
                      target_ratio=limits.flutter_ratio)
        for factor in (0.85, 1.15)
    ]
    thickness_values = [float(value) / 1000 for value in config["thickness_sweep_mm"]]
    thickness = thickness_sweep(baseline, thickness_values)
    materials = material_sweep(baseline, config["materials"], limits.flutter_ratio)
    thickness_by_material = {
        slug: thickness_sweep(baseline, thickness_values, MATERIALS[slug]["shear_pa"])
        for slug in config["materials"]
    }
    thin_algebraic = thickness_sweep(baseline, [thin_design.fin_thickness_m])[0]["min_ratio"]
    algebraic_relative_difference = abs(thin_algebraic - thin["summary"]["min_flutter_ratio"]) / thin["summary"]["min_flutter_ratio"]
    print("Comprobando refinamiento temporal...", flush=True)
    refined = evaluate_case(base, config["samples"] * 2, max_time_step=0.06, target_ratio=limits.flutter_ratio)
    b, r = baseline["summary"], refined["summary"]
    convergence = {
        key: {"base": b[key], "refined": r[key],
              "relative_change": abs(r[key] - b[key]) / max(abs(r[key]), 1e-12)}
        for key in ("apogee_agl_m", "max_airspeed_m_s", "min_flutter_ratio")
    }
    convergence_ok = all(v["relative_change"] < 0.05 for v in convergence.values())
    best, ranked = select_best(summaries, limits, len(config["winds_m_s"]))
    sources = [
        {"name": "RocketPy: ejemplo oficial y datos Calisto", "url": "https://docs.rocketpy.org/en/latest/user/first_simulation.html", "retrieved": "2026-09-15"},
        {"name": "RocketPy: Flight, coordenadas y velocidad relativa", "url": "https://docs.rocketpy.org/en/latest/reference/classes/Flight.html", "retrieved": "2026-09-15"},
        {"name": "Bennett (2023): flutter corregido y ejemplo de 1425 ft/s", "url": "https://www.nakka-rocketry.net/articles/Calculating_Fin_Flutter_Velocity_Bennett-12-23.pdf", "retrieved": "2026-09-15"},
        {"name": "OpenRocket: no incluye análisis de flutter", "url": "https://wiki.openrocket.info/Third-Party_Compatibility", "retrieved": "2026-09-15"},
        {"name": "Apogee Components: Peak of Flight, flutter de aletas", "url": "https://www.apogeerockets.com/Peak-of-Flight/Newsletter", "retrieved": "2026-09-15"},
    ]
    manifest = {str(p.relative_to(DATA)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(DATA.rglob("*")) if p.is_file()}
    unit_count = int(re.search(r"Ran (\d+) tests", check.stderr).group(1))
    checks = {
        "unit_tests_passed": True,
        "unit_test_count": unit_count,
        "refinement_below_5_percent": convergence_ok,
        "algebraic_vs_resimulated_thin_fin": algebraic_relative_difference < 0.02,
    }
    result = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "demo preliminar", "versions": {name: importlib.metadata.version(name)
        for name in ("rocketpy", "numpy", "scipy", "matplotlib")},
        "python": sys.version.split()[0], "config": config, "checks": checks,
        "baseline": b, "baseline_reasons": rejection_reasons(b, limits),
        "thin_fin": thin["summary"], "drag_sensitivity": [c["summary"] for c in drag_cases],
        "cases": summaries, "best_sampled_design": best, "ranked_designs": ranked,
        "convergence": convergence, "thickness_sweep": thickness,
        "thickness_sweep_materials": thickness_by_material, "material_sweep": materials,
        "thin_algebraic_min_ratio": thin_algebraic,
        "thin_algebraic_relative_difference": algebraic_relative_difference,
        "sources": sources, "data_sha256": manifest,
    }
    write_json(output / "results.json", result)
    write_json(output / "effective-config.json", config)
    with (output / "cases.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_columns(output / "baseline.csv", baseline["trace"])
    write_columns(output / "thin-fin.csv", thin["trace"])
    write_columns(output / "thickness-sweep.csv", {
        "thickness_mm": [row["thickness_m"] * 1000 for row in thickness],
        **{slug: [row["min_ratio"] for row in thickness_by_material[slug]] for slug in config["materials"]},
    })
    write_columns(output / "material-sweep.csv", {
        "slug": [row["slug"] for row in materials],
        "nombre": [row["nombre"] for row in materials],
        "min_ratio": [row["min_ratio"] for row in materials],
        "shear_pa": [row["shear_pa"] for row in materials],
        "density_kg_m3": [row["density_kg_m3"] for row in materials],
        "required_thickness_mm": [row["required_thickness_mm"] for row in materials],
    })
    from report import generate_report
    sweeps = {"thickness": thickness, "thickness_by_material": thickness_by_material,
              "materials": materials, "thin_algebraic_min_ratio": thin_algebraic}
    generate_report(output, result, baseline, thin, drag_cases, sweeps)
    print(f"\nInforme: {(output / 'index.html').resolve()}")
    print(f"Pruebas: {checks['unit_test_count']} OK. Refinamiento <5%: {convergence_ok}.")
    print("Mejor diseño muestreado:", best if best else "Ninguno cumple todas las restricciones.")
    if not convergence_ok or not checks["algebraic_vs_resimulated_thin_fin"]:
        raise RuntimeError("Falló una comprobación numérica; consulte el informe")
    return output / "index.html"


def main():
    parser = argparse.ArgumentParser(description="Demo Calisto: vuelo, flutter, barridos y gráficas offline")
    parser.add_argument("--config", type=Path, default=ROOT / "demo.json", help="Configuración JSON en SI")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs", help="Carpeta de resultados regenerables")
    parser.add_argument("--quick", action="store_true", help="Solo el diseño base en los escenarios de viento")
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
