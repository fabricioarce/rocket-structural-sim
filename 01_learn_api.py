"""
Paso 1: aprender la API de RocketPy usando el cohete de ejemplo "Calisto"
(el mismo que usa la documentación oficial). Una vez entendida la API,
se reemplaza esto por los datos del cohete real.

Las 4 clases centrales de RocketPy:
  - Environment : clima, atmósfera, sitio de lanzamiento
  - SolidMotor  : curva de empuje, quemado de propelente
  - Rocket      : geometría, masa, superficies aerodinámicas (nariz, aletas, cola)
  - Flight      : corre la simulación y guarda resultados (integra las
                  ecuaciones de movimiento con masa/inercia variable)
"""

from pathlib import Path
from rocketpy import Environment, SolidMotor, Rocket, Flight

ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 1. Environment: dónde y cuándo se lanza
# ---------------------------------------------------------------------------
env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)

# Usamos el modelo atmosférico "standard_atmosphere" en vez de forecast (GFS)
# para que esto corra offline y sea reproducible sin depender de internet
# ni de la fecha en que se corre.
env.set_date((2026, 9, 15, 12))
env.set_atmospheric_model(type="standard_atmosphere")

# ---------------------------------------------------------------------------
# 2. Motor: Cesaroni M1670 (motor sólido de ejemplo)
# ---------------------------------------------------------------------------
motor = SolidMotor(
    thrust_source=str(ROOT / "data/motors/cesaroni/Cesaroni_M1670.eng"),
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

# ---------------------------------------------------------------------------
# 3. Rocket: geometría, masa, superficies aerodinámicas
# ---------------------------------------------------------------------------
calisto = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag=str(ROOT / "data/rockets/calisto/powerOffDragCurve.csv"),
    power_on_drag=str(ROOT / "data/rockets/calisto/powerOnDragCurve.csv"),
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

calisto.add_motor(motor, position=-1.255)

calisto.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)

nose_cone = calisto.add_nose(length=0.55829, kind="von karman", position=1.278)

fin_set = calisto.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
    airfoil=(str(ROOT / "data/airfoils/NACA0012-radians.txt"), "radians"),
)

tail = calisto.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

# ---------------------------------------------------------------------------
# 4. Flight: correr la simulación
# ---------------------------------------------------------------------------
flight = Flight(
    rocket=calisto,
    environment=env,
    rail_length=5.2,
    inclination=85,
    heading=0,
    terminate_on_apogee=True,
)

# ---------------------------------------------------------------------------
# Lo que nos interesa para el estudio de flutter:
# Flight expone estas series de tiempo (funciones que se pueden evaluar en
# cualquier instante t, o discretizar con .set_discrete / list comprehension).
# ---------------------------------------------------------------------------
print(f"Apogeo: {flight.apogee - env.elevation:.1f} m AGL / {flight.apogee:.1f} m ASL (t={flight.apogee_time:.2f} s)")
print(f"Velocidad máxima: {flight.max_speed:.1f} m/s (t={flight.max_speed_time:.2f} s)")
print(f"Max-Q: {flight.max_dynamic_pressure:.1f} Pa (t={flight.max_dynamic_pressure_time:.2f} s)")
print(f"Ángulo de ataque en Max-Q: {flight.angle_of_attack(flight.max_dynamic_pressure_time):.2f} deg")
print(f"Velocidad de salida del riel: {flight.out_of_rail_velocity:.1f} m/s")

# Estas son las funciones (rocketpy.Function) que vamos a necesitar en el
# estudio de flutter:
#   flight.speed(t)                  -> velocidad total [m/s]
#   flight.dynamic_pressure(t)       -> presión dinámica q [Pa]
#   flight.angle_of_attack(t)        -> ángulo de ataque [deg]
#   flight.z(t)                      -> altitud [m]
#   flight.env.density(flight.z(t))  -> densidad del aire a esa altitud [kg/m3]
#   flight.env.speed_of_sound(flight.z(t)) -> velocidad del sonido [m/s]
#   motor.thrust(t)                  -> empuje axial [N]
#   calisto.power_on_drag(mach) / power_off_drag(mach) -> Cd
