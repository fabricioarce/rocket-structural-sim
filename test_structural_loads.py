import unittest

import numpy as np

import structural_loads as sl


class LegacyRegressionTests(unittest.TestCase):
    def test_free_body_closes_shear(self):
        loads = [{"station": 1.0, "force": 10.0}, {"station": -0.9, "force": 10.0}]
        result = sl.shear_and_moment_diagram(loads, 2.0, 2.0)
        self.assertAlmostEqual(result["residual_shear_at_tail"], 0.0, places=8)

    def test_free_body_closes_bending(self):
        loads = [{"station": 1.0, "force": 10.0}, {"station": -0.9, "force": 10.0}]
        result = sl.shear_and_moment_diagram(loads, 2.0, 2.0)
        self.assertAlmostEqual(result["moment"][-1], 0.0, places=8)

    def test_invalid_tube_rejected(self):
        with self.assertRaises(ValueError):
            sl.TubeSection(outer_radius=0.05, thickness=0.06)


class AnalyticalTests(unittest.TestCase):
    def test_center_force_two_end_masses(self):
        result = sl.section_loads([0], [[10, 0, 0]], [-1, 1], [1, 1], [-1.1, 0, 1.1])
        np.testing.assert_allclose(result["moment"], [0, 5, 0], atol=1e-12)
        np.testing.assert_allclose(result["residual_force"], 0, atol=1e-12)
        np.testing.assert_allclose(result["residual_moment"], 0, atol=1e-12)

    def test_pure_couple_closes_both_ends(self):
        result = sl.section_loads([-1, 1], [[-10, 0, 0], [10, 0, 0]],
                                  [-0.5, 0.5], [1, 1], [-1.1, 0, 1.1])
        np.testing.assert_allclose(result["residual_moment"], 0, atol=1e-12)
        np.testing.assert_allclose(result["moment"][[0, -1]], 0, atol=1e-12)
        self.assertAlmostEqual(result["angular_acceleration"][1], 40)

    def test_axial_load_is_section_dependent(self):
        result = sl.section_loads([-1], [[0, 0, 100]], [-0.5, 0.5], [1, 1],
                                  [-1.1, -0.9, 0, 0.9, 1.1])
        np.testing.assert_allclose(result["axial"], [0, 100, 50, 0, 0], atol=1e-12)

    def test_translation_of_coordinates_preserves_loads(self):
        a = sl.section_loads([0], [[10, 3, 7]], [-1, 1], [1, 2], [-2, 0, 2])
        b = sl.section_loads([10], [[10, 3, 7]], [9, 11], [1, 2], [8, 10, 12])
        np.testing.assert_allclose(a["moment"], b["moment"], atol=1e-12)

    def test_two_bending_planes(self):
        result = sl.section_loads([0], [[6, 8, 0]], [-1, 1], [1, 1], [-2, 0, 2])
        self.assertAlmostEqual(result["moment"][1], 5)

    def test_stress_combines_at_same_section(self):
        section = sl.TubeSection(0.05, 0.001)
        actual = sl.combined_stress(np.array([10, 0]), np.array([0, 100]), section)
        np.testing.assert_allclose(actual, [10 * 0.05 / section.second_moment_of_area, 100 / section.area])

    def test_missing_mass_model_rejected(self):
        from types import SimpleNamespace
        flight = SimpleNamespace(out_of_rail_time=0.1, apogee_time=10)
        with self.assertRaisesRegex(ValueError, "distribución"):
            sl.analyze_time_step(flight, 1, [], 2, sl.TubeSection(0.05, 0.001))


if __name__ == "__main__":
    unittest.main()
