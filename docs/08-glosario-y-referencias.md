# 08 · Glosario, símbolos y fuentes

[Índice](../README.md) · [Anterior: reproducibilidad](07-reproducibilidad.md)

## Glosario

| Término | Definición para este proyecto |
|---|---|
| Aceleración | Cambio de velocidad por tiempo; puede cambiar rapidez, dirección o ambas |
| Admisible | Cumple los criterios configurados del estudio, no una certificación de seguridad |
| Aeroelasticidad | Interacción entre fuerzas aerodinámicas y deformación de una estructura |
| AGL | Altura sobre el terreno de referencia de lanzamiento |
| Algoritmo | Procedimiento expresado como pasos de cálculo o decisión |
| Alivio inercial | Reconstrucción que equilibra cargas externas mediante cargas inerciales equivalentes |
| API | Interfaz para utilizar funciones, clases y datos de una biblioteca |
| Apogeo | Máxima altura del ascenso; velocidad vertical nula en ese instante idealizado |
| Array | Estructura numérica que contiene varios valores con forma definida |
| Arrastre | Fuerza aerodinámica que se opone al movimiento relativo al aire según la descomposición utilizada |
| ASL | Altitud sobre el nivel del mar |
| Barrido paramétrico | Evaluación de combinaciones discretas de entradas |
| Biblioteca | Herramientas de software reutilizables |
| Burnout | Fin de combustión/empuje del motor según el modelo |
| Calibre | En el margen estático, unidad igual al diámetro de referencia del cuerpo |
| Carga útil añadida | Masa agregada al ejemplo de referencia, no masa total del vehículo |
| Cd | Coeficiente de arrastre respecto a un área y condiciones definidas |
| Centro de masa / CG | Posición media ponderada por las masas; para gravedad aproximadamente uniforme coincide con centro de gravedad |
| Centro de presión / CP | Posición equivalente de la acción aerodinámica según el modelo y el flujo |
| Commit | Identificador de una versión registrada con Git |
| Convergencia numérica | Tendencia de una solución aproximada al refinar el procedimiento; un chequeo de dos resoluciones es evidencia limitada |
| Cortante | Resultante interna transversal a un corte |
| Cribado | Filtrado mediante condiciones explícitas |
| CSV | Formato de tabla de texto con separadores |
| Cuadratura | Aproximación de una integral con nodos y pesos |
| Cuaternión | Representación de orientación usada para transformar entre sistemas de ejes |
| Densidad | Masa por volumen; especificar si se habla de aire, aleta u otro material |
| Empuje | Acción propulsiva representada mediante el motor y su intercambio de cantidad de movimiento |
| Equilibrio de cargas efectivas | Cierre de fuerzas y momentos externos más inerciales en la reconstrucción |
| Esfuerzo | Intensidad local de fuerzas internas, expresada por unidad de área; no equivale a fuerza total |
| FEA | Análisis por elementos finitos; no está implementado como validación independiente aquí |
| Flexión | Deformación de curvatura asociada a momentos flectores |
| Fluencia | Inicio de deformación plástica según un material y un criterio |
| Flutter | Inestabilidad aeroelástica; no es sinónimo de cualquier vibración o resonancia |
| Función | Operación de software con entradas y salidas; también relación matemática entre variables |
| GitHub | Servicio que aloja repositorios; no es el intérprete de Python |
| Grados de libertad | Movimientos independientes usados para describir un sistema |
| HTML | Formato de la página del informe |
| Inercia de masa | Resistencia al cambio de rotación; unidad kg·m² |
| Interpolación | Estimación de valores entre muestras conocidas |
| JSON | Formato de datos estructurados usado para configuración y resultados |
| Mach | Rapidez relativa al aire dividida por velocidad local del sonido |
| Margen de flutter | Cociente Vf/Vrel en este proyecto; no probabilidad de fallo |
| Margen estático | Distancia de CG por delante de CP dividida por diámetro, según convención |
| Max-Q | Máxima presión dinámica del intervalo analizado |
| Momento flector | Resultante de giro interna asociada a flexión, en N·m |
| Nodo equivalente | Punto de cálculo que representa una parte de una distribución; no una pieza identificada |
| Pandeo | Pérdida de estabilidad estructural bajo cargas como compresión |
| Parámetro | Entrada o constante elegida del modelo |
| Presión dinámica | q = ρ Vrel²/2, escala aerodinámica definida; no esfuerzo de material |
| Presión estática | Propiedad termodinámica local de la atmósfera |
| Refinamiento | Aumento de resolución de una representación o cálculo |
| Resonancia | Respuesta a excitación próxima a frecuencias relevantes; depende de amortiguamiento y acoplamientos |
| Residuo | Lo que queda de una igualdad que debería cerrar dentro de tolerancia |
| Rigidez | Resistencia a deformarse; no es lo mismo que resistencia a fallar |
| Segundo momento de área | Propiedad geométrica de una sección, en m⁴, usada en flexión |
| Sección crítica | Sección donde se encontró el máximo de la métrica estructural elegida |
| Sensibilidad | Cambio de un resultado al perturbar una entrada; no implica una probabilidad de ocurrencia |
| Simulación | Aplicación computacional de un modelo a unas condiciones |
| Validación física | Contraste del modelo con evidencia apropiada del sistema real |
| Verificación | Comprobación de implementación, ecuaciones o consistencia numérica |
| Viga libre | Modelo sin empotramiento o apoyo externo; puede tener cargas aplicadas y movimiento |

