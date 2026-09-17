# 05 · Las siete gráficas, explicadas con su física

[Índice](../README.md) · [Anterior: código y datos](04-codigo-y-datos.md) ·
[Siguiente: metodología](06-metodologia-y-redaccion.md)

Todas las imágenes salen de `outputs/` con la configuración congelada de
`demo.json`. El **caso base** es: carga útil 0 kg, escala de aleta 1,
espesor 3 mm de aluminio 6061 (\(G = 26\) GPa), viento 4 m/s. El intervalo
graficado va desde que el cohete abandona el riel (0.37 s) hasta el apogeo
(25.8 s). El sitio de lanzamiento está a 1400 m sobre el nivel del mar, por
eso conviven dos alturas: **AGL** (sobre el suelo) y **ASL** (sobre el mar).

Cada sección sigue el mismo orden: qué se dibuja, qué física hay detrás,
cómo leerla, qué cifras salen de ella y qué **no** se puede concluir.

## Antes de empezar: las tres cantidades que se repiten

- **Rapidez relativa al aire \(V\)**: lo que “siente” la aleta. Es la rapidez
  del cohete respecto al suelo combinada con el viento
  (\(v_{\mathrm{rel}} = v_{\mathrm{cohete}} - v_{\mathrm{aire}}\) como vectores, capítulo 01).
- **Velocidad de flutter \(V_f\)**: la rapidez del aire a la que, según la
  fórmula de Bennett (capítulo 02), la aleta entraría en flutter. Depende de
  la aleta (\(G\), espesor, geometría) y de la atmósfera local (presión \(p\)
  y velocidad del sonido \(a_s\)); **no** depende de cuánto corra el cohete.
- **Ratio \(R_f = V_f/V\)**: cuántas veces más rápido tendría que ir el aire
  para llegar al flutter. \(R_f>1\) es zona segura según el modelo; la demo
  exige \(R_f \ge 1.25\) como margen.

La pregunta de todo el estudio es: *¿en qué instante del vuelo se acercan más
\(V\) y \(V_f\), y cuánto margen queda ahí?*

## Figura 01 · `01-flight.png` — el vuelo que alimenta todo lo demás

![Figura 01: vuelo base](../outputs/01-flight.png)

**Qué se dibuja.** Cuatro paneles contra el tiempo desde la ignición.
Arriba izquierda: altura AGL. Arriba derecha: rapidez respecto al aire (línea
continua) y respecto al suelo (discontinua). Abajo izquierda: presión
dinámica \(q\) con la línea de Max‑Q. Abajo derecha: margen estático en
calibres con su límite de 1.

**La física detrás.**

- *Altura.* Mientras el empuje supera al peso más el arrastre la curva se
  dobla hacia arriba (aceleración positiva). Eso termina a 3.38 s, un poco
  antes del burnout (3.9 s), porque el empuje del motor decae en su cola.
  Después solo actúan la gravedad y el arrastre, ambas frenando: la curva se
  va aplanando hasta el apogeo, donde la velocidad vertical es cero. Es la cinemática de MRUA que ya conoces, pero
  con una aceleración que cambia en el tiempo.
- *Velocidades.* La rapidez sube casi en línea recta mientras hay empuje y
  alcanza 285.8 m/s respecto al suelo (286.1 m/s respecto al aire) a
  3.38 s. La caída posterior es más lenta que la subida porque, sin empuje,
  la desaceleración es \(g + D/m\) y el arrastre \(D\) disminuye conforme el
  cohete frena. Las dos curvas casi se superponen porque el viento (4 m/s) es
  pequeño frente a la rapidez del cohete: el viento importa para el ángulo de
  ataque, no para la magnitud de \(V\).
- *Presión dinámica.* \(q = \rho V^2/2\). Crece con el cuadrado de la
  velocidad y decrece con la densidad, que baja con la altura. El máximo
  (**Max‑Q = 41.6 kPa a 3.34 s**) ocurre unas décimas antes de la velocidad
  máxima: el cohete todavía acelera, pero ya subió lo suficiente para que la
  pérdida de \(\rho\) empiece a pesar más que la ganancia de \(V^2\).
- *Margen estático.* Distancia entre centro de presión y centro de masa en
  diámetros del cuerpo. Sube durante la combustión porque el propelente (que
  está atrás) se consume y el CG avanza hacia la nariz. Nunca baja de 1, así
  que el cohete es estable en todo el tramo.

