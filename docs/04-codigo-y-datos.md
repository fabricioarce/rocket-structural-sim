# 04 · Mapa del código, ecuaciones y datos

[Índice](../README.md) · [Anterior: programación](03-programacion-desde-cero.md) · [Siguiente: gráficas](05-graficas-explicadas.md)

Este capítulo describe **el código existente**, no una arquitectura futura. Usa los nombres de función para localizar una implementación: los números de línea pueden cambiar.

## 1. Recorrido completo

```text
demo.json
   │
   ▼
run_demo.load_config → Design + TubeSection + Limits
   │
   ├── unittest: pruebas antes de generar resultados
   │
   ▼
study.grid_designs → combinación de carga útil, aletas y viento
   │
   ▼
study.evaluate_case
   ├── simulation.build_flight → Environment, SolidMotor, Rocket, Flight
   ├── structural_loads.find_critical_time
   │      └── analyze_time_step
   │             ├── get_point_loads: fuerzas locales de RocketPy
   │             ├── distribución de masas + empuje y arrastre supuestos
   │             ├── section_loads: alivio inercial y cortes
   │             └── combined_stress: esfuerzo por sección
   └── flutter.flutter_speed → Vf(t) y margen Vf/Vrel
   │
   ▼
rejection_reasons + select_best → cribado y selección discreta
   │
   ▼
CSV + JSON + report.generate_report → PNG + HTML
```

«Cribado» significa filtrar usando criterios concretos. No equivale a una certificación estructural.

## 2. Qué hace cada archivo

| Archivo | Responsabilidad | Lo que no hace |
|---|---|---|
| [01_learn_api.py](../01_learn_api.py) | Ejemplo introductorio de API, sin viento | No es la ejecución estructural de referencia con viento de 4 m/s |
| [02_structural_loads.py](../02_structural_loads.py) | Ejemplo directo de las cargas del caso base; imagen auxiliar | No genera los 18 casos ni todo el informe |
| [simulation.py](../simulation.py) | Construye geometría, masas equivalentes, ambiente, motor y vuelo | No identifica la estructura interna real |
| [structural_loads.py](../structural_loads.py) | Cargas y esfuerzo longitudinal por corte | No calcula modos, pandeo, torsión o uniones |
| [flutter.py](../flutter.py) | Frontera empírica para aletas trapezoidales | No calcula una oscilación temporal de la aleta |
| [study.py](../study.py) | Métricas, escenarios, límites y selección | No encuentra un óptimo global continuo |
| [run_demo.py](../run_demo.py) | Coordina ejecución, pruebas, exportaciones y refinamiento | No es por sí solo el modelo físico |
| [report.py](../report.py) | Dibuja y prepara el informe | No valida las ecuaciones al dibujarlas |
| [report_template.html](../report_template.html) | Texto y controles del informe | Sus controles no ejecutan Python |
| [requirements.txt](../requirements.txt) | Versiones del entorno de cálculo publicado | No describe el hardware real del cohete |
| `test_*.py` | Pruebas automáticas de casos concretos | No son mediciones de vuelos |
| [verify_outputs.py](../verify_outputs.py) | Coherencia de CSV, extremos, selección e imágenes | No prueba todos los supuestos estructurales |
| [verify_report.cjs](../verify_report.cjs) | Lógica DOM de filtros y curvas mediante Node.js | No es una prueba visual completa en un navegador |
| [verify_docs.py](../verify_docs.py) | Enlaces locales, sintaxis de ejemplos y evidencia numérica citada | No es una revisión por pares |

## 3. Tres objetos distintos de configuración

### A. `base`: diseño de vuelo y aletas

