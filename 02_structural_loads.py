"""
Paso 2: correr el módulo de cargas estructurales sobre el cohete de ejemplo
(Calisto) para verificar que el pipeline completo funciona antes de meterle
los datos reales del cohete.
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import structural_loads as sl
from simulation import NOSE, TAIL, build_flight

flight = build_flight()
calisto = flight.rocket

# ---------------------------------------------------------------------------
# Geometría/material PLACEHOLDER — ver docstring de structural_loads.py.
# Calisto tiene radio 127/2000 = 0.0635 m. Se asume una pared de aluminio de
# 1.5 mm de espesor solo para poder correr el ejemplo end-to-end.
# ---------------------------------------------------------------------------
section = sl.TubeSection(outer_radius=calisto.radius, thickness=1.5e-3)

# Longitud del dominio: de la punta de la nariz a la estación del motor.
# Los extremos se especifican aparte de los centros de presión.
# La distribución interna de masas es equivalente, no medida.
surface_stations = sl.get_surface_stations(calisto)
nose_tip = NOSE  # punta geométrica, no centro de presión
# El dominio del ejemplo tiene la nariz en 1.278 y la cola en -1.255.
# Se usa una sección tubular equivalente, no la geometría interna real.
# PLACEHOLDER: reemplazar por la longitud real del cohete cuando se defina.
rocket_length = NOSE - TAIL

print(f"Longitud del cohete (placeholder): {rocket_length:.3f} m")
print(f"Área sección transversal: {section.area * 1e4:.2f} cm^2")
print(f"I (segundo momento de área): {section.second_moment_of_area:.3e} m^4")
print()

critical, all_results = sl.find_critical_time(flight, surface_stations, rocket_length, section)

print("=== DEMO: máximo esfuerzo del ascenso libre, no de toda la misión ===")
print("Se excluyen riel, recuperación, pandeo y uniones. No usar como certificación.")
assert np.linalg.norm(critical['diagram']['residual_force']) < 1e-7
assert np.linalg.norm(critical['diagram']['residual_moment']) < 1e-7
print(f"t = {critical['t']:.3f} s")
print(f"Momento flector máximo: {critical['max_moment']:.2f} N·m en estación {critical['max_moment_station']:.3f} m")
print(f"Carga axial: {critical['axial_force']:.2f} N")
print(f"Esfuerzo combinado: {critical['combined_stress']/1e6:.2f} MPa")
print(f"Esfuerzo de fluencia del material (placeholder): {section.yield_strength/1e6:.1f} MPa")
print(f"Razón fluencia supuesta / esfuerzo (NO factor de seguridad global): {section.yield_strength / critical['combined_stress']:.2f}")
print(f"Cortante residual en cola (debería ser ~0, chequeo de consistencia): {critical['diagram']['residual_shear_at_tail']:.4f} N")
print()
print(f"Para comparar: Max-Q ocurre en t={flight.max_dynamic_pressure_time:.3f} s")
print(f"¿El instante crítico coincide con Max-Q? {'sí' if abs(critical['t'] - flight.max_dynamic_pressure_time) < 0.05 else 'NO — vale la pena investigar por qué'}")

# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
times = [r["t"] for r in all_results]
combined_stresses = [r["combined_stress"] / 1e6 for r in all_results]
moments = [r["max_moment"] for r in all_results]

fig, axes = plt.subplots(3, 1, figsize=(8, 10), sharex=False)
axes[0].set_xlabel("Tiempo [s]")
axes[1].set_xlabel("Tiempo [s]")

axes[0].plot(times, combined_stresses)
axes[0].axvline(critical["t"], color="r", linestyle="--", label="instante crítico")
axes[0].axvline(flight.max_dynamic_pressure_time, color="g", linestyle=":", label="Max-Q")
axes[0].set_ylabel("Esfuerzo combinado (MPa)")
axes[0].legend()
axes[0].set_title("Esfuerzo combinado vs tiempo")

axes[1].plot(times, moments)
axes[1].set_ylabel("Momento flector máximo (N·m)")

axes[2].plot(critical["diagram"]["stations"], critical["diagram"]["moment"])
axes[2].set_xlabel("Estación a lo largo del cuerpo [m], +z hacia la nariz")
axes[2].set_ylabel("Momento flector en\ninstante crítico (N·m)")
axes[2].set_title(f"Diagrama de momento flector en t={critical['t']:.2f}s")

plt.tight_layout()
output = Path(__file__).resolve().parent / "structural_loads_calisto.png"
plt.savefig(output, dpi=120)
plt.close(fig)
print(f"\nGráficos guardados en {output}")
