# 06 · Cómo preparar la justificación y la parte escrita

[Índice](../README.md) · [Anterior: gráficas](05-graficas-explicadas.md) · [Siguiente: reproducibilidad](07-reproducibilidad.md)

Esta guía no es una justificación terminada ni inventa un contexto experimental. Propone una estructura para que el equipo escriba a partir de una pregunta acordada, fuentes revisadas y resultados trazables.

## 1. Diagnóstico del alcance actual

El trabajo actual puede presentarse como **desarrollo y verificación numérica de un prototipo computacional para explorar relaciones entre vuelo y cargas preliminares**.

No alcanza todavía para afirmar:

- Que predice las cargas reales de un vehículo con una precisión conocida.
- Que sustituye ensayos o análisis estructural detallado.
- Que encuentra el diseño óptimo de un cohete real.
- Que reduce costos o accidentes en un porcentaje determinado.
- Que tiene una novedad científica demostrada frente a toda la literatura.

La razón no es que un simulador sea inútil, sino que faltan datos, validación independiente y una comparación sistemática que sostenga esas conclusiones.

## 2. Problema, justificación y objetivo: diferencias

| Sección | Pregunta que contesta | Error que evitar |
|---|---|---|
| Planteamiento del problema | ¿Qué dificultad concreta existe y para quién? | «El problema es que queremos hacer un programa» |
| Justificación | ¿Por qué vale la pena abordar esa dificultad con este alcance? | Beneficios sociales o económicos inventados |
| Marco teórico | ¿Qué conceptos y modelos necesitamos? | Coleccionar fórmulas sin relacionarlas con el cálculo |
| Objetivos | ¿Qué resultados o capacidades vamos a producir y evaluar? | Prometer seguridad real cuando solo se verifica una demo |
| Metodología | ¿Cómo se obtiene y evalúa la respuesta? | Confundir el nombre de una biblioteca con todo el método |
| Resultados | ¿Qué se obtuvo? | Explicar antes de mostrar datos o mezclar escenarios |
| Discusión | ¿Qué significan los resultados y cuáles son sus límites? | Generalizar una tendencia de una malla a cualquier cohete |
| Conclusiones | ¿Qué responde efectivamente el trabajo? | Introducir afirmaciones nuevas sin evidencia |

## 3. Construir una justificación sin inventar hechos

Una secuencia de argumentos posible, para desarrollar con palabras del equipo:

