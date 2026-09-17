import unittest

import numpy as np

from flutter import Fin, flutter_speed


class FlutterTests(unittest.TestCase):
    def test_bennett_2023_worked_example(self):
        inch = 0.0254
        fin = Fin(7.5*inch, 2.5*inch, 3*inch, 4.285*inch, 0.125*inch, 600000*6894.757293)
        actual_fps = flutter_speed(fin, 7.2*6894.757293, 1043.36*0.3048) / 0.3048
        self.assertAlmostEqual(actual_fps, 1425, delta=4)

    def test_thickness_scaling(self):
        a = Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9)
        b = Fin(0.12, 0.06, 0.11, 0.06, 0.006, 26e9)
        self.assertAlmostEqual(flutter_speed(b, 101325, 340) / flutter_speed(a, 101325, 340), 2**1.5)

    def test_pressure_and_stiffness_scaling(self):
        fin = Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9)
        values = flutter_speed(fin, np.array([101325, 101325/4]), 340)
        self.assertAlmostEqual(values[1]/values[0], 2)

    def test_nonphysical_geometry_rejected(self):
        with self.assertRaises(ValueError):
            Fin(0.12, 0.06, 0.11, 0.06, -0.003, 26e9)

    def test_zero_pressure_rejected(self):
        with self.assertRaises(ValueError):
            flutter_speed(Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9), 0, 340)


if __name__ == "__main__":
    unittest.main()
