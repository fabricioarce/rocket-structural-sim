import unittest
from dataclasses import asdict

import numpy as np

from simulation import Design
from study import Limits, grid_designs, rejection_reasons, select_best, thickness_sweep


def case(payload=0, wind=0, apogee=3000):
    return {
        "payload_kg": payload, "fin_scale": 1, "wind_m_s": wind,
        "apogee_agl_m": apogee, "min_flutter_ratio": 2,
        "min_stability_cal": 2, "rail_speed_m_s": 25,
        "loaded_aoa_deg": 3, "max_mach": 0.8,
    }


class StudyTests(unittest.TestCase):
    def test_no_feasible_design_returns_none(self):
        best, rows = select_best([{**case(), "min_flutter_ratio": 1}], Limits(), 1)
        self.assertIsNone(best)
        self.assertIn("flutter", rows[0]["reasons"])

    def test_reject_best_altitude_when_over_limit(self):
        best, _ = select_best([{**case(), "min_flutter_ratio": 1}, case(payload=2)], Limits(), 1)
        self.assertEqual(best["payload_kg"], 2)

    def test_robust_selection_requires_all_scenarios(self):
        cases = [case(apogee=4000), {**case(wind=6), "min_flutter_ratio": 1},
                 case(payload=2, apogee=3100), case(payload=2, wind=6, apogee=2900)]
        best, _ = select_best(cases, Limits(), 2)
        self.assertEqual(best["worst_apogee_agl_m"], 2900)

    def test_missing_scenario_not_feasible(self):
        best, _ = select_best([case()], Limits(), 2)
        self.assertIsNone(best)

    def test_bad_model_domain_not_feasible(self):
        row = {**case(), "max_mach": 2}
        self.assertTrue(rejection_reasons(row, Limits()))

    def test_invalid_limit_rejected(self):
        with self.assertRaises(ValueError):
            Limits(flutter_ratio=float("nan"))

    def test_grid_updates_requested_parameters(self):
        rows = grid_designs(Design(), [0, 3], [0.85, 1.15], [0, 6])
        self.assertEqual(len(rows), 8)
        self.assertEqual(rows[-1].payload_kg, 3)
        self.assertEqual(rows[-1].fin_scale, 1.15)

    def test_grid_rejects_duplicate_scenarios(self):
        with self.assertRaises(ValueError):
            grid_designs(Design(), [0], [1], [0, 0])

    def test_thickness_sweep_monotonic(self):
        design = Design()
        result = {
            "summary": asdict(design),
            "trace": {
                "pressure_pa": np.array([101325, 90000]),
                "sound_speed_m_s": np.array([340, 335]),
                "airspeed_m_s": np.array([100, 150]),
            },
        }
        rows = thickness_sweep(result, [0.001, 0.002, 0.003])
        self.assertTrue(all(a["min_ratio"] < b["min_ratio"] for a, b in zip(rows, rows[1:])))


if __name__ == "__main__":
    unittest.main()
