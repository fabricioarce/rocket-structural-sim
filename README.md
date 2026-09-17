# Estudio de flutter de aletas para un cohete de alta potencia

Proyecto educativo que usa **RocketPy como caja negra de vuelo** y estudia la
frontera empírica de flutter de sus aletas. La documentación empieza
**desde cero**: cada capítulo introduce un concepto, una ecuación o una
decisión del programa antes de usarlo.

> **Estado:** prototipo computacional verificado con pruebas numéricas, no
> validado experimentalmente. No autoriza la fabricación ni el lanzamiento de
> un cohete.

## Qué hace

RocketPy proporciona trayectoria, rapidez relativa al aire, altitud, presión,
velocidad del sonido, Mach y estabilidad. El proyecto calcula con esos datos
la velocidad nominal de flutter \(V_f\), el cociente \(V_f/V\), el espesor
requerido para un margen elegido y barridos de espesor y material.

El caso de referencia usa Calisto, el motor Cesaroni M1670, viento constante
de 4 m/s y el intervalo entre la salida del riel y el apogeo. Hay 18 casos
de la malla de carga útil, escala de aleta y viento; no son ensayos.

## Qué NO hace

El modelo trata aletas trapezoidales homogéneas, de espesor constante y
propiedades efectivas isótropas. No predice amplitud de vibración ni rotura
segura. Tampoco resuelve modos, uniones, laminados, amortiguamiento o
divergencia. Rebasar la frontera señala riesgo según el modelo, no una
rotura segura. El resultado no sustituye ensayos, FEA ni una certificación.

## Rama archivada

La versión completa anterior, con cargas internas, modelo de viga y esfuerzos,
se conserva permanentemente en
[archive/full-structural-sim](https://github.com/fabricioarce/rocket-structural-sim/tree/archive/full-structural-sim).
Esta rama reduce deliberadamente el alcance a flutter de aletas.

## Empieza aquí

| Necesitas… | Lee… |
|---|---|
| Entender el alcance y repartir tareas | [00 · Guía del equipo](docs/00-guia-del-equipo.md) |
| Aprender la física del vuelo | [01 · Física desde cero](docs/01-fisica-desde-cero.md) |
| Entender aeroelasticidad y la fórmula | [02 · Flutter desde cero](docs/02-flutter-desde-cero.md) |
| Leer Python con ejemplos pequeños | [03 · Programación desde cero](docs/03-programacion-desde-cero.md) |
| Seguir archivos, datos y ecuaciones | [04 · Código y datos](docs/04-codigo-y-datos.md) |
| Interpretar las siete figuras | [05 · Gráficas explicadas](docs/05-graficas-explicadas.md) |
| Redactar hipótesis y resultados | [06 · Metodología y redacción](docs/06-metodologia-y-redaccion.md) |
| Reproducir la referencia | [07 · Reproducibilidad](docs/07-reproducibilidad.md) |
| Consultar símbolos y fuentes | [08 · Glosario y referencias](docs/08-glosario-y-referencias.md) |

Ruta sugerida: **00 → 01 → 02 → 05 → 06**. Consulta 03 y 04 al explicar la
implementación, y 07 antes de publicar una cifra.

## Cómo ejecutar

Desde la raíz, con el entorno preparado:

```bash
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m unittest discover -v
.venv/bin/python run_demo.py
.venv/bin/python verify_outputs.py
node verify_report.cjs
```

También se pueden usar `python run_demo.py --quick`, `--open`, `--config
ruta.json` y `--output carpeta`. El informe es local y no necesita servicios
externos.

## Qué produce

La ejecución genera `results.json`, `effective-config.json`, `cases.csv`,
`case-001.csv` a `case-018.csv`, `baseline.csv`, `thin-fin.csv`,
`thickness-sweep.csv`, `material-sweep.csv`, `tests.txt` e `index.html`.
Las siete figuras son:

1. `01-flight.png`, resumen de vuelo.
2. `02-flutter-history.png`, historia de \(V_f\), velocidad y ratio.
3. `03-altitude.png`, atmósfera y \(V_f\) frente a altitud.
4. `04-thickness-sweep.png`, espesores y materiales.
5. `05-geometry-map.png`, escala de planta y espesor.
6. `06-design-space.png`, espacio discreto de diseños.
7. `07-drag-sensitivity.png`, sensibilidad al factor de arrastre.

## Resultados de referencia

Son datos congelados de `outputs/results.json`, no mediciones. El objetivo de
selección es un ratio mínimo de **1.25**.

| Caso o material | Resultado |
|---|---:|
| Base: ratio mínimo \(V_f/V\) | **2.038** |
| Aleta delgada, 1.2 mm: ratio mínimo | **0.510** |
| Espesor requerido, aluminio 6061 | **2.17 mm** |
| Espesor requerido, G10 | **4.00 mm** |
| Espesor requerido, carbono tejido | **3.89 mm** |
| Espesor requerido, contrachapado de abedul | **7.23 mm** |
| Espesor requerido, acrílico/policarbonato | **6.42 mm** |

Los cinco espesores son para la trayectoria base y el objetivo 1.25. El
apogeo base es 3287.34 m AGL, la máxima rapidez relativa es 286.12 m/s y
Max-Q es 41.60 kPa.

## Límites del modelo

RocketPy conserva la responsabilidad de simular el vuelo. El módulo de
flutter es una aproximación empírica: usa \(G\), geometría, presión y
velocidad del sonido, pero no conoce la construcción real de las aletas.
Los barridos algebraicos no cambian la masa de la aleta; el caso delgado sí
se vuelve a simular. El ratio no es una probabilidad de fallo.

## Estructura del repositorio

`simulation.py` construye el vuelo, `flutter.py` calcula \(V_f\),
`materials.py` contiene datos de referencia, `study.py` evalúa casos,
`report.py` dibuja, y `run_demo.py` coordina la referencia. Los archivos
`verify_*.py` comprueban resultados y documentación. `data/` contiene datos
locales y `LICENSES/` conserva atribuciones.

## Licencias y fuentes

El proyecto conserva las atribuciones existentes. Las fuentes principales son
John K. Bennett (2023), la documentación de RocketPy, MatWeb y *Wood
Handbook FPL-GTR-190*. Las propiedades de materiales son valores típicos de
referencia, no propiedades certificadas. La fórmula y el ejemplo publicado
de 1425 ft/s se contrastan en [test_flutter.py](test_flutter.py).
