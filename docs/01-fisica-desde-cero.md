# 01 · Física desde cero: del movimiento al vuelo

[Índice](../README.md) · [Anterior](00-guia-del-equipo.md) · [Siguiente: estructuras](02-estructuras-y-flutter.md)

**Objetivo:** entender qué representa cada magnitud antes de utilizar fórmulas. Los ejemplos redondos de este capítulo son didácticos; no son resultados medidos de Calisto. Fuentes: [F1–F5 y F8](08-glosario-y-referencias.md#fuentes).

## 1. Número, magnitud y unidad

Decir «el cohete pesa 20» no basta. ¿20 gramos, kilogramos o newtons? Una **magnitud física** es algo que podemos cuantificar; la **unidad** dice con qué referencia lo expresamos.

| Magnitud | Significado | Unidad usada |
|---|---|---|
| Tiempo | Cuánto transcurre | Segundo, s |
| Longitud | Distancia o dimensión | Metro, m |
| Masa | Medida de inercia traslacional | Kilogramo, kg |
| Velocidad | Cambio de posición por tiempo, con dirección | m/s |
| Aceleración | Cambio de velocidad por tiempo | m/s² |
| Fuerza | Interacción capaz de cambiar el movimiento | Newton, N |
| Momento de fuerza | Tendencia de una fuerza a producir giro | N·m |
| Presión y esfuerzo | Fuerza por unidad de área; distintos conceptos físicos | Pascal, Pa = N/m² |
| Densidad | Masa por volumen | kg/m³ |

Unidades frecuentes: `1 mm = 0.001 m`, `1 kPa = 1000 Pa`, `1 MPa = 1 000 000 Pa`, `1 GPa = 1 000 000 000 Pa`.

**Error típico:** escribir 1.5 cuando el campo espera un espesor en metros y se quería introducir 1.5 mm. La entrada correcta sería `0.0015`.

## 2. Cómo leer una fórmula sin asustarse

- `=` significa igualdad, no «causa» por sí sola.
- `Δ` significa cambio: valor final menos valor inicial.
- `Σ` significa sumar varios términos.
- `v²` significa `v × v`; `√x` es la raíz cuadrada.
- `|x|` es el valor absoluto; `‖v⃗‖` es la longitud o magnitud de un vector.
- `∝` significa «es proporcional a», manteniendo constantes las otras condiciones especificadas.
- `q(t)` significa que q depende del instante t.
- `σ(z,t)` depende tanto del lugar dentro del cohete como del instante.

Por ejemplo, si `q = 0.5 ρ v²`, duplicar v con ρ fija multiplica q por cuatro. Si al mismo tiempo la densidad baja a la mitad, q aumenta solamente por un factor de dos. **Nunca elimines la condición “manteniendo lo demás fijo”.**

## 3. Posición, velocidad y aceleración son distintas

La posición dice dónde está algo. La velocidad dice qué tan rápido cambia esa posición y hacia dónde. La aceleración dice cómo cambia la velocidad.

Para intervalos finitos:

$$
v_{\mathrm{media}} = \frac{\Delta x}{\Delta t}, \qquad
 a_{\mathrm{media}} = \frac{\Delta v}{\Delta t}.
$$

Si en 2 s un objeto pasa de 10 a 30 m/s, su aceleración media en ese intervalo es `(30 − 10)/2 = 10 m/s²`. Eso no significa que su velocidad sea 10 m/s.

Una gráfica de altura puede seguir subiendo mientras la velocidad vertical disminuye. La pendiente de la altura representa la velocidad vertical. Una curva menos inclinada indica que sube más lentamente.

### Apogeo y fin de combustión

- **Fin de combustión o burnout:** el motor deja de producir empuje en el modelo.
- **Apogeo:** punto de mayor altura de la trayectoria, donde la componente vertical de velocidad pasa por cero.

No coinciden necesariamente. Después del burnout el cohete puede seguir subiendo por su velocidad acumulada, mientras gravedad y aerodinámica cambian su movimiento.

En el apogeo **no tienen que ser cero** la velocidad horizontal, la velocidad relativa al viento ni la presión dinámica. Tampoco tiene que desaparecer la aceleración.

## 4. Escalares y vectores

La masa es un escalar: basta un número y una unidad. La velocidad y la fuerza son vectores: además importan sus componentes y dirección.

Un vector `v = (vx, vy, vz)` puede tener rapidez:

$$
V = \sqrt{v_x^2 + v_y^2 + v_z^2}.
$$

Ejemplo: componentes perpendiculares de 3 y 4 m/s dan una rapidez de 5 m/s, no 7. Sumar magnitudes no sustituye sumar vectores.

El código usa ambos tipos de cantidades: componentes con signo para calcular fuerzas y giros, y magnitudes para algunas gráficas. Un gráfico de magnitud pierde información sobre la dirección.

## 5. Dos sistemas de coordenadas y dos clases de altura

### Coordenadas del entorno

RocketPy usa ejes horizontales y un eje vertical positivo hacia arriba. `flight.z(t)` es una altitud usada para consultar la atmósfera.

- **ASL:** altitud sobre el nivel del mar.
- **AGL:** altura sobre el terreno de referencia del lanzamiento.

En esta demo, el sitio está a 1400 m ASL:

$$
h_{\mathrm{AGL}} = h_{\mathrm{ASL}} - 1400\ \mathrm{m}.
$$

Por eso un apogeo de aproximadamente 4687 m ASL corresponde a 3287 m AGL. Usar 3287 como altitud atmosférica consultaría condiciones del aire a una cota equivocada.

### Coordenadas del cuerpo

Para situar motor, nariz, masas y cortes se usa un eje axial solidario al cohete, positivo hacia la nariz. La cola del dominio está en `−1.255 m` y la punta en `+1.278 m`. El cero es una referencia del modelo, **no el nivel del mar ni el suelo**.

A medida que el cohete se inclina, su eje axial deja de coincidir con la vertical. Una fuerza lateral en ejes del cuerpo no se puede sumar directamente a una componente vertical terrestre sin transformar coordenadas.

La matriz de rotación y los cuaterniones del código sirven para traducir entre esos sistemas. No hace falta dominarlos para redactar, pero sí saber para qué están.

## 6. Masa no es peso

La masa se expresa en kg. El peso es la fuerza gravitatoria, aproximadamente:

$$
W = m g.
$$

Para un ejemplo de 20 kg y `g = 9.81 m/s²`, el peso sería 196.2 N. La masa no se vuelve 196.2 kg.

El cohete pierde masa al consumir propelente. También cambia dónde se concentra esa masa. El programa necesita actualizar ambas cosas, no solo borrar un porcentaje del peso al final.

**Carga útil añadida de 0 kg** significa que no añadimos masa al ejemplo de referencia. No significa que el vehículo entero no tenga masa o que se haya identificado toda su carga útil original.

## 7. Las leyes de Newton y las fuerzas principales

Para un sistema de masa constante visto desde un marco inercial:

$$
\sum \vec F_{\mathrm{externas}} = m\vec a.
$$

La fuerza **neta** es la suma vectorial de las fuerzas externas. Más fuerza neta sobre la misma masa implica mayor aceleración; más masa bajo la misma fuerza neta implica menor aceleración. Referencia: [OpenStax, F1](08-glosario-y-referencias.md#fuentes).

En un cohete intervienen:

- **Empuje:** intercambio de cantidad de movimiento con los gases expulsados, representado aquí mediante el motor y su curva de empuje. No necesita «empujar contra el aire».
- **Gravedad:** contribuye al peso.
- **Aerodinámica:** fuerzas del aire sobre el vehículo.
- **Reacciones del riel:** mientras está guiado; el módulo estructural actual no las reconstruye.

Para explicar un ascenso vertical idealizado puede escribirse `m a ≈ T − D − m g`, suponiendo que el empuje ya representa correctamente el efecto de la expulsión y que las direcciones son las indicadas. **No es la ecuación completa de vuelo 6-DOF ni una fórmula de la carga axial interna.**

El cohete real es un sistema de masa variable. La dinámica de RocketPy considera ese problema con mayor detalle; no se obtiene simplemente aplicando todas las fórmulas de un bloque de masa constante a un cohete sin revisar sus supuestos.

### ¿Qué son 6 grados de libertad?

Tres movimientos de traslación y tres de rotación. La orientación influye en qué aire encuentra cada superficie y en hacia dónde actúan las fuerzas. El modelo de vuelo y el modelo estructural de este proyecto tienen distinto nivel de detalle.

## 8. La velocidad que “siente” el aire

La aerodinámica depende del movimiento **relativo** entre cohete y aire:

$$
\vec v_{\mathrm{rel}} = \vec v_{\mathrm{cohete}} - \vec v_{\mathrm{aire}},
\qquad V_{\mathrm{rel}} = \|\vec v_{\mathrm{rel}}\|.
$$

Si el cohete avanza a 100 m/s en una dirección y el viento sopla a 10 m/s en la misma dirección, la rapidez relativa sería 90 m/s. Si el viento es perpendicular, se combinan componentes: no se restan 10 m/s a la rapidez directamente.

El código puede usar el vector opuesto, aire menos cohete, para describir el flujo incidente. Ambos tienen la misma magnitud, pero sus direcciones y convenciones de ángulo deben mantenerse consistentes.

Además, un punto alejado del centro de giro tiene velocidad local por la rotación. Por eso nariz y aletas no ven necesariamente el mismo flujo. `get_point_loads` incluye ese efecto al consultar fuerzas por superficie.

## 9. Atmósfera: densidad, presión y temperatura

- **Densidad ρ:** masa de aire en un volumen.
- **Presión estática p:** propiedad termodinámica local del aire.
- **Temperatura:** influye, entre otras cosas, en la velocidad del sonido.

En la atmósfera estándar del ejemplo la densidad disminuye con la altitud. No es un pronóstico para un día real ni contiene ráfagas. El viento transversal de cada escenario es constante.

## 10. Presión dinámica y Max-Q

La presión dinámica se define como:

$$
q = \frac12\rho V_{\mathrm{rel}}^2.
$$

Ejemplo: `ρ = 1 kg/m³` y `Vrel = 100 m/s` dan `q = 5000 Pa = 5 kPa`. A 200 m/s, con igual densidad, q sería 20 kPa.

**Max-Q** es el máximo de q a lo largo del intervalo de vuelo considerado. Al principio aumenta la velocidad; a mayor altitud suele disminuir la densidad. El máximo depende de la combinación, no solo del máximo de velocidad.

q tiene unidades de presión, pero **no es la presión real uniforme sobre toda la piel**, ni la fuerza total, ni un esfuerzo del material. Se usa para expresar la escala de las fuerzas aerodinámicas. Fuente: [NASA, F3](08-glosario-y-referencias.md#fuentes).

## 11. Arrastre, coeficientes y área de referencia

Una representación habitual del arrastre es:

$$
D = q C_D A_{\mathrm{ref}}.
$$

- D: fuerza de arrastre en N.
- Cd: coeficiente adimensional; recoge dependencias aerodinámicas.
- Aref: área de referencia compatible con la definición del coeficiente.

Para `q = 5000 Pa`, `Cd = 0.4` y `Aref = 0.01 m²`, D sería 20 N. No se puede sustituir Aref por cualquier área sin cambiar la definición de Cd.

El **área frontal aerodinámica** no es el **área de material del tubo** usada para esfuerzos. Ambas se expresan en m², pero representan cosas diferentes.

Cd puede variar con Mach, geometría y otras condiciones. Esta demo lee curvas de Cd del ejemplo de RocketPy. Cambiar aletas no regenera esas curvas. Fuente de la relación: [NASA, F4](08-glosario-y-referencias.md#fuentes).

## 12. Ángulo de ataque, fuerzas normales y Mach

El **ángulo de ataque α** representa la desalineación del eje del vehículo respecto al flujo incidente, según la convención utilizada. No es simplemente la inclinación del riel respecto al suelo.

Como intuición de ángulos pequeños, una fuerza normal puede escalar como `q Aref Cα α`. Pero el adaptador llama al cálculo de fuerzas de cada superficie de RocketPy con el flujo local; no usa exclusivamente un único α global. Si se usa la fórmula lineal, α debe estar en radianes cuando el coeficiente está definido por radián.

El **número de Mach** es:

$$
\mathrm{Ma} = \frac{V_{\mathrm{rel}}}{a_s},
$$

donde `a_s` es la velocidad local del sonido. No es la aceleración. Mach 1 significa que ambas velocidades tienen igual magnitud.

El límite Mach 1.5 configurado es un criterio de alcance del estudio. Estar debajo de ese valor no valida automáticamente todos sus modelos.

## 13. Centro de masa, centro de presión y estabilidad

El **centro de masa** es una posición media ponderada por masas:

$$
z_{\mathrm{CG}} = \frac{\sum_i m_i z_i}{\sum_i m_i}.
$$

No requiere que haya igual masa a cada lado: importan también las distancias. Puede desplazarse al añadir carga útil o quemar propelente.

El **centro de presión** es una localización equivalente de la acción aerodinámica bajo una definición y condición de flujo. No es necesariamente el centro geométrico de la silueta y puede depender de Mach.

En la convención positiva hacia la nariz del modelo, el margen estático se expresa como la distancia de CG por delante de CP dividida por el diámetro. «Dos calibres» significa dos diámetros de separación, no dos metros.

Una perturbación pequeña puede producir un momento que tienda a restaurar la orientación si la disposición es apropiada. Esa es la intuición de estabilidad estática de un cohete con aletas [F5]. No garantiza buena estabilidad dinámica, amortiguamiento, trayectoria deseada o resistencia estructural.

El umbral de un calibre de esta demo es una elección de cribado. No debe presentarse como una norma universal de lanzamiento.

## 14. Relaciones que puedes defender, con sus condiciones

| Cambio | Relación directa | Lo que no se deduce automáticamente |
|---|---|---|
| Duplicar Vrel con ρ fija | q se multiplica por 4 | Que el esfuerzo máximo de toda la estructura se multiplique por 4 |
| Aumentar Cd con q y Aref fijas | Aumenta D | La nueva trayectoria completa; hay que resolverla |
| Añadir masa bajo igual fuerza neta | Disminuye la aceleración instantánea | Que todo cohete alcance siempre menos altura; también cambian otras relaciones |
| Cambiar posición de carga útil | Cambia CG y puede cambiar inercia | Un resultado universal de estabilidad sin recalcular |
| Aumentar la altitud | En el perfil usado disminuye ρ | Que q siempre disminuya mientras se asciende |
| Llegar al apogeo | La velocidad vertical pasa por cero | Que no haya movimiento horizontal ni cargas |

**Siguiente paso:** explica por qué un cohete puede seguir ganando altura después de que su motor se apaga y por qué Max-Q no es, por definición, el máximo esfuerzo estructural. Después pasa a los cortes internos del capítulo 02.
