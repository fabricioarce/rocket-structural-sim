"""Cribado de flutter flexión-torsión; no predice rotura ni amplitud de vibración.

Fuente: John K. Bennett, Fin Flutter Analysis Revisited (Again), diciembre 2023,
páginas 5–9. Consultado 2026-09-15:
https://www.nakka-rocketry.net/articles/Calculating_Fin_Flutter_Velocity_Bennett-12-23.pdf

Vf/a = sqrt(G*(AR+2)*(t/cr)^3 / ((24*epsilon*gamma/pi)*p*AR^3*(1+lambda)/2)).
epsilon = Cx/cr - 1/4; gamma=1.4. Presión y G deben usar las mismas unidades.
Se comprueba contra el ejemplo publicado de 1425 ft/s; no se utiliza la forma
antigua con la doble división por dos que sobreestima Vf por sqrt(2).

Aletas trapezoidales homogéneas, espesor constante, propiedades efectivas
isótropas. No resuelve laminados, modos, uniones, amortiguamiento ni divergencia.
Rebasar esta frontera señala riesgo según el modelo, no una rotura segura.
"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Fin:
    root_m: float
    tip_m: float
    span_m: float
    sweep_m: float
    thickness_m: float
    shear_pa: float

    def __post_init__(self):
        values = (self.root_m, self.tip_m, self.span_m, self.thickness_m, self.shear_pa)
        if not all(np.isfinite(v) and v > 0 for v in values) or not np.isfinite(self.sweep_m):
            raise ValueError("Geometría y módulo de corte deben ser finitos y positivos")
        if self.epsilon <= 0:
            raise ValueError("Esta aproximación exige epsilon > 0")

    @property
    def area_m2(self):
        return (self.root_m + self.tip_m) * self.span_m / 2

    @property
    def epsilon(self):
        r, t, s = self.root_m, self.tip_m, self.sweep_m
        centroid = (r*r + r*t + t*t + s*(r+2*t)) / (3*(r+t))
        return centroid / r - 0.25


def flutter_speed(fin, pressure_pa, sound_speed_m_s):
    p, a = np.broadcast_arrays(np.asarray(pressure_pa, float), np.asarray(sound_speed_m_s, float))
    if not np.all(np.isfinite(p)) or not np.all(np.isfinite(a)) or np.any(p <= 0) or np.any(a <= 0):
        raise ValueError("Presión y velocidad del sonido deben ser positivas y finitas")
    ar = fin.span_m**2 / fin.area_m2
    taper = fin.tip_m / fin.root_m
    dn_over_p0 = 24 * fin.epsilon * 1.4 / np.pi
    return a * np.sqrt(fin.shear_pa * (ar+2) * (fin.thickness_m/fin.root_m)**3
                       / (dn_over_p0 * p * ar**3 * (taper+1)/2))
