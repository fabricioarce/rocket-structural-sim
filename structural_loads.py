"""Cargas preliminares de una viga libre, en SI y con +z hacia la nariz.

El equilibrio instantáneo incluye alivio inercial traslacional y angular en
los dos planos de flexión. La distribución equivalente de masas es una entrada,
no se deduce de las fuerzas aerodinámicas. La gravedad uniforme se cancela con
su aceleración de caída libre; no equivale a una compresión adicional m*g.

No es un solver aeroelástico: no incluye modos flexibles, torsión, términos
giroscópicos/centrífugos, flujo de momento del propelente, uniones, pandeo ni
recuperación. La reconstrucción cuasiestática no reproduce toda la dinámica de
masa variable de RocketPy. Las cargas internas dependen del camino de carga
supuesto, especialmente de dónde se aplica el arrastre y el empuje.

Los valores numéricos de material por defecto son supuestos de demostración,
no propiedades verificadas de Calisto. No usar como autorización de vuelo.
"""

from dataclasses import dataclass

import numpy as np
from rocketpy.mathutils import Matrix, Vector


# ---------------------------------------------------------------------------
# Geometría y material del fuselaje — PLACEHOLDER, reemplazar con datos reales
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class TubeSection:
    outer_radius: float  # m
    thickness: float  # m
    # Propiedades efectivas supuestas para la demostración, no certificadas.
    # No se conoce el material ni el espesor real del fuselaje de Calisto.
    # Cambiar estos valores no cambia por sí solo la masa del modelo de vuelo.
    youngs_modulus: float = 68.9e9  # Pa
    shear_modulus: float = 26.0e9  # Pa
    yield_strength: float = 276e6  # Pa

    def __post_init__(self):
        values = (self.outer_radius, self.thickness, self.youngs_modulus,
                  self.shear_modulus, self.yield_strength)
        if not np.all(np.isfinite(values)) or min(values) <= 0:
            raise ValueError("Geometría y propiedades deben ser finitas y positivas")
        if self.thickness >= self.outer_radius:
            raise ValueError("El espesor debe ser menor que el radio exterior")

    @property
    def inner_radius(self):
        return self.outer_radius - self.thickness

    @property
    def area(self):
        return np.pi * (self.outer_radius**2 - self.inner_radius**2)

    @property
    def second_moment_of_area(self):
        return np.pi / 4 * (self.outer_radius**4 - self.inner_radius**4)


# ---------------------------------------------------------------------------
# 1. Cargas aerodinámicas puntuales por superficie
# ---------------------------------------------------------------------------
def get_surface_stations(rocket):
    if rocket._csys != 1:
        raise ValueError("Este adaptador admite únicamente tail_to_nose")
    stations = []
    for surface, position in rocket.aerodynamic_surfaces:
        stations.append({
            "name": type(surface).__name__,
            "station": position.z - surface.cp[2],
            "reference_area": surface.reference_area,
            "clalpha": surface.clalpha,  # Function(mach) -> Cl_alpha
            "surface": surface,
        })
    return stations


def get_point_loads(flight, t, surface_stations):
    """Fuerzas por superficie con flujo local, orientación y velocidad angular.

    Usa compute_forces_and_moments de RocketPy 1.13.0, no q*Clalpha*alpha
    global. Conserva ambos componentes transversales y sus signos. Los momentos
    de roll no se transfieren al modelo de viga de esta versión.
    """
    k = Matrix.transformation([flight.e0(t), flight.e1(t), flight.e2(t), flight.e3(t)])
    kt = k.transpose
    velocity = kt @ Vector([flight.vx(t), flight.vy(t), flight.vz(t)])
    omega = Vector([flight.w1(t), flight.w2(t), flight.w3(t)])
    z = flight.z(t)
    rho = flight.env.density(z)
    sound = flight.env.speed_of_sound(z)
    loads = []
    for item in surface_stations:
        surface = item["surface"]
        cp = flight.rocket.surfaces_cp_to_cdm[surface]
        altitude = z + (k @ cp).z
        wind = kt @ Vector([flight.env.wind_velocity_x(altitude),
                            flight.env.wind_velocity_y(altitude), 0])
        stream = wind - velocity - (omega ^ cp)
        speed = abs(stream)
        reynolds = (flight.env.density(altitude) * speed * surface.reference_length
                    / flight.env.dynamic_viscosity(altitude))
        force = surface.compute_forces_and_moments(
            stream, speed, speed / sound, rho, cp, omega, reynolds
        )[:3] if speed > 1e-9 else (0, 0, 0)
        loads.append({"name": item["name"], "station": item["station"],
                      "force": np.asarray(force, dtype=float)})
    return loads