**Cómo leerla.** Localiza las tres marcas temporales que reaparecen en las
demás figuras: burnout (3.9 s), Max‑Q (3.34 s) y velocidad máxima (3.38 s).
Nota que las tres se apretujan en menos de un segundo: el tramo crítico para
las aletas es muy corto.

**Cifras que salen de aquí.** Apogeo 3287.3 m AGL (4687.3 m ASL); \(V\)
máxima 286.1 m/s; Max‑Q 41.60 kPa; Mach máximo 0.86; margen mínimo 2.28
calibres al salir del riel.

**No concluir.** Que el cohete “vuela recto”: la figura no muestra
trayectoria horizontal ni orientación. Tampoco que \(q\) sea una propiedad de
la aleta; es una propiedad del flujo que la aleta ve.

## Figura 02 · `02-flutter-history.png` — la gráfica central del proyecto

![Figura 02: historia de flutter](../outputs/02-flutter-history.png)

**Qué se dibuja.** Tres paneles con el mismo eje de tiempo. Arriba: \(V_f\)
(verde) y \(V\) relativa (azul) en m/s, con las líneas verticales de burnout,
Max‑Q y velocidad máxima. Centro: el ratio \(V_f/V\), la línea horizontal del
límite 1.25 y un punto en el mínimo. Abajo: presión estática \(p\) (kPa, eje
izquierdo) y velocidad del sonido \(a_s\) (m/s, eje derecho).

**La física detrás.**

- *Por qué \(V_f\) es casi horizontal.* La aleta no cambia durante el vuelo;
  lo único que varía en la fórmula es la atmósfera. Con \(V_f \propto a_s/\sqrt{p}\),
  al subir 3.3 km la presión baja de 85.6 kPa a 56.3 kPa y \(a_s\) baja de
  334.5 a 321.1 m/s. El efecto neto es que \(V_f\) **sube** de 569 m/s en el
  riel a 673 m/s en el apogeo: el aire enrarecido tiene menos capacidad de
  “empujar” la aleta hacia la inestabilidad.
- *Por qué el ratio tiene forma de “U” asimétrica.* Al salir del riel \(V\) es
  pequeña (26 m/s) y \(R_f = 21.5\), enorme. Conforme el motor acelera, \(V\)
  crece y el ratio se desploma. Después del burnout \(V\) decae y \(V_f\) sube,
  así que el ratio vuelve a crecer hasta 25.6 en el apogeo. El mínimo es la
  única zona que importa.
- *Por qué el mínimo coincide con Max‑Q y no exactamente con la velocidad
  máxima.* Sustituyendo \(a_s^2=\gamma p/\rho\) en la fórmula (capítulo 02,
  §9) se obtiene \(R_f^2 = \gamma G B/(\rho V^2) = \gamma G B/(2q)\),
  con \(B\) un factor puramente geométrico. Para una aleta dada, **minimizar
  \(R_f\) es exactamente maximizar \(q\)**. Por eso el mínimo (2.0382) cae a
  3.341 s, el instante de Max‑Q, y el ratio en la velocidad máxima (3.384 s)
  es apenas mayor: 2.0388.
- *Panel inferior.* Muestra las dos entradas atmosféricas de la fórmula. Ambas
  bajan con la altura; el descenso de \(p\) domina porque entra como
  \(p^{-1/2}\) y cae un 34 %, mientras que \(a_s\) cae solo un 4 %.

**Cómo leerla.** Primero mira el panel central: ¿la curva toca la línea
1.25? En el caso base no: el mínimo es **2.04**, así que hay 63 % de margen
sobre el límite y el doble de margen sobre el flutter nominal. Luego sube al
panel superior y comprueba la distancia vertical entre las dos curvas en el
instante de Max‑Q: 583 m/s frente a 286 m/s.

**Cifras que salen de aquí.** Mínimo \(R_f = 2.0382\) a 3.341 s y 1898 m
ASL; \(V_f\) en ese instante 583.0 m/s; \(V\) en ese instante 286.0 m/s.

**No concluir.** Que “la aleta vibra a 583 m/s”: \(V_f\) es una frontera
nominal empírica, no una medición. Ni que un ratio de 2 signifique “doble de
seguro” en sentido probabilístico: el modelo no tiene incertidumbre asociada.

## Figura 03 · `03-altitude.png` — separar la aleta de la atmósfera

![Figura 03: altitud y atmósfera](../outputs/03-altitude.png)