## Símbolos y unidades

| Símbolo | Significado aquí | Unidad |
|---|---|---|
| t | Tiempo desde ignición | s |
| z | Según contexto, altitud o estación axial; no confundir sistemas | m |
| m | Masa | kg |
| g | Aceleración gravitatoria | m/s² |
| a | Aceleración traslacional, cuando no se indica otra cosa | m/s² |
| as | Velocidad del sonido en la explicación de flutter | m/s |
| Vrel | Rapidez relativa al aire | m/s |
| T, D | Empuje, arrastre | N |
| ρ | Densidad del aire | kg/m³ |
| p, q | Presión estática, presión dinámica | Pa |
| Cd | Coeficiente de arrastre | Sin unidad |
| α | Ángulo de ataque | rad o grados, según interfaz |
| αang | Aceleración angular | rad/s² |
| N | Carga axial, positiva en compresión en el módulo | N |
| V | Cortante en el contexto estructural | N |
| M | Momento flector | N·m |
| σ | Esfuerzo normal longitudinal | Pa o MPa al exportar |
| E, G | Módulo de Young, módulo de corte | Pa |
| Amaterial | Área de material de una sección | m² |
| Aref | Área de referencia aerodinámica | m² |
| IA | Segundo momento de área | m⁴ |
| Imasa | Inercia de masa | kg·m² |
| cr, ct, b, s | Cuerda raíz, cuerda punta, envergadura y barrido de aleta | m |
| δ | Espesor de aleta en la explicación; el código usa nombres con `thickness` | m |
| S | Área de una aleta | m² |
| AR, λ, ε | Relaciones geométricas del modelo de flutter | Sin unidad |
| γ | Razón de calores específicos del aire en la aproximación | Sin unidad |
| Vf | Frontera nominal de velocidad de flutter | m/s |
| Rf | Cociente Vf/Vrel | Sin unidad |

Que dos magnitudes compartan unidad no las convierte en lo mismo. Presión y esfuerzo se expresan en Pa; una es una propiedad del fluido en este contexto y la otra describe fuerzas internas del sólido. Momento y energía usan unidades dimensionalmente equivalentes, pero no representan el mismo concepto.

## Fuentes

Las fuentes respaldan conceptos o métodos concretos; **ninguna certifica este prototipo**. No se asignan propiedades reales al cohete a partir de tablas genéricas. Las consultas documentales se indican sin inventar fechas de publicación que no se hayan confirmado.

### F1 · Dinámica y fuerzas internas/externas

**OpenStax.** *University Physics Volume 1*, sección 5.3, “Newton’s Second Law”.

- Fuente: https://openstax.org/books/university-physics-volume-1/pages/5-3-newtons-second-law
- Consultada: 2026-09-16.
- Respalda: diferencia entre fuerzas internas y externas y relación fuerza neta–masa–aceleración.
- No usar para: sustituir sin más las ecuaciones de un cohete de masa variable por un bloque de masa constante.

### F2 · Esfuerzo, deformación y módulos elásticos

**OpenStax.** *University Physics Volume 1*, sección 12.3, “Stress, Strain, and Elastic Modulus”.

- Fuente: https://openstax.org/books/university-physics-volume-1/pages/12-3-stress-strain-and-elastic-modulus
- Consultada: 2026-09-16.
- Respalda: esfuerzo, deformación, módulo de Young y módulo de corte; límites del régimen lineal.
- No usar para: declarar que los valores supuestos del ejemplo pertenecen al material real de Calisto.

### F3 · Presión dinámica

**NASA Glenn Research Center.** “Dynamic Pressure”, *Beginners Guide to Aeronautics*.

- Fuente: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/dynamic-pressure/
- Consultada: 2026-09-16.
- Respalda: definición `q = ρ V²/2` y uso como escala aerodinámica.
- No usar para: identificar q con esfuerzo máximo del material o presión uniforme sobre toda la superficie.

### F4 · Arrastre y área de referencia

**NASA Glenn Research Center.** “Drag Equation”, *Beginners Guide to Aeronautics*.

- Fuente: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-equation/
- Consultada mediante su contenido indexado: 2026-09-16.
- Respalda: `D = Cd ρ V² Aref/2`, dependencias y necesidad de definir el área de referencia.
- No usar para: suponer que Cd no cambia con la geometría real.

### F5 · Estabilidad de cohetes con aletas

**NASA Glenn Research Center.** “Rocket Stability”, *Beginners Guide to Aeronautics*.

- Fuente: https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/rocket-stability/
- Consultada: 2026-09-16.
- Respalda: momentos restauradores y relación entre centro de gravedad y centro de presión.
- No usar para: presentar un umbral particular de calibres como criterio universal o una garantía dinámica/estructural.