# ---------------------------------------------------------------------------
# 2. Diagrama de cortante y momento flector (con alivio inercial)
# ---------------------------------------------------------------------------
def mass_per_length_uniform(total_mass, rocket_length):
    if min(total_mass, rocket_length) <= 0:
        raise ValueError("Masa y longitud deben ser positivas")
    return total_mass / rocket_length


def section_loads(force_positions, forces, mass_positions, masses, stations):
    """Resultantes en cortes de una viga libre con masas puntuales equivalentes.

    forces tiene forma (n,3), en ejes de cuerpo. La inercia transversal es
    sum(m*(z-z_cg)**2). La aceleración angular de alivio es M_cg/I, no una
    aceleración leída de Flight. axial > 0 denota compresión. Se integran
    exactamente las fuerzas puntuales: no se acumulan con pasos de Euler.
    """
    fp, mp, m, x = (np.asarray(v, dtype=float) for v in
                    (force_positions, mass_positions, masses, stations))
    f = np.asarray(forces, dtype=float)
    if (fp.ndim != 1 or mp.ndim != 1 or m.shape != mp.shape or x.ndim != 1
            or f.shape != (len(fp), 3) or len(m) < 2 or len(x) < 2):
        raise ValueError("Formas incompatibles para fuerzas, masas o cortes")
    if not all(np.all(np.isfinite(v)) for v in (fp, mp, m, x, f)) or np.any(m <= 0):
        raise ValueError("Datos no finitos o masas no positivas")
    if min(fp.min(), mp.min()) < x.min() or max(fp.max(), mp.max()) > x.max():
        raise ValueError("Todas las masas y fuerzas deben quedar dentro de los extremos")
    cg = np.dot(m, mp) / m.sum()
    inertia = np.dot(m, (mp - cg)**2)
    if inertia <= 1e-12:
        raise ValueError("Se necesita inercia transversal positiva")
    acceleration = f.sum(axis=0) / m.sum()  # aceleración específica sin gravedad
    lever = np.column_stack((np.zeros(len(fp)), np.zeros(len(fp)), fp - cg))
    torque = np.cross(lever, f).sum(axis=0)
    angular_acceleration = torque / inertia
    mass_lever = np.column_stack((np.zeros(len(mp)), np.zeros(len(mp)), mp - cg))
    inertial = -m[:, None] * (acceleration + np.cross(angular_acceleration, mass_lever))
    positions = np.concatenate((fp, mp))
    effective = np.concatenate((f, inertial))
    distance = positions[None, :] - x[:, None]  # distancia del punto al corte
    # Cada fuerza actúa una sola vez; se considera el lado de la nariz.
    # En una discontinuidad se evalúan los límites izquierdo y derecho.
    ahead = distance > 0
    resultant = ahead.astype(float) @ effective
    # La integración de cada fuerza puntual usa su brazo exacto al corte.
    bending = (np.where(ahead, distance, 0)) @ effective[:, :2]
    moments = np.column_stack((-bending[:, 1], bending[:, 0]))
    residual_force = effective.sum(axis=0)
    residual_moment = np.cross(
        np.column_stack((np.zeros(len(positions)), np.zeros(len(positions)), positions - cg)),
        effective,
    ).sum(axis=0)
    return {
        "stations": x, "shear_components": resultant[:, :2],
        "shear": np.linalg.norm(resultant[:, :2], axis=1),
        "moment_components": moments, "moment": np.linalg.norm(moments, axis=1),
        "axial": -resultant[:, 2], "center_of_mass": cg,
        "acceleration": acceleration, "angular_acceleration": angular_acceleration,
        "residual_force": residual_force, "residual_moment": residual_moment,
        "residual_shear_at_tail": float(np.linalg.norm(residual_force[:2])),  # cierre global
    }