**Qué se dibuja.** El eje vertical es altitud ASL de 0 a 10 km, no tiempo.
Izquierda: \(V_f\) que tendría la aleta base (3 mm) y la aleta delgada
(1.2 mm) si el aire local fuese el de esa altitud. Derecha: presión,
densidad y velocidad del sonido del modelo atmosférico, divididas por su
valor al nivel del mar. La banda sombreada es el tramo que el vuelo base
recorre realmente (1.4 km a 4.7 km ASL).

**La física detrás.**

- *Atmósfera.* En la troposfera la temperatura baja unos 6.5 K por km, y
  presión y densidad caen aproximadamente de forma exponencial. La velocidad
  del sonido depende solo de la temperatura (\(a_s = \sqrt{\gamma R T}\)), por
  eso su curva es casi una recta suave y cae poco (12 % en 10 km), mientras
  \(p\) pierde el 74 % y \(\rho\) el 66 %.
- *\(V_f\) frente a altitud.* Es la misma fórmula evaluada a cada altura con
  la aleta fija. Crece porque \(1/\sqrt{p}\) crece más rápido de lo que
  \(a_s\) decrece. La curva de la aleta delgada tiene la misma forma pero
  está desplazada hacia la izquierda por el factor \((1.2/3)^{3/2} = 0.253\):
  \(V_f\) escala con \((t/c_r)^{3/2}\), y ese exponente 3/2 es la razón de que
  el espesor sea la variable más poderosa del diseño.

**Cómo leerla.** Sirve para responder “¿y si lanzamos desde otro sitio?”.
Un lanzamiento a nivel del mar tendría \(V_f = 530\) m/s en el riel en lugar
de 569 m/s: algo menos de margen. La banda sombreada recuerda que el resto de
la curva es una extrapolación del modelo atmosférico, no parte del vuelo.

**No concluir.** Que el cohete llegue a 10 km, ni que \(R_f\) mejore con la
altura “automáticamente”: aquí solo se dibuja \(V_f\); la rapidez \(V\) del
cohete también cambia con la altura y no aparece en esta figura.

## Figura 04 · `04-thickness-sweep.png` — la variable de diseño que más pesa

![Figura 04: barrido de espesor](../outputs/04-thickness-sweep.png)

**Qué se dibuja.** Izquierda: ratio mínimo del vuelo frente a espesor de la
aleta (1 a 8 mm), una curva por material, la línea del límite 1.25 y una
línea vertical en el espesor base (3 mm). Derecha: barras con el espesor
mínimo que cada material necesita para cumplir exactamente \(R_f = 1.25\) en
la trayectoria base.

**La física detrás.**

- *Forma de las curvas.* Como \(V_f \propto t^{3/2}\) y \(V\) no cambia (el
  barrido reutiliza la trayectoria base), \(R_f\) mínimo \(\propto t^{3/2}\).
  Duplicar el espesor multiplica el margen por \(2^{1.5} = 2.83\). Por eso
  las curvas se curvan hacia arriba y no son rectas.
- *Separación entre materiales.* La única propiedad del material en la
  fórmula es \(G\) y entra como \(\sqrt{G}\). El aluminio (26 GPa) tiene 6.3
  veces la \(G\) del G10 (4.14 GPa), así que su curva está \(\sqrt{6.3}=2.5\)
  veces más alta a igual espesor. Para compensar una \(G\) menor hay que
  aumentar \(t\) según \(t \propto G^{-1/3}\): el G10 necesita
  \(6.3^{1/3} = 1.85\) veces el espesor del aluminio (4.00 mm frente a
  2.17 mm), justo lo que muestran las barras.
- *Barras.* Es la fórmula invertida (`required_thickness`, capítulo 02 §7)
  aplicada a todo el vuelo y tomando el peor instante, que es Max‑Q.

**Cómo leerla.** Busca dónde cada curva cruza la línea 1.25: ese cruce es el
mismo número que la barra del panel derecho. Luego mira dónde queda la línea
vertical del espesor base: el aluminio de 3 mm está claramente por encima
(2.04); con esos mismos 3 mm el G10 daría 0.81 y el contrachapado 0.33, es
decir, **por debajo de 1**: flutter nominal antes de Max‑Q.

**Cifras que salen de aquí.** Espesor requerido para \(R_f=1.25\): aluminio
6061 2.17 mm; carbono tejido 0/90 3.89 mm; G10 4.00 mm; acrílico/
policarbonato 6.42 mm; contrachapado de abedul 7.23 mm. Aluminio a 1 mm:
0.39; a 2 mm: 1.11; a 3 mm: 2.04.