### F6 · Esfuerzos de flexión en vigas

**David Roylance / MIT OpenCourseWare.** “Stresses in Beams”, material de *3.11 Mechanics of Materials, Fall 1999*.

- Fuente: https://ocw.mit.edu/courses/3-11-mechanics-of-materials-fall-1999/96d839b02e4a6c63cf8031800e89cccd_MIT3_11F99_bstress.pdf
- Localizada y consultada mediante su contenido indexado: 2026-09-16.
- Respalda: esfuerzo longitudinal por flexión, distribución a través de la sección y papel del segundo momento de área.
- No usar para: afirmar que una viga tubular equivalente representa todas las uniones y mecanismos de fallo del cohete.

### F7 · Flutter empírico y corrección de la fórmula

**John K. Bennett (2023).** *Fin Flutter Analysis Revisited (Again)*, diciembre de 2023; especialmente páginas 5–9 y ejemplo numérico.

- Fuente: https://www.nakka-rocketry.net/articles/Calculating_Fin_Flutter_Velocity_Bennett-12-23.pdf
- Consulta técnica registrada durante la implementación: 2026-09-15.
- Respalda: fórmula, corrección de la sobreestimación por √2, parámetros geométricos y ejemplo aproximado de 1425 ft/s.
- Verificación local: [test_flutter.py](../test_flutter.py).
- No usar para: predecir rotura exacta, extrapolar sin revisar régimen o caracterizar laminados/uniones desconocidos.

La referencia histórica de NACA mencionada por esa literatura no se presenta aquí como si el equipo hubiera reproducido y validado todos sus ensayos originales. Para una revisión formal conviene localizar y leer la fuente primaria, verificando incluso su identificación bibliográfica.

### F8 · RocketPy y datos del ejemplo

**RocketPy Team.** Documentación oficial:

- Primera simulación: https://docs.rocketpy.org/en/latest/user/first_simulation.html
- Clase Flight: https://docs.rocketpy.org/en/latest/reference/classes/Flight.html
- Repositorio: https://github.com/RocketPy-Team/RocketPy
- Consultas técnicas registradas en la implementación: 2026-09-15.
- Código local contrastado: RocketPy 1.13.0.

Respalda la interfaz utilizada, convenciones y configuración del ejemplo. La URL `latest` puede cambiar; para reproducir esta publicación usa las versiones y archivos locales fijados, no copies automáticamente un ejemplo futuro.

Los archivos locales proceden de las rutas de RocketPy:

- `data/motors/cesaroni/Cesaroni_M1670.eng`.
- `data/rockets/calisto/powerOffDragCurve.csv`.
- `data/rockets/calisto/powerOnDragCurve.csv`.
- `data/airfoils/NACA0012-radians.txt`.

Se conservan checksums en [results.json](../outputs/results.json). La descarga inicial se hizo desde `master`; no se registró entonces un commit de procedencia de esos archivos. **No se inventa ahora uno.** Para esta publicación, las copias locales y sus hashes identifican exactamente los datos utilizados.

La licencia upstream se consultó el 2026-09-16 en https://raw.githubusercontent.com/RocketPy-Team/RocketPy/master/LICENSE y se conserva en [LICENSES/RocketPy-MIT.txt](../LICENSES/RocketPy-MIT.txt).

### F9 · Python

**Python Software Foundation.** *El tutorial de Python*, documentación en español.

- Fuente: https://docs.python.org/es/3/tutorial/
- Consultada: 2026-09-16; página presentada como documentación 3.14.7.
- Respalda: lenguaje, funciones, colecciones, clases, módulos y entornos virtuales.
- Nota pedagógica: el tutorial oficial indica que presupone conocimientos generales de programación; el capítulo 03 de esta guía introduce esos conceptos previos.

### F10 · Qué no incluye OpenRocket

**OpenRocket wiki.** “Third-Party Compatibility”.

- Fuente: https://wiki.openrocket.info/Third-Party_Compatibility
- Consulta técnica registrada: 2026-09-15.
- Respalda: la documentación declara que OpenRocket no analiza flutter o velocidad de divergencia.
- No usar para: afirmar que no existe otro software de flutter o que esta implementación es novedosa por sí sola.

## Evidencia propia, separada de las fuentes externas

- [Configuración de referencia](../outputs/effective-config.json): entradas realmente usadas.
- [Resultados completos](../outputs/results.json): números de esta simulación, no de un ensayo.
- [Casos del barrido](../outputs/cases.csv): comparación determinista.
- [Pruebas](../outputs/tests.txt): verificación de implementación.
- [Código estructural](../structural_loads.py): supuestos efectivos del método.

Para la bibliografía formal utiliza el estilo que pida la actividad. Antes de asignar autor, año, DOI o una afirmación específica, compruébalo en la fuente. No rellenes información faltante con una cita inventada.

**Siguiente paso:** construye una tabla con cada afirmación importante del borrador, su fuente y la sección exacta que la respalda. Marca por separado las inferencias propias del equipo.
