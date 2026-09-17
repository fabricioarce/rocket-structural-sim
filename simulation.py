"""Calisto adaptado: geometría de ejemplo, distribución interna equivalente.

La distribución seca se calibra a m=14.426 kg, CG=0 e I11=6.321 kg*m² del
 ejemplo oficial; infinitas distribuciones satisfacen esos tres datos. No es
la distribución real de Calisto. Al variar las aletas se actualizan su masa,
CG, inercia y superficies aerodinámicas. La curva de Cd total sigue siendo la
original: su dependencia de la nueva geometría NO está identificada.
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
from rocketpy import Environment, Flight, Function, Rocket, SolidMotor
from scipy.special import roots_jacobi

DATA = Path(__file__).resolve().parent / "data"
TAIL, NOSE = -1.255, 1.278
RADIUS = 0.0635


@dataclass(frozen=True)
class Design:
    payload_kg: float = 0.0
    fin_scale: float = 1.0
    fin_thickness_m: float = 0.003
    fin_density_kg_m3: float = 2700.0
    fin_shear_pa: float = 26e9
    wind_m_s: float = 4.0
    drag_factor: float = 1.0
    payload_station_m: float = 0.45
    drag_station_m: float = 0.8

    def __post_init__(self):
        if not all(np.isfinite(v) for v in self.__dict__.values()):
            raise ValueError("Todos los parámetros deben ser finitos")
        if self.payload_kg < 0 or self.wind_m_s < 0:
            raise ValueError("Carga útil y viento no pueden ser negativos")
        if not 0.6 <= self.fin_scale <= 1.3:
            raise ValueError("La demo limita la escala de aletas al intervalo [0.6, 1.3]")
        if min(self.fin_thickness_m, self.fin_density_kg_m3, self.fin_shear_pa, self.drag_factor) <= 0:
            raise ValueError("Espesor, densidad, rigidez y multiplicador de Cd deben ser positivos")
        if not all(TAIL < p < NOSE for p in (self.payload_station_m, self.drag_station_m)):
            raise ValueError("Las estaciones deben quedar dentro del cohete")

    @property
    def fin_geometry(self):
        return {"root": 0.12 * self.fin_scale, "tip": 0.06 * self.fin_scale,
                "span": 0.11 * self.fin_scale, "sweep": 0.06 * self.fin_scale}

    @property
    def fin_mass(self):
        g = self.fin_geometry
        return 4 * (g["root"] + g["tip"]) / 2 * g["span"] * self.fin_thickness_m * self.fin_density_kg_m3

    @property
    def fin_station(self):
        g = self.fin_geometry
        centroid = (g["root"]**2 + g["root"]*g["tip"] + g["tip"]**2
                    + g["sweep"]*(g["root"]+2*g["tip"])) / (3*(g["root"]+g["tip"]))
        return -1.04956 - centroid


@lru_cache(maxsize=8)
def quadrature(count):
    return np.polynomial.legendre.leggauss(count)


def equivalent_nodes(mass, center, inertia, count=32):
    """Cuadratura de una barra uniforme que reproduce masa, CG e inercia."""
    if mass <= 0 or inertia <= 0 or count < 2:
        raise ValueError("Masa, inercia y número de nodos inválidos")
    nodes, weights = quadrature(count)
    return center + nodes * np.sqrt(3 * inertia / mass), weights * mass / 2


def bounded_equivalent_nodes(mass, center, inertia, lower, upper, count=32):
    """Distribución beta equivalente, acotada, con los momentos prescritos.

    La longitud de carcasa de 0.757 m procede de la cabecera del archivo .eng.
    Esta distribución matemática no identifica el interior real del motor.
    """
    length = upper-lower
    mean = (center-lower)/length
    variance = inertia/mass/length**2
    if mass <= 0 or not 0 < mean < 1 or not 0 < variance < mean*(1-mean):
        raise ValueError("Los momentos de masa no caben dentro de los límites indicados")
    concentration = mean*(1-mean)/variance - 1
    alpha, beta = mean*concentration, (1-mean)*concentration
    nodes, weights = roots_jacobi(count, beta-1, alpha-1)
    return lower + (nodes+1)*length/2, weights/weights.sum()*mass


def dry_mass_nodes(design, count=32):
    baseline = Design()
    residual_mass = 14.426 - baseline.fin_mass
    center = -baseline.fin_mass * baseline.fin_station / residual_mass
    inertia = 6.321 - baseline.fin_mass * baseline.fin_station**2 - residual_mass * center**2
    positions, masses = equivalent_nodes(residual_mass, center, inertia, count)
    positions = np.r_[positions, design.fin_station]
    masses = np.r_[masses, design.fin_mass]
    if design.payload_kg > 0:
        positions = np.r_[positions, design.payload_station_m]
        masses = np.r_[masses, design.payload_kg]
    return positions, masses


def build_flight(design=Design(), mass_nodes=32, max_time_step=0.12):
    env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)
    env.set_date((2026, 9, 15, 12))
    env.set_atmospheric_model(type="custom_atmosphere", wind_u=design.wind_m_s, wind_v=0)
    motor = SolidMotor(
        thrust_source=str(DATA / "motors/cesaroni/Cesaroni_M1670.eng"),
        dry_mass=1.815, dry_inertia=(0.125, 0.125, 0.002),
        nozzle_radius=0.033, grain_number=5, grain_density=1815,
        grain_outer_radius=0.033, grain_initial_inner_radius=0.015,
        grain_initial_height=0.120, grain_separation=0.005,
        grains_center_of_mass_position=0.397, center_of_dry_mass_position=0.317,
        nozzle_position=0, burn_time=3.9, throat_radius=0.011,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )
    positions, masses = dry_mass_nodes(design, mass_nodes)
    center = np.dot(positions, masses) / masses.sum()
    i11 = np.dot(masses, (positions - center)**2)
    baseline = Design()
    i33 = (0.034 - baseline.fin_mass * (RADIUS + 0.11/2)**2
           + design.fin_mass * (RADIUS + design.fin_geometry["span"]/2)**2)
    off = np.loadtxt(DATA / "rockets/calisto/powerOffDragCurve.csv", delimiter=",")
    on = np.loadtxt(DATA / "rockets/calisto/powerOnDragCurve.csv", delimiter=",")
    off[:, 1] *= design.drag_factor
    on[:, 1] *= design.drag_factor
    rocket = Rocket(radius=RADIUS, mass=float(masses.sum()), inertia=(i11, i11, i33),
                    power_off_drag=Function(off), power_on_drag=Function(on), center_of_mass_without_motor=center,
                    coordinate_system_orientation="tail_to_nose")
    rocket.add_motor(motor, position=TAIL)
    rocket.set_rail_buttons(upper_button_position=0.0818, lower_button_position=-0.6182, angular_position=45)
    rocket.add_nose(length=0.55829, kind="von karman", position=NOSE)
    g = design.fin_geometry
    rocket.add_trapezoidal_fins(n=4, root_chord=g["root"], tip_chord=g["tip"], span=g["span"],
                               sweep_length=g["sweep"], position=-1.04956, cant_angle=0.5,
                               airfoil=(str(DATA / "airfoils/NACA0012-radians.txt"), "radians"))
    rocket.add_tail(top_radius=RADIUS, bottom_radius=0.0435, length=0.060, position=-1.194656)
    flight = Flight(rocket=rocket, environment=env, rail_length=5.2, inclination=85,
                    heading=0, terminate_on_apogee=True, max_time=120,
                    max_time_step=max_time_step, rtol=1e-7)
    if flight.apogee_time <= flight.out_of_rail_time or flight.out_of_rail_time <= 0:
        raise ValueError("La simulación no completó un ascenso libre hasta el apogeo")

    def mass_model(t):
        motor_positions, motor_masses = bounded_equivalent_nodes(
            motor.total_mass(t), TAIL + motor.center_of_mass(t), motor.I_11(t),
            TAIL, TAIL + 0.757, mass_nodes)
        return np.r_[positions, motor_positions], np.r_[masses, motor_masses]

    flight.structural_mass_model = mass_model
    flight.structural_bounds = (TAIL, NOSE)
    flight.drag_station = design.drag_station_m
    flight.design = design
    return flight
