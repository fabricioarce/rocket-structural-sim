import unittest

import numpy as np

from simulation import Design, build_flight, dry_mass_nodes
from structural_loads import TubeSection, analyze_time_step, get_point_loads, get_surface_stations


class SimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.flight = build_flight(Design(payload_kg=3, fin_scale=1.15))
        cls.surfaces = get_surface_stations(cls.flight.rocket)

    def test_mass_and_cg_match_rocketpy_during_burn(self):
        f = self.flight
        for t in (0, 1, 2, 3.9, 5):
            positions, masses = f.structural_mass_model(t)
            self.assertAlmostEqual(masses.sum(), f.rocket.total_mass(t), places=10)
            self.assertAlmostEqual(np.dot(masses, positions)/masses.sum(), f.rocket.center_of_mass(t), delta=1e-8)

    def test_mass_nodes_stay_inside_declared_bounds(self):
        f = self.flight
        for t in (0, 1, 2, 3.9, 5):
            positions, _ = f.structural_mass_model(t)
            self.assertGreaterEqual(positions.min(), f.structural_bounds[0])
            self.assertLessEqual(positions.max(), f.structural_bounds[1])

    def test_baseline_dry_aggregate_properties(self):
        positions, masses = dry_mass_nodes(Design())
        self.assertAlmostEqual(masses.sum(), 14.426, places=10)
        self.assertAlmostEqual(np.dot(masses, positions), 0, places=10)
        self.assertAlmostEqual(np.dot(masses, positions**2), 6.321, places=10)

    def test_component_forces_match_rocketpy_at_solver_nodes(self):
        f = self.flight
        times = np.asarray(f.solution)[:, 0]
        for target in (0.5, 1, 3, 5):
            t = times[np.argmin(abs(times-target))]
            loads = get_point_loads(f, t, self.surfaces)
            reconstructed = sum((item["force"] for item in loads))
            np.testing.assert_allclose(reconstructed[:2], [f.R1(t), f.R2(t)], rtol=1e-5, atol=1e-6)

    def test_rail_loads_not_silently_treated_as_free_flight(self):
        with self.assertRaisesRegex(ValueError, "riel"):
            analyze_time_step(self.flight, 0.1, self.surfaces, 2.533, TubeSection(0.0635, 0.0015))

    def test_flight_cut_equilibrium(self):
        r = analyze_time_step(self.flight, 1, self.surfaces, 2.533, TubeSection(0.0635, 0.0015))
        np.testing.assert_allclose(r["diagram"]["residual_force"], 0, atol=1e-8)
        np.testing.assert_allclose(r["diagram"]["residual_moment"], 0, atol=1e-8)


if __name__ == "__main__":
    unittest.main()