| Clave | Unidad / ejemplo | Efecto real en el programa |
|---|---|---|
| `payload_kg` | kg, 0 | Masa **adicional** a la referencia; cambia masa, CG e inercia transversal |
| `payload_station_m` | m, 0.45 | Posición axial de esa masa añadida |
| `fin_scale` | Sin unidad, 1 | Multiplica cr, ct, envergadura y barrido; no multiplica espesor |
| `fin_thickness_m` | m, 0.003 | Cambia masa de aletas y frontera de flutter |
| `fin_density_kg_m3` | kg/m³, 2700 | Cambia masa de aletas; no es densidad del aire |
| `fin_shear_pa` | Pa, 26e9 | G efectivo de la aleta en la fórmula de flutter |
| `wind_m_s` | m/s, 4 | Viento constante en el eje horizontal u del ambiente |
| `drag_factor` | Sin unidad, 1 | Multiplica ambas curvas del Cd total, a todos sus puntos |
| `drag_station_m` | m, 0.8 | Dónde se concentra el arrastre total **en el modelo de cargas**, no un CP aerodinámico identificado |

En la clase `Design`, `fin_scale` se restringe a [0.6, 1.3]. La configuración del barrido elige un subconjunto de ese intervalo. No es una validación de todas las geometrías posibles dentro de él.

### B. `section`: comparación de una sección equivalente

| Clave | Unidad / ejemplo | Efecto real |
|---|---|---|
| `outer_radius` | m, 0.0635 | Define A e IA; el cargador exige el radio de Calisto |
| `thickness` | m, 0.0015 | Define radio interior, A e IA y por tanto el esfuerzo |
| `youngs_modulus` | Pa, 68.9e9 | Se almacena; no se usa para calcular deflexión o esfuerzo en esta versión |
| `shear_modulus` | Pa, 26e9 | Se almacena para la sección; no sustituye `base.fin_shear_pa` |
| `yield_strength` | Pa, 276e6 | Comparación auxiliar en el script 02; no impone automáticamente el límite de `select_best` |

**Advertencia importante:** modificar espesor o propiedades del tubo no recalcula automáticamente su masa de vuelo. Es una comparación de sección, no un rediseño físicamente acoplado del fuselaje. Cambiar solo E puede no cambiar ninguna de las siete gráficas; eso responde a qué está implementado, no a que la rigidez carezca de importancia física.

No existe un factor de seguridad global validado. La razón «fluencia supuesta / esfuerzo normal» del script 02 omite mecanismos de fallo y no debe renombrarse como seguridad global.

### C. `limits`: reglas de selección

| Clave | Unidad | Regla de aceptación |
|---|---|---|
| `stress_mpa` | **MPa**, no Pa | Máximo esfuerzo longitudinal ≤ límite |
| `flutter_ratio` | Sin unidad | Mínimo Vf/Vrel ≥ límite |
| `stability_cal` | Calibres | Mínimo margen estático ≥ límite |
| `rail_speed_m_s` | m/s | Velocidad de salida del riel ≥ límite |
| `loaded_aoa_deg` | Grados | Máximo α en las muestras con q ≥ 500 Pa ≤ límite |
| `mach` | Sin unidad | Máximo Mach muestreado ≤ límite |

La regla q ≥ 500 Pa para revisar α está fijada en `study.py`, no es un campo de `demo.json`. Las cargas no se eliminan por debajo de ese umbral: este solo selecciona las muestras del criterio de ángulo.

Estas reglas son criterios de estudio. Aumentarlas hasta que un diseño «pase» no demuestra que el diseño se haya vuelto físicamente seguro.

### Listas y resolución

| Clave | Valor de referencia | Interpretación |
|---|---|---|
| `payloads_kg` | [0, 3, 6] | Cargas útiles añadidas para el barrido |
| `fin_scales` | [0.85, 1, 1.15] | Escalas del plano de la aleta |
| `winds_m_s` | [0, 4] | Escenarios constantes, no muestras aleatorias |
| `samples` | 180 | Muestras uniformes solicitadas, a las que se añaden otras |
| `mass_nodes` | 32 | Nodos por grupo equivalente, no número total de piezas |

Hay `3 × 3 = 9` diseños geométrico-másicos, evaluados en `2` vientos: 18 casos. El caso base también debe tener su viento dentro de la lista de escenarios. El cargador rechaza listas duplicadas o vacías y limita la demo a 100 casos por barrido.

