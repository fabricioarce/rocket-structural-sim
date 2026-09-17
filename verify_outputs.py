"""Comprobar exportaciones: .venv/bin/python verify_outputs.py [outputs]."""

import csv
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image

from study import Limits, select_best


def verify(output):
    data = json.loads((output / "results.json").read_text(encoding="utf-8"))
    assert data["checks"]["unit_tests_passed"]
    assert data["checks"]["refinement_below_5_percent"]
    for case in data["cases"]:
        with (output / f"{case['case_id']}.csv").open(encoding="utf-8") as stream:
            records = list(csv.DictReader(stream))
        values = np.array([[float(v) for v in r.values()] for r in records])
        assert np.isfinite(values).all()
        times = np.array([float(r["time_s"]) for r in records])
        assert (np.diff(times) > 0).all()
        assert times[0] > case["rail_exit_s"]
        assert times[-1] <= case["apogee_time_s"]
        assert len(records) == case["samples"]
        np.testing.assert_allclose(max(float(r["stress_mpa"]) for r in records), case["stress_mpa"])
        np.testing.assert_allclose(min(float(r["flutter_ratio"]) for r in records), case["min_flutter_ratio"])
    best, ranked = select_best(data["cases"], Limits(**data["config"]["limits"]), len(data["config"]["winds_m_s"]))
    assert best == data["best_sampled_design"]
    assert ranked == data["ranked_designs"]
    with (output / "critical-diagram.csv").open(encoding="utf-8") as stream:
        cuts = list(csv.DictReader(stream))
    for cut in (cuts[0], cuts[-1]):
        for key in ("axial_n", "shear_n", "moment_nm", "stress_mpa"):
            assert abs(float(cut[key])) < 1e-7, (key, cut[key])
    images = list(output.glob("*.png"))
    assert len(images) == 7
    for image in images:
        with Image.open(image) as img:
            img.verify()
    print(f"OK: {len(data['cases'])} series CSV finitas, ordenadas y consistentes; selección reproducible, extremos libres y 7 PNG válidos.")


if __name__ == "__main__":
    verify(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "outputs")
