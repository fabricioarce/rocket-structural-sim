import unittest

from simulation import Design, build_flight


class SimulationTests(unittest.TestCase):
    def test_design_validation(self):
        with self.assertRaises(ValueError):
            Design(fin_thickness_m=0)
        with self.assertRaises(ValueError):
            Design(payload_station_m=-2)

    def test_fin_mass_bookkeeping(self):
        base = Design()
        thin = Design(fin_thickness_m=base.fin_thickness_m / 2)
        self.assertAlmostEqual(thin.fin_mass, base.fin_mass / 2)

    def test_payload_shifts_cg_toward_payload_station(self):
        base = build_flight(Design(), max_time_step=0.3)
        loaded = build_flight(Design(payload_kg=3, payload_station_m=0.45), max_time_step=0.3)
        self.assertGreater(loaded.rocket.center_of_mass(0), base.rocket.center_of_mass(0))

    def test_build_flight_smoke(self):
        flight = build_flight(Design(), max_time_step=0.3)
        self.assertGreater(flight.apogee_time, flight.out_of_rail_time)
        self.assertIs(flight.design, flight.design)


if __name__ == "__main__":
    unittest.main()
