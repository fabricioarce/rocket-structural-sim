import unittest
from dataclasses import replace

from simulation import Design
from study import Limits, grid_designs, rejection_reasons, select_best


def case(payload=0, wind=0, apogee=3000, stress=2):
    return {"payload_kg": payload, "fin_scale": 1, "wind_m_s": wind,
            "apogee_agl_m": apogee, "stress_mpa": stress, "min_flutter_ratio": 2,
            "min_stability_cal": 2, "rail_speed_m_s": 25, "loaded_aoa_deg": 3, "max_mach": 0.8}


class StudyTests(unittest.TestCase):
    def test_no_feasible_design_returns_none(self):
        best, rows = select_best([case(stress=20)], Limits(), 1)
        self.assertIsNone(best)
        self.assertIn("esfuerzo", rows[0]["reasons"])

    def test_reject_best_altitude_when_over_limit(self):
        best, _ = select_best([case(apogee=5000, stress=20), case(payload=2)], Limits(), 1)
        self.assertEqual(best["payload_kg"], 2)

    def test_robust_selection_requires_all_scenarios(self):
        cases = [case(apogee=4000), case(wind=6, stress=20),
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
            Limits(stress_mpa=float("nan"))

    def test_grid_updates_requested_parameters(self):
        rows = grid_designs(Design(), [0, 3], [0.85, 1.15], [0, 6])
        self.assertEqual(len(rows), 8)
        self.assertEqual(rows[-1].payload_kg, 3)
        self.assertEqual(rows[-1].fin_scale, 1.15)

    def test_grid_rejects_duplicate_scenarios(self):
        with self.assertRaises(ValueError):
            grid_designs(Design(), [0], [1], [0, 0])


if __name__ == "__main__":
    unittest.main()