## 4. Relación entre funciones y ecuaciones

### Geometría y masa

`Design.fin_mass` usa cuatro aletas homogéneas: `4 × S × espesor × densidad`. Si solo el plano de la aleta se escala por k, su masa escala por k², manteniendo espesor y densidad.

`dry_mass_nodes` resta las contribuciones supuestas de las aletas de referencia para mantener una parte seca residual común, y añade las aletas del diseño y la carga útil. De esta forma no se añade dos veces la masa base de aletas.

`equivalent_nodes` y `bounded_equivalent_nodes` reconstruyen momentos agregados. La distribución beta del motor está acotada; los nodos no deben aparecer fuera del cohete. La inercia polar se actualiza mediante una aproximación de masa de aletas a un radio representativo; no se identifica un tensor completo de cada componente físico.

### Flujo local y fuerzas

`get_surface_stations` obtiene las estaciones de aplicación según la convención axial de RocketPy. El adaptador utiliza también atributos internos como `_csys` y `surfaces_cp_to_cdm`; por eso se fija la versión y se requieren pruebas si RocketPy cambia.

`get_point_loads` transforma velocidades a ejes del cuerpo e incorpora el movimiento local por rotación. Llama a `surface.compute_forces_and_moments`. Conserva las fuerzas con signo. Los momentos de roll devueltos por la superficie no se transmiten a este modelo de viga.

### Cargas internas

`section_loads` suma fuerzas y momentos externos, calcula alivio traslacional y angular con las masas equivalentes y evalúa los cortes. La carga axial es positiva en compresión. Las curvas de cortante y momento del informe son **magnitudes** de dos componentes, no diagramas firmados de un único plano.

`analyze_time_step` añade empuje equivalente en la cola y arrastre concentrado. Verifica que todos los puntos queden dentro de los extremos explícitos y evalúa ambos lados de las discontinuidades usando desplazamientos numéricos pequeños.

`combined_stress` combina N y M del **mismo corte**. `find_critical_time` añade muestras del integrador, nodos de empuje y eventos relevantes a la malla temporal solicitada. El resultado es el máximo encontrado en esa discretización, no una prueba analítica del máximo continuo exacto.

### Flutter y selección

`flutter_speed` calcula Vf con presión y velocidad del sonido locales. `evaluate_case` obtiene `flutter_ratio = Vf/Vrel` y resume sus mínimos.

`rejection_reasons` enumera los criterios incumplidos. `select_best` agrupa por masa añadida y escala de aletas y exige todos los escenarios previstos. Ordena por apogeo mínimo de cada grupo y devuelve el primer grupo admisible. Si ninguno pasa, devuelve `None`.

## 5. Qué datos hay en cada salida

| Archivo | Contenido |
|---|---|
| [results.json](../outputs/results.json) | Parámetros, versiones, caso base, aletas delgadas, sensibilidad, casos, ranking, refinamiento y checksums |
| [effective-config.json](../outputs/effective-config.json) | Configuración efectiva usada en la ejecución |
| [cases.csv](../outputs/cases.csv) | Una fila de resumen por caso, con motivos de descarte |
| `case-001.csv` … `case-018.csv` | Historias temporales completas de los casos del barrido de referencia |
| [baseline.csv](../outputs/baseline.csv) | Historia temporal del caso base, equivalente al case-004 de esta configuración |
| [thin-fin.csv](../outputs/thin-fin.csv) | Historia del vuelo con espesor de aleta multiplicado por 0.4 |
| [critical-diagram.csv](../outputs/critical-diagram.csv) | Cortes de N, V, M y esfuerzo en el instante crítico del caso base |
| `01-flight.png` … `07-drag-sensitivity.png` | Figuras estáticas |
| [index.html](../outputs/index.html) | Informe con gráficas y subconjunto de curvas incrustado para interacción |
| [tests.txt](../outputs/tests.txt) | Salida de las pruebas ejecutadas al generar la referencia |

