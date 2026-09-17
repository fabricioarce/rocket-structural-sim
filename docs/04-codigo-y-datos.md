# 04 · Código y datos: seguir una cifra hasta su origen

[Índice](../README.md) · [Anterior: programación](03-programacion-desde-cero.md) ·
[Siguiente: gráficas](05-graficas-explicadas.md)

## 1. Mapa del flujo

```text
demo.json
   ↓
run_demo.py → build_flight(Design)
   ↓
RocketPy: trayectoria, aire, altitud, presión, sonido, Mach, estabilidad
   ↓
study.evaluate_case → flutter_history + required_thickness
   ↓
report.py → siete PNG + index.html
```

## 2. Archivos principales

| Archivo | Responsabilidad |
|---|---|
| `simulation.py` | Construye ambiente, motor, cohete y vuelo; lleva masa seca agregada |
| `flutter.py` | Define `Fin`, `flutter_speed`, `required_thickness` y `flutter_history` |
| `materials.py` | Datos típicos de cinco materiales y `get_material` |
| `study.py` | Muestreo, resúmenes, barridos, límites y selección |
| `report.py` | Genera las siete figuras |
| `run_demo.py` | Pruebas, 18 casos, sensibilidad, exportación e informe |
| `verify_outputs.py` | Revisa CSV, selección, barridos e imágenes |
| `verify_report.cjs` | Revisa la lógica offline del HTML |
| `verify_docs.py` | Revisa enlaces, ejemplos y cifras documentadas |
| `demo.json` | Configuración de referencia |

La versión completa anterior está en la rama archivada permanente; esta rama
solo conserva el flujo de vuelo y flutter.

## 3. Tres objetos de configuración

### `Design`

```text
payload_kg, fin_scale, fin_thickness_m, fin_density_kg_m3,
fin_shear_pa, wind_m_s, drag_factor, payload_station_m
```

La masa seca base es 14.426 kg. `fin_mass` calcula cuatro aletas homogéneas;
`dry_properties` retira las aletas base, añade las nuevas y suma la carga útil
como masas puntuales. RocketPy recibe la masa, CG e inercias resultantes.

### `Limits`

```text
flutter_ratio=1.25
stability_cal=1.0
rail_speed_m_s=20
loaded_aoa_deg=10
mach=1.5
```

No hay un límite de material en este estudio. Estos criterios son reglas de
cribado para comparar casos.

### `demo.json`

Sus claves son exactamente `base`, `limits`, `payloads_kg`, `fin_scales`,
`winds_m_s`, `samples`, `thickness_sweep_mm` y `materials`. La configuración
base usa 3 mm, aluminio 6061, viento de 4 m/s y `payload_station_m=0.45`.

## 4. Funciones y ecuaciones

| Función | Qué calcula |
|---|---|
| `Fin.aspect_ratio` | \(\mathrm{AR}=b^2/S\) |
| `Fin.taper` | \(\lambda=c_t/c_r\) |
| `flutter_speed` | \(V_f\) de Bennett con \(G,p,a_s\) y geometría |
| `required_thickness` | Inversa de \(V_f\) para una velocidad objetivo |
| `flutter_history` | \(V_f\), ratio y `argmin` temporal |
| `_time_grid` | linspace más Max-Q, máxima velocidad y burnout |
| `evaluate_case` | Trajectory de RocketPy más historia y resumen |
| `thickness_sweep` | Comparación algebraica de espesores |
| `material_sweep` | Comparación algebraica de materiales |
| `select_best` | Mejor apogeo mínimo entre escenarios |

Los dos barridos algebraicos reutilizan la trayectoria y **ignoran el cambio de
masa de la aleta**. El caso delgado de la referencia se resimula aparte.

## 5. Salidas

`results.json` contiene configuración, versiones, `baseline`, `thin_fin`,
`cases`, `best_sampled_design`, `convergence`, `checks`, `thickness_sweep`,
`thickness_sweep_materials`, `material_sweep`,
`thin_algebraic_min_ratio` y `thin_algebraic_relative_difference`.

También se escriben:

| Salida | Contenido |
|---|---|
| `effective-config.json` | Configuración realmente usada |
| `cases.csv` | Una fila por cada uno de 18 casos |
| `case-XXX.csv` | Historia de cada caso |
| `baseline.csv` | Historia base, 184 muestras |
| `thin-fin.csv` | Historia re-simulada con 1.2 mm |
| `thickness-sweep.csv` | Ratio frente a espesor, por material |
| `material-sweep.csv` | Ratio y espesor requerido por material |
| `tests.txt` | Salida del gate de unittest |
| `index.html` | Informe offline e inspector |

Las columnas de historia incluyen `time_s`, altitudes, velocidades, `q_pa`,
ángulo de ataque, Mach, estabilidad, densidad, presión, sonido,
`flutter_speed_m_s` y `flutter_ratio`.

## 6. Del dato al párrafo

Para redactar «el caso base tiene ratio mínimo 2.038»:

1. Abre `outputs/results.json`.
2. Lee `baseline.min_flutter_ratio`.
3. Comprueba que el viento base es 4 m/s en `config.base`.
4. Escribe «la trayectoria simulada produce…».
5. No lo conviertas en una propiedad garantizada del cohete.

La misma trazabilidad produce «el espesor requerido de G10 es 4.00 mm» desde
`material_sweep`, con objetivo 1.25 y la trayectoria base.