**No concluir.** Que una aleta más gruesa sea “gratis”: el barrido es
algebraico, mantiene la masa y la trayectoria del caso base. Una aleta de
7 mm de madera pesa distinto, mueve el CG y baja el apogeo; eso solo lo
muestra una nueva simulación. El caso delgado sí se resimuló y la diferencia
con el estimado algebraico fue 1.0 %, lo que da confianza al barrido para
comparar, no para certificar. Tampoco concluir que “carbono es peor que
G10”: los valores de \(G\) son típicos y para un laminado dependen mucho de
la orientación de las fibras.

## Figura 05 · `05-geometry-map.png` — tamaño de aleta frente a espesor

![Figura 05: mapa geométrico](../outputs/05-geometry-map.png)

**Qué se dibuja.** Un mapa de color. Eje horizontal: espesor (1 a 8 mm). Eje
vertical: escala uniforme de la planta de la aleta (0.85, 1.0, 1.15). El
color es el ratio mínimo del vuelo; la línea blanca es la frontera
\(R_f = 1.25\). Cada fila usa la trayectoria simulada para esa escala
(carga útil y viento base) y recalcula \(V_f\) para cada espesor.

**La física detrás.**

- *Escalar la planta.* Multiplicar cuerda raíz, cuerda punta, envergadura y
  flecha por un factor \(k\) deja iguales el alargamiento AR, el
  estrechamiento \(\lambda\) y \(\epsilon\); lo único que cambia en la fórmula
  es \(t/c_r\), que se divide por \(k\). Por tanto
  \(V_f \propto k^{-3/2}\): una aleta 15 % más grande con el mismo espesor
  pierde un 19 % de \(V_f\). Físicamente: una placa más larga y ancha con el
  mismo grosor es más flexible a torsión.
- *Efecto sobre la trayectoria.* Aletas más grandes generan más arrastre y
  algo más de masa, así que \(V\) máxima baja un poco; ese efecto va en la
  dirección contraria pero es mucho menor que el de \(t/c_r\). El resultado
  neto para 3 mm es 2.59 (×0.85), 2.04 (×1.0) y 1.66 (×1.15).
- *Forma de la frontera.* Para mantener \(R_f\) constante al crecer \(k\) hay
  que crecer \(t\) en la misma proporción (\(t/c_r\) constante), de modo que
  la línea blanca sube hacia la derecha casi linealmente.

**Cómo leerla.** Fija una fila (tu tamaño de aleta) y recorre hacia la
derecha hasta cruzar la línea blanca: ese espesor es el mínimo. Compara con
la figura 06: aletas pequeñas dan más margen de flutter pero menos
estabilidad.

**No concluir.** Que las 3 filas representen todo el espacio de diseño
(solo hay tres escalas simuladas; el color entre ellas es interpolación
visual). Ni que agrandar aletas sea siempre malo: el criterio de flutter
empuja hacia aletas pequeñas, el de estabilidad hacia aletas grandes, y el
diseño vive en el compromiso.

## Figura 06 · `06-design-space.png` — elegir un diseño con varios criterios

![Figura 06: espacio de diseño](../outputs/06-design-space.png)

**Qué se dibuja.** Izquierda: apogeo AGL frente a carga útil (0, 3, 6 kg),
una línea por escala de aleta, con viento base. Derecha: cada uno de los 18
casos (3 cargas × 3 escalas × 2 vientos) como un punto de apogeo frente a
ratio mínimo; los círculos son admisibles y las cruces no; la línea
discontinua es el límite 1.25.

**La física detrás.**

- *Apogeo frente a carga.* Más masa con el mismo empuje significa menos
  aceleración (\(a = (T - D - m g)/m\)) y menos velocidad al burnout; el apogeo
  cae unos 170 m por kilogramo. Las tres rectas casi paralelas muestran que
  el tamaño de aleta cuesta poco apogeo (unos 20 m por escalón de escala) por
  su arrastre adicional.
- *Ratio frente a carga.* Aquí hay un efecto menos intuitivo: los cohetes
  más pesados vuelan **más lento**, así que \(q\) máxima baja y el ratio de
  flutter **mejora** (2.04 con 0 kg → 2.38 con 3 kg → 2.74 con 6 kg para la
  escala 1). La carga útil, sin tocar la aleta, es una forma de ganar margen
  a costa de altura.
- *Por qué hay cruces.* Los dos casos no admisibles (×0.85, 0 kg) tienen el
  mejor ratio de flutter (2.59) pero un margen estático de 0.9 calibres,
  por debajo del límite 1.0: la aleta pequeña no estabiliza suficiente. El
  flutter no es el único criterio de `Limits`; también hay estabilidad,
  velocidad de salida del riel, ángulo de ataque y Mach.
