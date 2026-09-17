# 02 · Estructuras y flutter: de la fuerza externa al esfuerzo interno

[Índice](../README.md) · [Anterior: vuelo](01-fisica-desde-cero.md) · [Siguiente: programación](03-programacion-desde-cero.md)

Fuentes de fundamentos: [F2, F6 y F7](08-glosario-y-referencias.md#fuentes). Las simplificaciones descritas son las de [structural_loads.py](../structural_loads.py) y [flutter.py](../flutter.py), no propiedades verificadas de un cohete real.

## 1. “Carga estructural” no es una sola magnitud

En conversación se habla de «la carga» como si fuera un número. Para calcular y redactar hay que distinguir:

| Concepto | Ejemplo intuitivo | Unidad |
|---|---|---|
| Fuerza externa | El motor empuja la estructura | N |
| Carga axial interna N | Una sección transmite compresión o tracción a la siguiente | N |
| Cortante interno V | Partes contiguas tienden a deslizarse transversalmente | N |
| Momento flector M | La carga tiende a curvar el cuerpo | N·m |
| Esfuerzo normal σ | Intensidad local de fuerza interna por área | Pa |
| Deformación | Cambio de forma o tamaño | m para desplazamientos; sin unidad para deformación relativa |

N se usa tanto como símbolo de la carga axial como abreviatura de la unidad newton. El contexto importa. V puede designar rapidez en aerodinámica y cortante en estructuras; esta guía usa Vrel para la primera cuando puede haber confusión.

## 2. Por qué mirar el cohete entero no basta

Imagina dos bloques unidos: uno de 3 kg delante y otro de 2 kg detrás. Empujamos el bloque trasero con 100 N, sin rozamiento ni gravedad en la dirección del movimiento.

La aceleración conjunta es `100/(3+2) = 20 m/s²`. Pero la unión no transmite 100 N al bloque delantero: transmite `3 × 20 = 60 N`, suficientes para acelerarlo. El resto de la fuerza acelera el bloque trasero.

**Conclusión:** conocer la fuerza neta del conjunto no determina, por sí sola, la fuerza interna en cada unión. Hay que saber cómo se distribuyen las masas y las fuerzas.

Un **corte imaginario** divide el objeto. Al aislar una parte aparecen fuerzas internas en el corte que antes se cancelaban al estudiar el conjunto completo. Esa es la idea detrás de los diagramas por sección.

En el módulo, `axial_force(flight,t)` no ofrece una fuerza única: rechaza esa formulación. La cantidad que interesa es `N(z,t)`.

## 3. Momento de fuerza: la analogía de una puerta

Abrir una puerta empujando cerca de la bisagra cuesta más que empujar lejos, para la misma fuerza y orientación. El efecto de giro depende del brazo perpendicular:

$$
M = F d_\perp.
$$

Una fuerza perpendicular de 10 N aplicada a 0.5 m produce 5 N·m. En tres dimensiones se escribe `M⃗ = r⃗ × F⃗`; el producto vectorial conserva la dirección de giro y el brazo efectivo.

Por eso no basta con sumar las magnitudes de las fuerzas de nariz y aletas: sus posiciones y signos afectan el momento. «Momento flector máximo» no significa «instante máximo»; momento es aquí una magnitud mecánica.

## 4. Viga libre, no una regla empotrada

Una regla fijada a una mesa puede transmitir fuerzas y momentos a su soporte. Un cohete después de dejar el riel no tiene ese apoyo: se traslada y gira por las fuerzas externas.

El modelo usa **alivio inercial** para reconstruir cargas internas compatibles con ese movimiento. No añade un soporte ficticio a la cola.

### Idea traslacional

Si las fuerzas externas suman F, una distribución de masa total m tiene aceleración específica de alivio `a = F/m`. Se añaden al cálculo fuerzas inerciales equivalentes `−mi a` en las posiciones de las masas.

Así, las cargas efectivas satisfacen:

$$
\sum \vec F_{\mathrm{externas}} + \sum_i(-m_i\vec a)=0.
$$

Esto es una herramienta de cálculo; no significa que las fuerzas externas reales sean cero.

### También hay que equilibrar el giro

Si queda un momento neto, cancelar solo la fuerza no basta. El módulo calcula una aceleración angular de alivio a partir del momento alrededor del CG y la inercia transversal equivalente. A cada masa se le asocia además la aceleración `α⃗ang × r⃗i`.

De forma resumida:

$$
\vec f_{i,\mathrm{inercial}}=-m_i\left(\vec a+\vec\alpha_{\mathrm{ang}}\times\vec r_i\right).
$$

Las cargas efectivas resultantes deben cerrar tanto fuerza como momento. El programa comprueba los residuos y luego suma las fuerzas y sus brazos situados al lado de la nariz de cada corte.

**Límite:** estas aceleraciones son las de la reconstrucción cuasiestática del módulo. No se leen como una recuperación exacta de todas las aceleraciones y términos de RocketPy. Se omiten giroscopía, centrífugas, modos flexibles y flujo de momento del propelente.

### ¿Por qué no se añade simplemente otro m·g?

La gravedad aproximadamente uniforme acelera a todas las partes por igual. En caída libre ideal esa aceleración cancela su contribución al alivio inercial. Un objeto flotando en caída libre no soporta internamente su peso como si estuviera sobre una mesa.

RocketPy **sí incluye gravedad en el vuelo**. Lo incorrecto sería usar siempre `empuje − arrastre − peso` como compresión interna de todo el tubo. Con apoyos o gravedad no uniforme habría que revisar el tratamiento.

## 5. Qué es una distribución de masa equivalente

El ejemplo aporta masa, centro de masa e inercia agregados, pero no identifica cada batería, unión o soporte. Distintas distribuciones internas pueden compartir esos mismos valores y producir cargas locales diferentes.

El proyecto construye nodos con masas positivas:

- Una distribución equivalente de la parte seca que reproduce las propiedades agregadas de referencia.
- Masas de aletas y de carga útil añadida en posiciones explícitas.
- Una distribución equivalente del motor que cambia durante la combustión y queda dentro de sus límites axiales.

La cuadratura numérica coloca nodos y pesos para reproducir integrales. **Un nodo no es una pieza descubierta del cohete.** Aumentar el número de nodos refina la representación matemática de los mismos supuestos; no aporta datos experimentales nuevos.

La distribución del motor utiliza una familia beta acotada. Se eligen sus parámetros para reproducir masa, CG e inercia transversal. No se está afirmando que el propelente físico tenga una distribución beta.

## 6. Dos inercias distintas que comparten la letra I

### Inercia de masa: kg·m²

Mide la resistencia a cambiar el movimiento de rotación. Para masas puntuales respecto a un eje:

$$
I_{\mathrm{masa}} = \sum_i m_i r_{\perp,i}^2.
$$

Importa al calcular cómo gira el vehículo y en el alivio angular. El modelo axial usa distancias al CG para representar la inercia transversal.

### Segundo momento de área: m⁴

Describe cómo se distribuye el área de material en una sección. Importa en flexión. Para un tubo circular de radio exterior ro e interior ri:

$$
A_{\mathrm{material}} = \pi(r_o^2-r_i^2),
\qquad
I_A = \frac{\pi}{4}(r_o^4-r_i^4).
$$

No se mide en kg·m² y no se puede reemplazar por la inercia de masa de RocketPy. La diferencia de unidades permite detectar esa confusión.

## 7. Fuerza, esfuerzo, rigidez y resistencia

### Esfuerzo axial

Una fuerza axial distribuida de forma uniforme sobre una sección ideal produce:

$$
\sigma_{\mathrm{axial}} = \frac{N}{A_{\mathrm{material}}}.
$$

Por ejemplo, 1000 N sobre `0.001 m²` producen 1 MPa. La misma fuerza sobre la mitad de esa área produce 2 MPa.

### Esfuerzo de flexión

Bajo las hipótesis de viga elástica apropiadas, el esfuerzo longitudinal varía con la distancia al eje neutro:

$$
|\sigma_{\mathrm{flexion}}|_{\mathrm{extremo}} = \frac{|M|r_o}{I_A}.
$$

Una cara tiende a comprimirse y la opuesta a traccionarse. El módulo combina las dos componentes de flexión mediante `|M| = √(Mx²+My²)`, adecuado a su sección circular equivalente.

### Esfuerzo combinado usado

El máximo valor absoluto longitudinal en la sección ideal es:

$$
\sigma_{\mathrm{max,seccion}}(z,t)
=\frac{|N(z,t)|}{A_{\mathrm{material}}}
+\frac{\sqrt{M_x(z,t)^2+M_y(z,t)^2}\,r_o}{I_A}.
$$

Después se busca el máximo entre secciones e instantes. No se suman, por ejemplo, una carga axial máxima de un lugar con un momento máximo de otro como si hubieran ocurrido juntos.

**No es un esfuerzo equivalente de von Mises completo.** No incorpora esfuerzo cortante, torsión, concentraciones locales o fallo de uniones. El cortante se grafica, pero no se introduce en esta expresión de esfuerzo normal.

### Rigidez no significa resistencia

- E, módulo de Young: relaciona esfuerzo normal y deformación longitudinal en el régimen elástico lineal.
- G, módulo de corte: relaciona esfuerzo cortante y deformación angular en el régimen correspondiente.
- Fluencia: comienzo de deformación plástica según un criterio y un material.
- Pandeo: pérdida de estabilidad de una estructura comprimida, posible antes de alcanzar la fluencia.

Una regla delgada puede pandear antes de que su material «se aplaste». Comparar únicamente con fluencia no cubre ese fallo.

En este código E y G del **tubo** se almacenan, pero no resuelven deformaciones ni aparecen en la expresión de esfuerzo anterior. `yield_strength` solo aparece en la comparación auxiliar del script 02; **no define automáticamente el umbral de selección**. El G de las **aletas**, en cambio, sí entra en flutter. Véase [el mapa de parámetros](04-codigo-y-datos.md).

## 8. Por qué la demo da casi el mismo esfuerzo máximo para muchos diseños

Este es uno de los resultados más importantes para interpretar honestamente el prototipo:

1. El motor es el mismo en todos los casos del barrido.
2. El empuje se aplica en la estación trasera.
3. Justo delante de esa aplicación, la sección transmite esencialmente el empuje al resto del modelo.
4. La sección tubular de comparación también es la misma.
5. En los casos calculados, esa compresión domina el máximo global, mientras la flexión es relativamente pequeña.

A 1 s el empuje usado es aproximadamente 2034 N. Con `ro = 0.0635 m` y espesor `0.0015 m`, el área de material es aproximadamente `5.91405 × 10⁻⁴ m²`. La razón `2034/A` es aproximadamente **3.439 MPa**, el máximo repetido en la malla.

Eso **no prueba** que cambiar la masa no afecte las cargas: cambian la aceleración, los diagramas y otras secciones. Muestra que el máximo de esta representación está dominado por una condición común. Tampoco es una validación del soporte real del motor: su camino de carga no está modelado en detalle.

## 9. Vibración, resonancia y flutter no son sinónimos

- **Vibración:** oscilación alrededor de una configuración.
- **Frecuencia natural:** frecuencia propia de un modo, determinada por masa, rigidez y condiciones de apoyo.
- **Resonancia forzada:** respuesta elevada ante una excitación próxima a una frecuencia relevante, dependiendo también del amortiguamiento.
- **Flutter:** inestabilidad aeroelástica en la que el flujo y la deformación se acoplan y pueden alimentar una oscilación.

Como intuición, un sistema simple masa–resorte tiene frecuencia natural proporcional a `√(rigidez/masa)`. Esa relación **no es el cálculo de flutter implementado** ni permite hallar por sí sola cuándo se rompe una aleta.

El módulo no anima vibraciones, no calcula frecuencias modales ni predice cuándo se desprende una aleta. Calcula una frontera empírica de velocidad y la compara con el vuelo.

## 10. Geometría de la aleta y fórmula utilizada

Para una aleta trapezoidal:

- cr: cuerda raíz, longitud de la aleta junto al cuerpo.
- ct: cuerda punta.
- b: envergadura expuesta desde el cuerpo hasta la punta.
- s: barrido, desplazamiento axial del borde delantero de la punta respecto a la raíz.
- δ: espesor constante de la aleta; se usa δ para no confundirlo con el tiempo t.
- S: área de una aleta, `(cr+ct)b/2`.
- AR: relación de aspecto, `b²/S`.
- λ: estrechamiento, `ct/cr`.

El centroide axial Cx del trapecio homogéneo usado es:

$$
C_x=\frac{c_r^2+c_rc_t+c_t^2+s(c_r+2c_t)}{3(c_r+c_t)},
\qquad \epsilon=\frac{C_x}{c_r}-\frac14.
$$

La versión implementada requiere ε positivo y utiliza la revisión de Bennett [F7]:

$$
V_f = a_s\sqrt{
\frac{G(AR+2)(\delta/c_r)^3}
{(24\epsilon\gamma/\pi)\,p\,AR^3(1+\lambda)/2}
},\qquad \gamma=1.4.
$$

G y p deben estar en las mismas unidades de presión. El código usa Pa; as y Vf están en m/s. La constante incluye la corrección que evita la sobreestimación por √2 discutida en esa referencia. Una prueba reproduce aproximadamente su ejemplo de 1425 ft/s.

No se debe presentar esta fórmula como válida para cualquier laminado, unión, geometría o régimen de Mach. El criterio Mach de la demo no comprueba automáticamente todas las hipótesis de la fórmula, ni valida una frontera nominal que caiga fuera de su rango de aplicación.

## 11. Relaciones de flutter, siempre con condiciones

Manteniendo la geometría restante y el estado atmosférico:

- `Vf ∝ √G`: multiplicar G por 4 multiplica Vf por 2.
- `Vf ∝ δ^(3/2)`: duplicar espesor multiplica Vf por aproximadamente 2.828.
- Con as fija, `Vf ∝ 1/√p`.
- Aumentar todas las dimensiones del plano de la aleta por un factor k, **sin aumentar su espesor**, conserva AR, λ y ε, pero reduce δ/cr. Entonces Vf escala como `k^(−3/2)` a igual atmósfera.

Eso explica por qué «aletas más grandes» no significa automáticamente «mejor resistencia al flutter». También cambia el vuelo y la masa; el margen final exige recalcular la trayectoria.

El cociente graficado es:

$$
R_f(t)=\frac{V_f(t)}{V_{\mathrm{rel}}(t)}.
$$

- `Rf > 1`: velocidad calculada por debajo de la frontera nominal.
- `Rf = 1`: coincidencia con la frontera.
- `Rf < 1`: cruce de la frontera; riesgo según la aproximación.

El umbral de estudio predeterminado es 1.25, una reserva elegida para comparar, **no un requisito de seguridad validado**. Un Rf de 0.51 no significa 51% de probabilidad de fallo.

## 12. Relación especial entre flutter y Max-Q en este modelo

Con geometría y G constantes y aire ideal coherente, `as² = γ p/ρ`. Si llamamos B al factor geométrico adimensional de la fórmula, se tiene:

$$
V_f^2 = a_s^2\frac{G B}{p} = \frac{\gamma G B}{\rho},
\qquad
R_f^2 = \frac{\gamma G B}{\rho V_{\mathrm{rel}}^2}
=\frac{\gamma G B}{2q}.
$$

B es `(AR+2)(δ/cr)³ / [(24 ε γ/π) AR³(1+λ)/2]`. Por tanto, bajo esas hipótesis, minimizar el margen equivale a maximizar q. Pequeñas diferencias de tiempo pueden deberse al muestreo y a las interpolaciones de las funciones del programa.

**No es un descubrimiento independiente si las dos curvas coinciden:** en esta aproximación existe esa relación matemática. Tampoco significa que Max-Q determine todos los fenómenos de flutter de una estructura flexible real. La afirmación general de que el instante de flutter «siempre es diferente de Max-Q» sería incorrecta aquí.

**Siguiente paso:** explica por separado por qué el máximo esfuerzo global casi no cambia entre los diseños actuales y por qué las aletas delgadas reducen fuertemente su margen de flutter. Son mecanismos y métricas diferentes.