Los CSV numéricos usan punto decimal y coma separadora. Si una hoja de cálculo en español los interpreta mal, especifica esos separadores al importar. En `cases.csv`, `True` y `False` son texto exportado de booleanos; en JSON son `true` y `false`.

### Columnas de una historia temporal

| Columna | Significado | Unidad |
|---|---|---|
| `time_s` | Tiempo desde ignición | s |
| `altitude_agl_m` | Altura sobre el lanzamiento | m |
| `altitude_asl_m` | Altitud sobre el mar | m |
| `airspeed_m_s` | Rapidez relativa al aire | m/s |
| `speed_m_s` | Rapidez respecto al suelo | m/s |
| `q_pa` | Presión dinámica | Pa |
| `aoa_deg` | Ángulo de ataque global de Flight | Grados |
| `mach` | Rapidez relativa / velocidad local del sonido | Sin unidad |
| `stability_cal` | Margen estático con dependencia de Mach | Calibres |
| `density_kg_m3` | Densidad local del aire | kg/m³ |
| `pressure_pa` | Presión atmosférica estática local | Pa |
| `stress_mpa` | Mayor esfuerzo longitudinal entre cortes a ese instante | MPa |
| `max_moment_nm` | Mayor magnitud del momento entre cortes a ese instante | N·m |
| `max_axial_n` | Máxima compresión axial entre cortes a ese instante | N |
| `flutter_speed_m_s` | Frontera nominal Vf | m/s |
| `flutter_ratio` | Vf / rapidez relativa | Sin unidad |

`max_axial_n` no es el máximo valor absoluto de N: una región en tracción puede no dominar esa métrica. El esfuerzo combinado sí utiliza `abs(N)`.

### Resúmenes que requieren cuidado

- `critical_time_s` y `critical_station_m`: instante y sección del mayor esfuerzo longitudinal modelado.
- `max_moment_nm` del resumen: máximo de momento durante todo el intervalo; puede ocurrir en **otro instante**.
- `flutter_time_s`: instante de menor margen, no instante de desprendimiento.
- `max_speed_m_s`: propiedad de Flight; `max_airspeed_m_s`: máximo de las muestras del análisis. No son idéntica definición ni necesariamente idéntica discretización.
- `samples`: cantidad real de muestras, no el 180 de entrada. El caso base de referencia tiene 1345 filas de historia.
- `force_residual_n` y `moment_residual_nm`: residuos de equilibrio, no errores respecto a un ensayo.
- `refinement_below_5_percent`: pasa un chequeo de resolución, no significa error físico menor al 5%.

## 6. Qué se conserva y qué no se conserva

Las curvas completas del barrido, base y aleta delgada se exportan. Para la sensibilidad al Cd, se guardan resúmenes y figuras, pero no CSV dedicados de esas dos historias. Para volver a analizarlas punto a punto hay que ejecutar `evaluate_case` con esos factores o añadir una exportación explícita.

El mapa de calor se interpola a 101 estaciones para representación visual y no se exporta como un CSV completo espacio–tiempo. `critical-diagram.csv` contiene **un instante**, no toda la película. La imagen no permite recuperar exactamente todos los valores originales.

El inspector HTML usa hasta 240 muestras por caso y redondea sus números para visualización. No debes leer el máximo preciso del inspector si existe el resumen numérico completo.

## 7. Del dato al párrafo: ejemplo trazable

Para escribir que el caso base alcanza unos 3287 m AGL:

1. Identifica `case-004` en `cases.csv` por sus parámetros, no solo por su número.
2. Lee `apogee_agl_m`; no lo confundas con `apogee_asl_m`.
3. Comprueba los mismos parámetros en `effective-config.json`.
4. Indica «simulado» y «caso base con viento constante de 4 m/s».
5. No añadas una afirmación de precisión experimental que no aparece respaldada.

Si cambian las listas del barrido, `case-004` puede representar otro diseño. Los identificadores son de la ejecución, no nombres universales de vehículos.

**Siguiente paso:** elige una cifra de una figura y encuentra su columna, función de cálculo y parámetro de entrada relacionado. Esa cadena es la base de una explicación defendible.