def shear_and_moment_diagram(point_loads, total_mass, rocket_length, n_stations=200):
    """Caso didáctico legado: masa uniforme equivalente, no geometría de Calisto.

    El extremo delantero se toma de las cargas solo para compatibilidad con
    esta función de juguete. El análisis de vuelo exige extremos explícitos.
    """
    if not point_loads or n_stations < 2:
        raise ValueError("Se requieren cargas y al menos dos cortes")
    mass_per_length_uniform(total_mass, rocket_length)
    nose = max(p["station"] for p in point_loads)
    tail = nose - rocket_length
    nodes, weights = np.polynomial.legendre.leggauss(32)
    mp = (nose + tail) / 2 + nodes * rocket_length / 2
    x = np.linspace(nose + 1e-8, tail - 1e-8, n_stations)
    return section_loads([p["station"] for p in point_loads],
                         [[p["force"], 0, 0] for p in point_loads],
                         mp, weights * total_mass / 2, x)


# ---------------------------------------------------------------------------
# 3. Esfuerzo combinado (flexión + axial) y comparación con el material
# ---------------------------------------------------------------------------
def axial_force(flight, t):
    raise NotImplementedError("La carga axial es N(z,t), no empuje-arrastre-peso. Use analyze_time_step.")


def combined_stress(moment, axial_load, section):
    return (np.abs(axial_load) / section.area
            + np.abs(moment) * section.outer_radius / section.second_moment_of_area)


def analyze_time_step(flight, t, surface_stations, rocket_length, section):
    if not flight.out_of_rail_time < t <= flight.apogee_time:
        raise ValueError("Cargas disponibles solo en ascenso libre, después del riel")
    if not hasattr(flight, "structural_mass_model"):
        raise ValueError("Falta una distribución de masas y extremos explícitos; use simulation.build_flight")
    points = get_point_loads(flight, t, surface_stations)
    z = flight.z(t)
    motor = flight.rocket.motor
    burning = motor.burn_start_time < t < motor.burn_out_time
    thrust = max(motor.thrust(t) + motor.pressure_thrust(flight.env.pressure(z)), 0) if burning else 0
    drag = float(flight.R3(t))  # R3 incluye drag en el eje axial del cuerpo
    points += [{"name": "Empuje equivalente", "station": flight.structural_bounds[0],
                "force": np.array([0., 0., thrust])},
               {"name": "Arrastre concentrado supuesto", "station": flight.drag_station,
                "force": np.array([0., 0., drag])}]
    mp, masses = flight.structural_mass_model(t)
    tail, nose = flight.structural_bounds
    events = np.r_[mp, [p["station"] for p in points]]
    if events.min() < tail or events.max() > nose:
        raise ValueError("Masas o cargas fuera de los extremos físicos declarados")
    stations = np.unique(np.r_[np.linspace(tail - 1e-8, nose + 1e-8, 101),
                              events - 1e-8, events + 1e-8])
    diagram = section_loads([p["station"] for p in points],
                            [p["force"] for p in points], mp, masses, stations)
    stress = combined_stress(diagram["moment"], diagram["axial"], section)
    idx = int(np.argmax(stress))
    return {
        "t": float(t), "max_moment": float(np.max(diagram["moment"])),
        "max_moment_station": float(stations[np.argmax(diagram["moment"])]),
        "critical_station": float(stations[idx]), "axial_force": float(diagram["axial"][idx]),
        "combined_stress": float(stress[idx]), "stress": stress,
        "diagram": diagram, "point_loads": points,
    }


def find_critical_time(flight, surface_stations, rocket_length, section, t_end=None, n_samples=180):
    if n_samples < 3:
        raise ValueError("Se requieren al menos tres muestras")
    start = flight.out_of_rail_time + 1e-5
    end = flight.apogee_time if t_end is None else float(t_end)
    if not start < end <= flight.apogee_time:
        raise ValueError("Intervalo de tiempo fuera del ascenso libre")
    special = [flight.max_dynamic_pressure_time, flight.max_speed_time,
               flight.rocket.motor.burn_out_time - 1e-5,
               flight.rocket.motor.burn_out_time + 1e-5]
    thrust_nodes = flight.rocket.motor.thrust.source[:, 0]
    solver_nodes = np.asarray(flight.solution)[:, 0]
    times = np.unique(np.r_[np.linspace(start, end, n_samples), special, thrust_nodes, solver_nodes])
    times = times[(times >= start) & (times <= end)]
    results = [analyze_time_step(flight, t, surface_stations, rocket_length, section) for t in times]
    critical = max(results, key=lambda r: r["combined_stress"])
    return critical, results
