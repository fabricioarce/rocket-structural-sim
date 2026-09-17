# Simulador de cohetes con análisis preliminar de cargas

Proyecto educativo que usa **RocketPy para simular el vuelo** y añade una reconstrucción simplificada de cargas internas, un chequeo empírico de *fin flutter* y una comparación de diseños.

**La documentación empieza desde cero.** No necesitas programar para leer las gráficas ni para contribuir a la parte escrita. Sí necesitas distinguir un resultado de simulación de una medición real.

> **Estado:** prototipo computacional verificado con pruebas numéricas, **no validado experimentalmente**. No autoriza la fabricación ni el lanzamiento de un cohete. Cubre cargas del ascenso libre, después de abandonar el riel y hasta el apogeo; no toda la misión.

## Empieza aquí

| Si quieres… | Lee… |
|---|---|
| Entender el proyecto y cómo ayudar a redactarlo | [00 · Guía del equipo](docs/00-guia-del-equipo.md) |
| Aprender unidades, fuerzas, vuelo y aerodinámica | [01 · Física desde cero](docs/01-fisica-desde-cero.md) |
| Entender esfuerzo, flexión, masa distribuida y flutter | [02 · Estructuras y flutter](docs/02-estructuras-y-flutter.md) |
| Entender qué hace un programa y leer Python básico | [03 · Programación desde cero](docs/03-programacion-desde-cero.md) |
| Seguir cada cálculo, archivo y parámetro | [04 · Mapa del código y los datos](docs/04-codigo-y-datos.md) |
| Interpretar todos los paneles de las siete figuras | [05 · Gráficas explicadas](docs/05-graficas-explicadas.md) |
| Preparar justificación, objetivos, metodología y discusión | [06 · Guía de redacción y metodología](docs/06-metodologia-y-redaccion.md) |
| Instalar, ejecutar y reproducir resultados | [07 · Reproducibilidad y uso](docs/07-reproducibilidad.md) |
| Consultar símbolos, definiciones y fuentes | [08 · Glosario y referencias](docs/08-glosario-y-referencias.md) |

**Ruta sugerida para el equipo de redacción:** 00 → 01 → 02 → 05 → 06. Consulta 03 y 04 cuando necesites explicar la implementación. No copies una fórmula o conclusión que no puedas explicar con tus propias palabras.

## Ver resultados sin instalar Python

Las imágenes y los datos de una ejecución de referencia están incluidos en [outputs](outputs/). Puedes leer [la guía ilustrada](docs/05-graficas-explicadas.md) directamente en GitHub.

Para usar el inspector interactivo:

1. Descarga o clona **el repositorio completo**; no solo el HTML.
2. Abre `outputs/index.html` con tu navegador.
3. Selecciona un caso y una variable, o modifica los límites de la tabla.

GitHub muestra un archivo HTML como código o descarga: **este repositorio no configura GitHub Pages**. El informe funciona localmente, sin servidor ni conexión a internet. Los controles filtran simulaciones ya hechas; no ejecutan nuevas trayectorias.

![Mapa de esfuerzo longitudinal durante el ascenso libre](outputs/04-stress-map.png)

La imagen muestra esfuerzo modelado, no temperatura ni probabilidad de rotura. [Cómo leerla y qué significa la sección crítica](docs/05-graficas-explicadas.md#figura-04-mapa-de-esfuerzo).

## Qué está implementado

- Ejemplo de las cuatro clases principales de RocketPy: ambiente, motor, cohete y vuelo.
- Caso basado en Calisto y motor Cesaroni M1670, con datos locales.
- Fuerzas por superficie con orientación y velocidad local del aire.
- Viga libre equivalente con alivio inercial traslacional y angular, cargas axiales, cortantes y momentos en dos planos.
- Máximo esfuerzo longitudinal combinado por **sección e instante**.
- Frontera empírica de flutter según la revisión de Bennett de 2023.
- Malla de 9 diseños y 2 vientos: **18 casos**, no 18 ensayos experimentales.
- Selección del mayor apogeo mínimo entre los escenarios de viento que cumplen los criterios definidos.
- Caso adicional de aletas delgadas, sensibilidad a Cd ±15% y refinamiento numérico del caso base.
- Siete figuras PNG, informe HTML, series CSV y metadatos JSON.

## Resultados de referencia, no mediciones

Configuración: [demo.json](demo.json). Datos de respaldo: [results.json](outputs/results.json) y [cases.csv](outputs/cases.csv).

| Magnitud del caso base | Resultado aproximado |
|---|---:|
| Carga útil **añadida** | 0 kg |
| Viento transversal constante | 4 m/s |
| Apogeo sobre el lanzamiento, AGL | 3287 m |
| Máxima velocidad relativa al aire muestreada | 286.1 m/s |
| Máxima presión dinámica | 41.60 kPa, en 3.341 s |
| Máximo esfuerzo longitudinal modelado | 3.439 MPa, en 1.000 s |
| Mínimo cociente de flutter Vf/V | 2.038 |
| Mínimo Vf/V con aletas de 1.2 mm | 0.510 |

**No basta con estos números para decir que el cohete es seguro.** En esta malla el máximo esfuerzo es casi idéntico entre diseños, dominado por el empuje aplicado en la cola y la sección uniforme. La selección no demuestra una optimización estructural validada. Además, al cambiar aletas se conserva el Cd total original: el ranking geométrico es demostrativo.

## Ejecutar en el entorno ya preparado

Desde la raíz del proyecto, en Linux:

```bash
.venv/bin/python run_demo.py --output outputs-local --open
```

Para una instalación nueva, Windows o una ejecución rápida, sigue [la guía de reproducibilidad](docs/07-reproducibilidad.md). La versión comprobada es Python 3.14.7 con las dependencias fijadas en [requirements.txt](requirements.txt).

### Verificación

```bash
.venv/bin/python -m unittest discover -v
.venv/bin/python verify_outputs.py
.venv/bin/python verify_docs.py
node verify_report.cjs
```

Node.js se usa únicamente en el último chequeo de la lógica de la interfaz; no es necesario para las simulaciones ni para abrir el HTML. Estas comprobaciones no sustituyen la validación física independiente.

## Límites principales

- La distribución interna de masas es **equivalente**, no medida.
- La estructura se trata como una sección tubular uniforme con propiedades supuestas.
- No incluye pandeo, uniones, torsión, recuperación, reacciones del riel ni un análisis modal.
- El modelo estructural cuasiestático no reproduce todos los términos de la dinámica de masa variable de RocketPy.
- El criterio de esfuerzo es un límite de estudio configurable, no un admisible certificado del material.
- La velocidad de flutter es una frontera empírica, no una simulación de vibraciones o una predicción del instante de rotura.

## Créditos y procedencia

El ejemplo Calisto, los archivos de `data/` y partes de la configuración/adaptación se basan en [RocketPy](https://github.com/RocketPy-Team/RocketPy). Se conserva su [aviso de licencia MIT](LICENSES/RocketPy-MIT.txt). Las fórmulas físicas y sus fuentes están identificadas en [las referencias](docs/08-glosario-y-referencias.md).

Esta publicación no asigna por sí sola una licencia general a las aportaciones nuevas; esa elección corresponde al titular del proyecto. Tampoco atribuye a RocketPy la validación del módulo estructural desarrollado aquí.