1. **Necesidad técnica:** la trayectoria por sí sola no describe todas las cargas internas. Respaldar la distinción entre dinámica y mecánica estructural con fuentes [F1, F2, F6](08-glosario-y-referencias.md#fuentes).
2. **Contexto concreto:** describir quién necesita comparar diseños y qué dificultades ha observado. Esta información debe aportarla el equipo; no está determinada por el repositorio.
3. **Enfoque:** reutilizar RocketPy permite obtener condiciones de vuelo y dedicar la extensión a cargas, relaciones y trazabilidad.
4. **Aporte alcanzable:** integrar una cadena reproducible de cálculo y presentar claramente sus supuestos, criterios y relaciones.
5. **Límite:** el prototipo no reemplaza caracterización de materiales, modelado de uniones o validación física.

**Ejemplo de frase defendible sobre el prototipo, no de una justificación completa:**

> El proyecto integra condiciones de vuelo obtenidas con RocketPy con una reconstrucción cuasiestática simplificada de cargas y un chequeo empírico de flutter, para comparar escenarios de diseño con supuestos y límites explícitos.

Antes de escribir «herramienta accesible», defina accesible en términos verificables: requisitos de software, documentación, instalación, necesidad de datos o conocimientos. No suponga que usar Python demuestra por sí solo facilidad de uso o costo cero.

Antes de escribir «no existe una herramienta similar», realice una revisión comparativa. La documentación de OpenRocket indica que no incluye flutter [F10], pero eso no prueba que ningún otro programa lo calcule.

## 4. Pregunta y objetivos: propuestas para discutir

Una pregunta **compatible con la implementación actual** sería:

> ¿Cómo cambian las métricas de vuelo, cargas longitudinales preliminares y margen empírico de flutter al variar carga útil añadida y escala de aletas, bajo escenarios definidos de viento y una configuración basada en Calisto?

Esta formulación estudia el comportamiento del modelo; no afirma que reproduce ya las cargas reales.

Un objetivo general posible es desarrollar y verificar numéricamente una herramienta reproducible para esa comparación. Objetivos específicos posibles:

1. Reproducir un caso de vuelo con entradas y unidades identificadas.
2. Reconstruir cargas internas bajo una distribución equivalente de masa y comprobar equilibrio.
3. Evaluar una frontera empírica de flutter a lo largo del ascenso libre.
4. Comparar una malla de diseños bajo criterios explícitos y reportar casos descartados.
5. Examinar sensibilidad y refinamiento, y delimitar lo que requerirá validación física.

**No están aprobados automáticamente:** revisarlos con el contexto, los requisitos de la actividad y el papel de cada integrante. Si la meta cambia a diseño de un cohete real, estos objetivos y el método deben ampliarse.

## 5. Describir el diseño del estudio

### Tipo de evidencia

Es un estudio computacional determinista de escenarios. No es un experimento aleatorizado, un estudio poblacional ni un Monte Carlo.

### Factores y controles

| Tipo | En la ejecución de referencia |
|---|---|
| Variables de diseño exploradas | Masa añadida: 0, 3, 6 kg; escala de aletas: 0.85, 1, 1.15 |
| Escenario ambiental | Viento transversal constante: 0 y 4 m/s |
| Condiciones comunes | Motor M1670, geometría de cuerpo, lanzamiento, modelo atmosférico y sección estructural supuesta |
| Respuestas | Apogeo, velocidades, Max-Q, N/V/M, esfuerzo, margen de flutter y criterios de estabilidad |
| Sensibilidad separada | Factor de Cd de 0.85, 1 y 1.15 para el caso base |
| Caso ilustrativo adicional | Espesor de aleta multiplicado por 0.4, con masa y vuelo recalculados |

18 casos son 9 diseños en 2 vientos. No son 18 réplicas del mismo experimento. Las filas temporales de un CSV están relacionadas por una trayectoria; no son observaciones independientes que permitan inflar el tamaño de muestra.

### Procedimiento reproducible

1. Registrar versión de código y entorno, datos y configuración.
2. Construir las propiedades agregadas y la distribución equivalente para cada diseño.
3. Simular el vuelo hasta el apogeo.
4. Analizar solo el ascenso libre después del riel.
5. Evaluar fuerzas locales y reconstruir cargas por sección.
6. Calcular esfuerzo longitudinal y frontera de flutter.
7. Aplicar criterios de descarte sin ocultar los motivos.
8. Comparar diseños en todos los escenarios de viento definidos.
9. Repetir el caso base con resolución refinada y evaluar cambios.
10. Exportar resultados y relacionarlos con las figuras.

La sección de métodos debe indicar qué hace RocketPy y qué añade este proyecto. La validación de una biblioteca de vuelo no se transfiere automáticamente a una extensión estructural.

## 6. Explicar la selección con restricciones

Para cada diseño d y escenario de viento w, sea `H(d,w)` su apogeo AGL. El objetivo implementado es:

$$
\max_{d\in\mathcal D}\ \min_{w\in\mathcal W}H(d,w)
$$

sujeto a que se cumplan los criterios de esfuerzo, flutter, estabilidad, salida del riel y alcance del modelo **en todos** los escenarios muestreados.

En lenguaje cotidiano: calculamos la menor altura de cada diseño entre los vientos considerados, descartamos los que incumplen condiciones y elegimos el mejor de los restantes.

No significa «soporta cualquier viento». No es un óptimo continuo ni una garantía probabilística. Los valores entre nodos de la malla y otros entornos no se han optimizado.

En el ejemplo:

- La combinación de 0 kg añadidos y aletas ×0.85 tiene mayor apogeo, pero margen estático inferior al criterio de un calibre.
- La combinación de 0 kg añadidos y aletas ×1 pasa el cribado y es la seleccionada.
- Con carga útil mínima de 3 kg, la selección entre los casos existentes cambia; no se ejecuta un nuevo vuelo al cambiar ese filtro del HTML.

**Resultado metodológico clave:** todos los máximos de esfuerzo son aproximadamente 3.439 MPa. El límite predeterminado de 4 MPa no es la restricción activa que distingue los diseños. No describir la selección actual como si hubiera encontrado una frontera resistente de diseño.

## 7. Verificación frente a validación

| Comprobación | Qué respalda | Qué no respalda |
|---|---|---|
| Prueba con solución conocida | Una implementación produce la solución esperada de ese caso | Validez de todas las hipótesis de Calisto |
| Cierre de fuerza y momento | Consistencia del equilibrio del modelo | Exactitud de la distribución de masa real |
| Comparación de fuerzas con RocketPy | Consistencia del adaptador con la biblioteca en los casos probados | Validación independiente de la aerodinámica |
| Ejemplo publicado de flutter | Reproducción numérica de esa fórmula y sus unidades | Predicción de rotura de estas aletas reales |
| Refinamiento del caso base | Menor dependencia de las resoluciones comparadas | Error físico menor al 5% o convergencia de toda la malla |
| Ensayo o instrumentación independiente | Podría contrastar el modelo con el objeto real | **No se ha realizado en este repositorio** |

El umbral del 5% es una regla de comprobación numérica del prototipo, no una incertidumbre experimental calculada. En el caso base la variación del máximo momento entre las resoluciones es aproximadamente 0.109%; no debe llamarse «error respecto al valor verdadero».

## 8. Amenazas a la validez que deben aparecer en la discusión

| Limitación | Por qué importa | Camino concreto para reducirla |
|---|---|---|
| Cd total fijo al cambiar aletas | Puede sesgar el ranking de altura | Obtener curvas específicas por geometría y documentar su procedencia |
| Masa interna equivalente | Los esfuerzos locales dependen de dónde están las masas | Medir distribución y posiciones de componentes; hacer análisis de sensibilidad a su ubicación |
| Empuje y arrastre concentrados | Pueden dominar artificialmente una sección o ignorar soportes | Representar transmisión de cargas y comparar con un modelo independiente |
| Sección uniforme | Ignora nariz, variaciones de espesor, acoples y concentraciones | Definir tramos estructurales y uniones reales |
| Solo esfuerzo longitudinal | Omite otros mecanismos de fallo | Añadir criterios apropiados de pandeo, cortante, torsión, laminados y uniones con datos suficientes |
| Flutter empírico | No calcula modos, amortiguamiento ni adhesivos | Contrastar con análisis aeroelástico o ensayo adecuado al material |
| Dos vientos constantes | No representan ráfagas ni una distribución de entornos | Definir perfiles y rangos con datos del sitio; distinguir escenarios de probabilidades |
| Omisión de riel y recuperación | El máximo de misión podría estar fuera del intervalo | Ampliar las fases con modelos de apoyos y despliegue verificables |
| Resolución comparada solo en la base | Otros casos pueden requerir más detalle | Refinar también diseños extremos y cercanos a los límites |

Un número mayor de casos no corrige automáticamente una limitación compartida por todos ellos.

## 9. Matriz para redactar resultados sin exagerar

| Afirmación | ¿Se puede escribir ahora? | Evidencia o condición |
|---|---|---|
| «Se implementó un barrido de 18 escenarios» | Sí | Configuración y casos exportados |
| «El caso base simulado alcanza unos 3287 m AGL» | Sí | Identificar configuración y versión |
| «En esta malla, la carga útil añadida reduce el apogeo calculado» | Sí | Comparaciones manteniendo los otros factores correspondientes |
| «Añadir masa siempre reduce la altura de cualquier cohete» | No | Generalización no demostrada |
| «El máximo de esfuerzo coincide con Max-Q» | No para esta base | Ocurren en instantes distintos |
| «El material real tiene un factor de seguridad de 80» | No | Propiedades y camino de carga supuestos; mecanismos omitidos |
| «Con aletas delgadas, Vf/V cae por debajo de 1 en la aproximación usada» | Sí | Caso delgado y fórmula identificados |
| «Las aletas se rompen exactamente en ese instante» | No | No hay modelo de rotura ni evidencia experimental |
| «El software pasó las pruebas incluidas» | Sí | Adjuntar resultados de las pruebas de esa versión |
| «El software está validado para diseñar cohetes reales» | No | Falta validación independiente |

## 10. Cómo escribir un párrafo sobre una figura

Estructura útil:

1. **Condición:** qué caso o comparación se está observando.
2. **Dato:** qué cambia y cuánto, con unidad y fuente.
3. **Mecanismo:** relación física compatible con el modelo.
4. **Límite:** qué explicación alternativa o simplificación condiciona la interpretación.

Ejemplo de análisis acotado:

> En el caso base con viento constante de 4 m/s, el máximo esfuerzo longitudinal modelado ocurre a 1 s, mientras Max-Q se alcanza alrededor de 3.341 s. El primer máximo está dominado por la transmisión del empuje en la sección trasera equivalente. Este resultado corresponde al camino de carga y sección supuestos y no localiza necesariamente la sección crítica del cohete real.

No usar «se demuestra» cuando solo se observa una tendencia compatible con una explicación. Las oscilaciones de momento de la figura 02 no prueban flutter: el modelo no calcula deformaciones de aletas.

## 11. Organización práctica del trabajo escrito

Reparto sugerido por tareas, sin asumir quién integra el equipo:

- Una persona revisa conceptos y unidades del marco teórico.
- Otra construye la tabla fuente–afirmación y compara herramientas existentes.
- Otra explica las figuras y contrasta cifras con CSV/JSON.
- Quien conoce la física y el código revisa supuestos y coherencia de los métodos.
- El equipo acuerda pregunta, alcance y conclusiones; no se delegan a una plantilla.

Para cada fuente guarda autor o institución, título, fecha disponible, enlace, fecha de consulta y qué afirmación respalda. No cites una herramienta de IA como si fuera la fuente física primaria. Si las reglas de la actividad piden declarar su uso, describan de forma honesta su contribución al código y a la documentación.

## 12. Lista previa a entregar

- [ ] Pregunta y objetivos compatibles con lo realmente implementado.
- [ ] Todas las variables y unidades definidas.
- [ ] Geometría, material y condiciones supuestas identificadas como tales.
- [ ] Cada figura tiene pie, condiciones, fuente y una interpretación limitada.
- [ ] No se confunden escenarios, réplicas y muestras temporales.
- [ ] No se presenta el umbral de 4 MPa como fluencia certificada.
- [ ] Se explica la conservación del Cd original en el barrido de aletas.
- [ ] Se distingue consistencia con RocketPy de validación independiente.
- [ ] Se discute por qué la restricción estructural no discrimina esta malla.
- [ ] Commit y configuración de resultados registrados.
- [ ] Las conclusiones responden la pregunta sin prometer seguridad de vuelo.

**Siguiente paso:** acuerden una pregunta y redacten la necesidad concreta del usuario del proyecto. Después asignen a cada afirmación de la justificación una fuente o un dato; si no existe, reformúlenla como objetivo o cuestión pendiente.