- *Viento.* Los pares de puntos casi superpuestos son el mismo diseño con 0 y
  4 m/s de viento: el viento cambia poco el apogeo (unos 20 m) y casi nada el
  ratio, pero sí el ángulo de ataque (1.8° frente a 5.6°).

**Cómo leerla.** La selección automática (`select_best`) escoge el diseño
admisible con **mayor apogeo en su peor viento**: escala 1, 0 kg, 3287 m,
ratio 2.04. Un punto solo cuenta si todos sus escenarios de viento son
admisibles.

**No concluir.** Que el punto más alto sea el mejor: el más alto es una cruz.
Ni que 18 puntos sean un diseño “optimizado”: es una malla gruesa de
comparación.

## Figura 07 · `07-drag-sensitivity.png` — ¿cuánto depende la conclusión del Cd?

![Figura 07: sensibilidad al arrastre](../outputs/07-drag-sensitivity.png)

**Qué se dibuja.** El coeficiente de arrastre del cohete se multiplica por
0.85, 1.00 y 1.15 y se vuelve a simular. Izquierda: altura AGL frente a
tiempo. Derecha: ratio \(V_f/V\) frente a tiempo para las tres trayectorias.

**La física detrás.**

- *Altura.* El arrastre \(D = q\,C_D\,A\) es la fuerza que más incertidumbre
  tiene en un cohete amateur (depende del acabado, las uniones, el ángulo de
  ataque). Un 15 % más de \(C_D\) resta 154 m de apogeo; un 15 % menos suma
  175 m. Las curvas se separan sobre todo después del burnout, cuando el
  arrastre ya no compite con el empuje.
- *Ratio.* Durante la combustión las tres curvas son indistinguibles: el
  empuje domina y la velocidad máxima apenas cambia (más arrastre → un poco
  menos de \(V\) máxima → un poco más de margen: 2.02, 2.04, 2.05). Después
  del burnout las curvas se abren porque el cohete con más arrastre frena
  antes, pero ahí el ratio ya es alto y no importa.

**Cómo leerla.** Es un análisis de sensibilidad, no de incertidumbre: se
prueban tres valores plausibles y se mira si la conclusión cambia. Aquí el
mínimo del ratio se mueve ±0.8 % y el veredicto (admisible con margen) no
cambia. Eso es lo que se debe reportar: “la conclusión de flutter es robusta
frente a ±15 % de \(C_D\); el apogeo no lo es (±5 %)”.

**No concluir.** Que el \(C_D\) real esté dentro de ±15 %, ni que las tres
curvas den una barra de error estadística.

## Cómo se conectan las siete figuras

1. **01** produce la trayectoria: \(V(t)\), \(h(t)\), \(q(t)\).
2. **03** explica cómo la atmósfera (\(p\), \(a_s\)) convierte esa altura en
   una frontera \(V_f\) que sube con la altitud.
3. **02** junta ambas cosas en el tiempo y encuentra el mínimo del ratio en
   Max‑Q: es el resultado principal.
4. **04** y **05** preguntan cómo mover ese mínimo cambiando la aleta:
   espesor (exponente 3/2), material (\(\sqrt{G}\)) y tamaño (\(k^{-3/2}\)).
5. **06** pone el flutter junto a los demás criterios (estabilidad, apogeo,
   viento) para elegir un diseño.
6. **07** comprueba que la conclusión no dependa del parámetro más incierto
   del vuelo.

## Cómo escribir un pie de figura

> **Figura N.** Qué se muestra, con unidades y caso utilizado. El patrón
> principal es ____, y se explica porque ____ (la ecuación o ley). Esta
> lectura permite ____, pero no permite concluir ____. La fuente numérica es
> `archivo.csv` o la clave correspondiente de `results.json`.

Ejemplo para la figura 02:

> **Figura 2.** Velocidad de flutter \(V_f\) y rapidez relativa al aire \(V\)
> del caso base entre la salida del riel y el apogeo, con el cociente
> \(V_f/V\) y el límite 1.25. El mínimo (2.04) ocurre a 3.34 s, coincidiendo
> con Max‑Q, porque para una aleta fija \(R_f^2 \propto 1/q\). Permite
> afirmar que el diseño base cumple el margen con la fórmula de Bennett; no
> permite afirmar que la aleta real no vibrará. Fuente: `baseline.csv`,
> `results.json → baseline.min_flutter_ratio`.
