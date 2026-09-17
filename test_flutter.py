import unittest

import numpy as np

from flutter import Fin, flutter_history, flutter_speed, required_thickness


class FlutterTests(unittest.TestCase):
    def test_bennett_2023_worked_example(self):
        inch = 0.0254
        fin = Fin(7.5 * inch, 2.5 * inch, 3 * inch, 4.285 * inch, 0.125 * inch, 600000 * 6894.757293)
        actual_fps = flutter_speed(fin, 7.2 * 6894.757293, 1043.36 * 0.3048) / 0.3048
        self.assertAlmostEqual(actual_fps, 1425, delta=4)

    def test_thickness_scaling(self):
        a = Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9)
        b = Fin(0.12, 0.06, 0.11, 0.06, 0.006, 26e9)
        self.assertAlmostEqual(flutter_speed(b, 101325, 340) / flutter_speed(a, 101325, 340), 2 ** 1.5)

    def test_pressure_and_stiffness_scaling(self):
        fin = Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9)
        values = flutter_speed(fin, np.array([101325, 101325 / 4]), 340)
        self.assertAlmostEqual(values[1] / values[0], 2)

    def test_nonphysical_geometry_rejected(self):
        with self.assertRaises(ValueError):
            Fin(0.12, 0.06, 0.11, 0.06, -0.003, 26e9)

    def test_zero_pressure_rejected(self):
        with self.assertRaises(ValueError):
            flutter_speed(Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9), 0, 340)

    def test_required_thickness_inverts_flutter_speed(self):
        fin = Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9)
        target = np.array([100, 250])
        thickness = required_thickness(fin, np.array([101325, 80000]), 340, target)
        candidate = Fin(fin.root_m, fin.tip_m, fin.span_m, fin.sweep_m, thickness[0], fin.shear_pa)
        self.assertAlmostEqual(flutter_speed(candidate, 101325, 340), target[0], places=10)

    def test_flutter_history_argmin(self):
        fin = Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9)
        history = flutter_history(fin, np.array([101325, 90000, 80000]), 340, np.array([100, 300, 100]))
        self.assertEqual(history["critical_index"], int(np.argmin(history["ratio"])))

    def test_uniform_planform_scaling(self):
        base = Fin(0.12, 0.06, 0.11, 0.06, 0.003, 26e9)
        scaled = Fin(0.24, 0.12, 0.22, 0.12, 0.003, 26e9)
        self.assertAlmostEqual(flutter_speed(scaled, 101325, 340) / flutter_speed(base, 101325, 340), 2 ** -1.5)


if __name__ == "__main__":
    unittest.main()
