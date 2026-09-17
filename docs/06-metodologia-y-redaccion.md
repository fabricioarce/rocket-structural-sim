# 06 · Metodología y redacción para un estudio de flutter

[Índice](../README.md) · [Anterior: gráficas](05-graficas-explicadas.md) ·
[Siguiente: reproducibilidad](07-reproducibilidad.md)

## 1. Pregunta e hipótesis

Pregunta: ¿qué combinación de espesor, material y escala de aleta mantiene el
ratio nominal por encima de 1.25 durante la trayectoria?

Hipótesis de trabajo:

1. Aumentar el espesor aumenta el ratio porque \(V_f\propto t^{3/2}\).
2. Un material con mayor \(G\) necesita menos espesor para la misma trayectoria.
3. El mínimo del ratio se aproxima al máximo de presión dinámica.
4. Cambiar el arrastre modifica trayectoria y ratio, por lo que la conclusión
   debe sobrevivir la sensibilidad \(C_D\times0.85/1.15\).

Son hipótesis comprobables en la malla, no afirmaciones universales.

## 2. Método

1. Cargar `demo.json`.
2. Construir cada `Design`.
3. Simular con RocketPy hasta apogeo.
4. Muestrear salida de riel, Max-Q, máxima velocidad y burnout.
5. Obtener \(p,a_s,V_{\mathrm{rel}}\) y calcular `flutter_history`.
6. Calcular espesor requerido y resumir estabilidad, Mach y apogeo.
7. Evaluar la malla de 18 casos y seleccionar el mejor grupo admisible.
8. Comparar aleta delgada, materiales, espesores, arrastre y refinamiento.

El umbral 1.25, estabilidad, velocidad de riel, ángulo de ataque y Mach son
criterios configurables del estudio. «Admisible» significa que pasa esas
reglas en los escenarios muestreados.

## 3. Resultados de referencia

El caso base alcanza 3287.34 m AGL, 286.12 m/s de rapidez relativa y ratio
mínimo 2.03819628. La aleta de 1.2 mm alcanza ratio 0.51033860. El barrido
requiere 2.17 mm de aluminio 6061 y 7.23 mm de contrachapado de abedul para
el objetivo 1.25.

El cálculo algebraico de la aleta delgada produce 0.51562740 frente a 0.51033860
re-simulado; la diferencia relativa 0.01036333 queda registrada en
`thin_algebraic_relative_difference`.

## 4. Qué significa validar aquí

Las pruebas verifican código, ecuaciones, orden de muestras, consistencia de
CSV y selección reproducible. El refinamiento compara apogeo, rapidez y ratio
entre resoluciones; no es una incertidumbre experimental.

La fórmula de Bennett se comprueba con su ejemplo publicado y el modelo se
mantiene dentro de las hipótesis documentadas. Eso no valida una aleta real:
faltan construcción, uniones, laminado, amortiguamiento y mediciones.

## 5. Cómo redactar sin exagerar

Preferir:

> «En la trayectoria base, el modelo calcula un ratio mínimo 2.038 cerca de
> Max-Q.»

Evitar:

> «La aleta es segura» o «el cohete soporta 2.038 veces la velocidad».

El ratio es adimensional y nominal. Un valor menor que uno señala que la
trayectoria cruza la frontera de la aproximación, no la probabilidad de rotura.

## 6. Discusión y límites

El modelo usa cinco materiales con \(G\) y densidad típicos. Deben sustituirse
por fichas técnicas para un diseño concreto. El barrido algebraico ignora el
cambio de masa; por eso el caso delgado re-simulado es una comprobación
separada.

RocketPy es la fuente de la trayectoria. El proyecto no predice amplitud,
rotura, modos, uniones, laminados, amortiguamiento ni divergencia. Tampoco
convierte el resultado en una autorización de lanzamiento.

## 7. Lista de revisión

- [ ] La pregunta menciona flutter y aletas.
- [ ] Cada número tiene archivo de origen.
- [ ] Se distingue AGL de ASL.
- [ ] Se distingue \(V_f\) de \(V_{\mathrm{rel}}\).
- [ ] Se indica si el resultado es algebraico o re-simulado.
- [ ] Se conserva el límite 1.25 y su carácter de criterio.
- [ ] Se explican los límites del modelo.
