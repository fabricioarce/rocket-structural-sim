#set page(
  paper: "a4",
  margin: (top: 2.4cm, bottom: 2.6cm, left: 2.2cm, right: 2.2cm),
  numbering: "1",
  header: context {
    if counter(page).get().first() > 1 {
      text(size: 8pt, fill: rgb("#777777"))[Estudio de flutter de aletas para un cohete de alta potencia — Guía]
      line(length: 100%, stroke: 0.4pt + rgb("#cccccc"))
    }
  },
)
#set text(lang: "es", size: 10.6pt)
#set par(justify: true, leading: 0.62em)
#set heading(numbering: none)
#set list(indent: 4pt, spacing: 0.65em)
#set enum(indent: 4pt, spacing: 0.65em)
#set table(inset: 6pt, stroke: 0.6pt + rgb("#a0a0a0"))
#show table.cell: set par(justify: false)
#show table.cell: set text(size: 9.6pt)
#set raw(theme: none)
#show raw: it => text(font: "DejaVu Sans Mono", size: 9pt, it)
#show link: it => text(fill: rgb("#0b5a86"))[#underline(it)]
#show figure.caption: it => text(size: 9pt, fill: rgb("#555555"), it)

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(2pt)
  block(width: 100%, below: 18pt)[
    #line(length: 100%, stroke: 1.4pt + rgb("#0b5a86"))
    #v(6pt)
    #text(size: 19pt, weight: "bold", fill: rgb("#0b5a86"))[#it.body]
    #v(2pt)
    #line(length: 100%, stroke: 0.6pt + rgb("#0b5a86"))
  ]
}
#show heading.where(level: 2): it => block(above: 14pt, below: 8pt, sticky: true)[
  #text(size: 13.5pt, weight: "bold")[#it.body]
]
#show heading.where(level: 3): it => block(above: 10pt, below: 6pt, sticky: true)[
  #text(size: 11.5pt, weight: "bold", style: "italic")[#it.body]
]

// --- Portada ---
#align(center)[
  #v(2.5cm)
  #text(size: 12pt, fill: rgb("#0b5a86"))[ROCKETPY + FIN FLUTTER]
  #v(0.6cm)
  #text(size: 27pt, weight: "bold")[Guía complementaria del proyecto]
  #v(0.2cm)
  #text(size: 16pt)[Física, flutter, programación y lectura de gráficas]
  #v(1.4cm)
  #block(width: 85%, fill: rgb("#fff4e6"), stroke: 1pt + rgb("#e8a33d"), radius: 5pt, inset: 14pt)[
    #text(size: 10.5pt)[
      *Estado del proyecto:* prototipo computacional verificado con pruebas numéricas,
      *no validado experimentalmente*. No autoriza fabricar ni lanzar un cohete real.
      Cubre únicamente el ascenso libre, desde el abandono del riel hasta el apogeo.
    ]
  ]
  #v(1.6cm)
  #text(size: 11pt)[Capítulos incluidos en este PDF: 01 · Física desde cero — 02 · Flutter desde cero —]
  #v(0.1cm)
  #text(size: 11pt)[03 · Programación desde cero — 05 · Todas las gráficas, explicadas desde sus ejes]
  #v(1.6cm)
  #text(size: 10pt, fill: rgb("#555555"))[
    Repositorio completo, capítulos 00, 04, 06, 07 y 08, código y resultados de referencia: \
    #link("https://github.com/fabricioarce/rocket-structural-sim")[github.com/fabricioarce/rocket-structural-sim]
  ]
  #v(0.3cm)
  #text(size: 9.5pt, fill: rgb("#777777"))[Documento generado a partir de docs/01, docs/02, docs/03 y docs/05 del repositorio (fuente editable en docs/pdf/).]
]

#pagebreak()
#outline(title: [Contenido], indent: auto)



#pagebreak(weak: true)


= 01 · Física desde cero: del vuelo al aire que ve la aleta



Siguiente: flutter



Este capítulo construye el vocabulario mínimo para leer una trayectoria. No se necesita aceptar una cifra porque «parece razonable»: primero se revisan unidades, intervalo y definición.



== 1. Unidades y magnitudes



#table(
  columns: (1.03fr, 1.41fr, 0.56fr),
  align: (left, left, left),
  table.header([*Magnitud*], [*Símbolo*], [*Unidad*]),
  [Tiempo], [$t$], [s],
  [Posición], [$x,y,z$], [m],
  [Masa], [$m$], [kg],
  [Velocidad], [$v$], [m/s],
  [Aceleración], [$a$], [m/s²],
  [Fuerza], [$F$], [N],
  [Presión], [$p$ o $q$], [Pa],
  [Densidad], [$rho$], [kg/m³],
)



El Pascal es $1 "Pa"=1 "N/m^2"$. Presión atmosférica y presión dinámica tienen la misma unidad, pero no son la misma magnitud.



== 2. Posición, velocidad y aceleración



La velocidad media entre dos instantes es:



$ bold(v)_("media") = (Delta bold(r))/(Delta t) $



La aceleración media es:



$ bold(a)_("media") = (Delta bold(v))/(Delta t) $



RocketPy integra ecuaciones de movimiento y proporciona muestras de la trayectoria. El proyecto consulta esas muestras; no reemplaza el integrador.



La rapidez es el tamaño de la velocidad:



$ V = sqrt(v_x^2 + v_y^2 + v_z^2) $



== 3. Fuerzas y motor



La segunda ley resume la relación:



$ sum bold(F)_("externas") = m bold(a) $



En un cohete la masa cambia durante la combustión y el empuje no es constante. Por eso una cuenta de «empuje dividido por masa inicial» solo es una intuición. El motor local `Cesaroni_M1670.eng` y RocketPy resuelven el vuelo de referencia.



La gravedad, el empuje y el arrastre afectan la trayectoria. La simulación analizada empieza después de abandonar el riel y termina en el apogeo.



== 4. Velocidad respecto al aire



El viento hace que la velocidad del cohete y la del aire no sean iguales:



$ bold(v)_("rel") = bold(v)_("cohete") - bold(v)_("aire"), quad V_("rel") = abs(bold(v)_("rel")) $



Flutter depende de lo que ve la aleta: $V_("rel")$, no simplemente de la velocidad respecto al suelo. En el caso base el viento es 4 m/s, pequeño frente a unos 286 m/s, pero no se descarta por definición.



== 5. Atmósfera y presión dinámica



La atmósfera local aporta presión estática $p$, densidad $rho$ y velocidad del sonido $a_s$. La presión dinámica es:



$ q = 1/2 rho V_("rel")^2 $



Max-Q es el máximo de $q$ en el intervalo elegido. No es una fuerza total, ni una presión uniforme sobre toda la superficie, ni un margen de flutter. Para convertirla en arrastre hacen falta coeficiente y área:



$ D = q C_D A_("ref") $



En el caso base Max-Q es aproximadamente 41.60 kPa a 3.341 s. El valor de salida de las funciones atmosféricas cambia con la altitud.



== 6. Ángulo de ataque, Mach y estabilidad



El ángulo de ataque describe la orientación del vehículo respecto al flujo. Mach compara la rapidez relativa con el sonido:



$ "Ma" = V_("rel") / a_s $



El centro de masa (CG) resume la distribución de masa; el centro de presión (CP) resume la acción aerodinámica del modelo. Una diferencia entre ambos, expresada en calibres, es el margen estático. Es un criterio de orientación, no una garantía de flutter.



== 7. Qué entrega RocketPy y qué añade este proyecto



RocketPy entrega vuelo, $V_("rel")$, altitud, $p$, $a_s$, Mach y estabilidad. `flutter.py` usa esas señales para calcular $V_f$. `study.py` calcula el ratio, el espesor requerido y resúmenes. La aleta no se deforma en la simulación de trayectoria.



== 8. Velocidad del sonido y por qué importa para el flutter



Para un gas ideal en la aproximación usada:



$ a_s = sqrt(gamma p/rho) $



Al ganar altitud disminuyen $p$ y $rho$, y la velocidad del sonido cambia de forma más suave que la presión. En la fórmula de Bennett, manteniendo la geometría:



$ V_("f") "∝" a_s sqrt(1/p), quad V_("f") "∝" 1/sqrt(rho) $



Por eso $V_f$ puede aumentar mientras el cohete asciende aunque la presión estática baje. El ratio final también depende de $V_("rel")$, así que no se debe interpretar la altitud aislada.



_Siguiente paso:_ en el capítulo 02 se construye la frontera de flutter desde la geometría y el módulo de corte $G$.




#pagebreak(weak: true)


= 02 · Flutter desde cero: aeroelasticidad de una aleta



Siguiente: programación



El proyecto es un _estudio de flutter de aletas para un cohete de alta potencia_. RocketPy es una caja negra de vuelo; este capítulo explica el cálculo empírico posterior. La fórmula procede de Bennett (2023) y no es una simulación modal de una estructura real.



== 1. Aeroelasticidad: por qué una aleta puede vibrar



Aeroelasticidad significa que el flujo y la deformación de una estructura se afectan mutuamente. Una aleta puede flexionarse, torcerse y cambiar el ángulo con el que encuentra el aire. Esa nueva orientación cambia la fuerza, y la fuerza puede alimentar la deformación.



El flutter aparece cuando el intercambio de energía del flujo con los movimientos supera la disipación efectiva. La palabra «aparece» aquí describe el fenómeno físico; el código solo calcula una frontera nominal de velocidad.



== 2. Vibración, resonancia y flutter no son sinónimos



- _Vibración:_ oscilación alrededor de una posición.
- _Resonancia:_ respuesta grande ante una excitación cercana a una frecuencia natural.
- _Flutter:_ inestabilidad aeroelástica autoalimentada por el acoplamiento entre flujo y deformación.



Una vibración no implica flutter, y una cuenta de $V_f$ no entrega frecuencias, amplitudes ni una película del movimiento.



== 3. Rigidez, $G$ y torsión



En elasticidad lineal, una tensión tangencial $tau$ y una deformación angular $gamma_s$ se relacionan aproximadamente por:



$ tau = G gamma_s $



El módulo de corte $G$ tiene unidades Pa. El módulo de Young $E$ describe otra deformación; no aparece en la fórmula de Bennett usada aquí. _$G$ es la única propiedad del material que entra en esa fórmula._ La densidad se usa para la masa del vuelo, no para calcular $V_f$ algebraicamente.



Las cifras de `materials.py` son valores típicos de referencia, no propiedades certificadas. Un fabricante, una orientación de fibras o una unión puede cambiar mucho $G$.



== 4. Geometría de la aleta



La aleta trapezoidal se describe con:



- $c_r$: cuerda raíz.
- $c_t$: cuerda punta.
- $s$: barrido axial del borde delantero.
- $b$: envergadura expuesta.
- $t$: espesor constante.
- $S=(c_r+c_t)b/2$: área.
- $"AR"=b^2/S$: relación de aspecto.
- $lambda=c_t/c_r$: taper o estrechamiento.



El centroide axial que usa el código es:



$ C_x = (c_r^2 + c_r c_t + c_t^2 + s(c_r+2c_t)) / (3(c_r+c_t)), quad epsilon = C_x/c_r - 1/4 $



La aproximación exige $epsilon>0$. Las propiedades `aspect_ratio` y `taper` de `Fin` alimentan directamente la fórmula.



== 5. Fórmula de Bennett (2023), término por término



La velocidad nominal de flutter implementada es:



$ V_f = a_s sqrt(N_v / D_v), quad N_v = G ("AR"+2) (delta/c_r)^3, quad D_v = (24 epsilon gamma)/pi dot p dot "AR"^3 dot (1+lambda)/2, quad gamma=1.4 $



Aquí:



#table(
  columns: (1.18fr, 1.50fr, 0.55fr),
  align: (left, left, left),
  table.header([*Símbolo*], [*Significado*], [*Unidad*]),
  [$V_f$], [frontera nominal de flutter], [m/s],
  [$a_s$], [velocidad local del sonido], [m/s],
  [$G$], [módulo de corte de la aleta], [Pa],
  [$p$], [presión estática], [Pa],
  [$t,c_r$], [espesor y cuerda raíz], [m],
  [AR, $lambda,epsilon$], [relaciones geométricas], [1],
  [$gamma$], [razón de calores específicos], [1],
)



El cociente $t/c_r$ no tiene unidad. Presión y $G$ deben expresarse en las mismas unidades; el programa usa Pa.



La dependencia útil es:



$ V_("f") "∝" (t/c_r)^(3/2), quad V_("f") "∝" G^(1/2), quad V_("f") "∝" p^(-1/2) $



AR aparece en el numerador y en el denominador, por lo que no basta con decir «AR grande es mejor» sin evaluar toda la expresión. Bennett publica un ejemplo de aproximadamente 1425 ft/s; los valores exactos del chequeo local están en `test_flutter.py` y la prueba conserva esa referencia.



== 6. Ratio, margen 1.25 y Max-Q



El margen graficado es:



$ R_f (t) = (V_f (t)) / (V_("rel") (t)) $



La demo exige $R_f>= 1.25$. Es un límite de comparación, no una certificación. En la trayectoria base el mínimo es _2.0381962789_. Ocurre cerca de Max-Q porque, bajo las hipótesis del modelo, la presión dinámica concentra la condición aerodinámica más exigente.



Para el caso base:



#table(
  columns: (1.41fr, 0.59fr),
  align: (left, right),
  table.header([*Métrica*], [*Resultado*]),
  [$R_f$ en Max-Q], [2.03819628],
  [$R_f$ en máxima velocidad], [2.03884546],
)



Son instantes y operaciones distintas. La diferencia pequeña no autoriza a redondearlos como si fueran la misma variable.



== 7. Espesor requerido



`required_thickness` invierte la fórmula para una velocidad objetivo $V_"objetivo"=R_"objetivo"V_"rel"$:



$ t_("req") = c_r ((V_("objetivo")/a_s)^2 dot (24 epsilon gamma/pi) dot p dot "AR"^3 dot (1+lambda)/2 / (G dot ("AR"+2)))^(1/3) $



El programa aplica la expresión a toda la historia y toma el máximo. Para la trayectoria base y $R_"objetivo"=1.25$, el aluminio requiere 2.17 mm; los demás valores aparecen en README y `results.json`.



== 8. Barrido algebraico frente a resimulación



Un barrido de espesor o material reutiliza presión, sonido y rapidez de una trayectoria y recalcula $V_f$. Es postprocesado algebraico: _ignora el cambio de masa de la aleta_. Sirve para comparar rápido, no para sustituir una nueva trayectoria.



La aleta delgada de 1.2 mm sí se vuelve a simular. Su ratio re-simulado es 0.51033860; el cálculo algebraico da 0.51562740. La diferencia relativa guardada en `results.json` es 0.01036333, inferior al 2% documentado.



== 9. Escala uniforme y relación con Max-Q



Si todas las dimensiones del plano se multiplican por $k$, pero $t$ no, AR, $lambda$ y $epsilon$ permanecen iguales y $t/c_r$ se divide por $k$. Por tanto:



$ V_f -> V_f k^(-3/2) $



La aleta más grande no es automáticamente más segura frente a flutter. También cambia área y masa, y una resimulación debe estudiar esos efectos.



Con el factor geométrico $B$ constante:



$ a_s^2 = gamma p/rho, quad V_f^2 = a_s^2 (G B)/p = (gamma G B)/rho, quad R_f^2 = (gamma G B)/(rho V_("rel")^2) = (gamma G B)/(2q) $



Esta es la _relación con Max-Q_: minimizar el ratio equivale a maximizar $q$ bajo esas hipótesis. No es una ley universal de estructuras flexibles.



== 10. Qué no dice el modelo



El módulo modela aletas trapezoidales homogéneas, espesor constante y propiedades efectivas isótropas. No resuelve amplitud, rotura, modos, uniones, laminados, amortiguamiento ni divergencia. Rebasar la frontera señala riesgo según el modelo, no una rotura segura.



_Siguiente paso:_ practica una evaluación de `Fin`, `flutter_speed` y `required_thickness` en el capítulo de programación.




#pagebreak(weak: true)


= 03 · Programación desde cero: convertir una ecuación en un estudio



Siguiente: código y datos



No necesitas conocer Python para empezar. El objetivo es reconocer entradas, operaciones, decisiones y resultados.



== 1. Un programa y un módulo



Un programa es una secuencia de instrucciones. Un módulo `.py` guarda funciones y clases que otros archivos pueden importar. La ejecución de referencia la coordina `run_demo.py`; la física de la frontera está en `flutter.py`.



== 2. Variables y unidades



```python
densidad = 1.0
velocidad = 100.0
presion_dinamica = 0.5 * densidad * velocidad**2
print(presion_dinamica)
```



La salida es `5000.0` Pa porque las entradas se expresan en kg/m³ y m/s. Python no añade unidades automáticamente.



`26e9` significa $26 dot 10^9$. En la configuración representa un módulo de corte en Pa.



== 3. Funciones y objetos



```python
from flutter import Fin, flutter_speed

fin = Fin(0.20, 0.10, 0.12, 0.04, 0.003, 26e9)
vf = flutter_speed(fin, 80000.0, 330.0)
print(f"{vf:.1f} m/s")
```



`Fin` agrupa geometría y propiedad efectiva. `flutter_speed` recibe el objeto y el estado atmosférico. El resultado es una cifra; su interpretación exige revisar las hipótesis del capítulo 02.



== 4. Invertir una función



```python
from flutter import Fin, required_thickness

fin = Fin(0.20, 0.10, 0.12, 0.04, 0.003, 26e9)
thickness = required_thickness(fin, 80000.0, 330.0, 1.25 * 250.0)
print(f"{float(thickness) * 1000:.2f} mm")
```



El espesor requerido toma una velocidad objetivo. El programa también acepta arrays de NumPy para recorrer toda una historia temporal.



== 5. Listas, bucles y barridos



```python
from flutter import Fin, flutter_speed

fin = Fin(0.20, 0.10, 0.12, 0.04, 0.003, 26e9)
for pressure in [100000.0, 80000.0, 60000.0]:
    print(pressure, flutter_speed(fin, pressure, 330.0))
```



`study.py` repite una idea similar para diseños, vientos y espesores. Un barrido no inventa incertidumbre: solo evalúa las combinaciones que aparecen en la configuración.



== 6. Diccionarios y resultados



```python
import json

data = json.loads(open("outputs/results.json", encoding="utf-8").read())
base = data["baseline"]
print(base["min_flutter_ratio"], base["required_thickness_mm"])
```



JSON conserva nombres junto con valores. `results.json` es más trazable que una cifra copiada de una gráfica porque incluye configuración y resúmenes.



== 7. Decisiones y pruebas



```python
from materials import get_material

material = get_material("aluminio_6061")
if material["shear_pa"] > 20e9:
    print("módulo de referencia alto")
else:
    print("módulo de referencia bajo")
```



Las pruebas automáticas comprueban casos concretos: inversión del espesor, escalado uniforme, selección y propiedades de masa. Una prueba pasada verifica el código para las entradas elegidas; no convierte el modelo en una medición.



== 8. Flujo completo



```text
demo.json
    ↓
Design + Environment + SolidMotor + Rocket + Flight
    ↓
presión, sonido, rapidez, altitud, Mach y estabilidad
    ↓
Fin + flutter_history + required_thickness
    ↓
resúmenes, barridos, JSON, CSV, PNG e HTML
```



_Siguiente paso:_ consulta el mapa de archivos en código y datos, y luego aprende a leer las figuras.




#pagebreak(weak: true)


= 05 · Las siete gráficas, explicadas con su física



Siguiente: metodología



Todas las imágenes salen de `outputs/` con la configuración congelada de `demo.json`. El _caso base_ es: carga útil 0 kg, escala de aleta 1, espesor 3 mm de aluminio 6061 ($G = 26$ GPa), viento 4 m/s. El intervalo graficado va desde que el cohete abandona el riel (0.37 s) hasta el apogeo (25.8 s). El sitio de lanzamiento está a 1400 m sobre el nivel del mar, por eso conviven dos alturas: _AGL_ (sobre el suelo) y _ASL_ (sobre el mar).



Cada sección sigue el mismo orden: qué se dibuja, qué física hay detrás, cómo leerla, qué cifras salen de ella y qué _no_ se puede concluir.



== Antes de empezar: las tres cantidades que se repiten



- _Rapidez relativa al aire $V$_: lo que “siente” la aleta. Es la rapidez del cohete respecto al suelo combinada con el viento ($v_("rel") = v_("cohete") - v_("aire")$ como vectores, capítulo 01).
- _Velocidad de flutter $V_f$_: la rapidez del aire a la que, según la fórmula de Bennett (capítulo 02), la aleta entraría en flutter. Depende de la aleta ($G$, espesor, geometría) y de la atmósfera local (presión $p$ y velocidad del sonido $a_s$); _no_ depende de cuánto corra el cohete.
- _Ratio $R_f = V_f/V$_: cuántas veces más rápido tendría que ir el aire para llegar al flutter. $R_f>1$ es zona segura según el modelo; la demo exige $R_f >= 1.25$ como margen.



La pregunta de todo el estudio es: _¿en qué instante del vuelo se acercan más $V$ y $V_f$, y cuánto margen queda ahí?_



== Figura 01 · `01-flight.png` — el vuelo que alimenta todo lo demás



#figure(image("../../outputs/01-flight.png", width: 92%), caption: [vuelo base])



_Qué se dibuja._ Cuatro paneles contra el tiempo desde la ignición. Arriba izquierda: altura AGL. Arriba derecha: rapidez respecto al aire (línea continua) y respecto al suelo (discontinua). Abajo izquierda: presión dinámica $q$ con la línea de Max‑Q. Abajo derecha: margen estático en calibres con su límite de 1.



_La física detrás._



- _Altura._ Mientras el empuje supera al peso más el arrastre la curva se dobla hacia arriba (aceleración positiva). Eso termina a 3.38 s, un poco antes del burnout (3.9 s), porque el empuje del motor decae en su cola. Después solo actúan la gravedad y el arrastre, ambas frenando: la curva se va aplanando hasta el apogeo, donde la velocidad vertical es cero. Es la cinemática de MRUA que ya conoces, pero con una aceleración que cambia en el tiempo.
- _Velocidades._ La rapidez sube casi en línea recta mientras hay empuje y alcanza 285.8 m/s respecto al suelo (286.1 m/s respecto al aire) a 3.38 s. La caída posterior es más lenta que la subida porque, sin empuje, la desaceleración es $g + D/m$ y el arrastre $D$ disminuye conforme el cohete frena. Las dos curvas casi se superponen porque el viento (4 m/s) es pequeño frente a la rapidez del cohete: el viento importa para el ángulo de ataque, no para la magnitud de $V$.
- _Presión dinámica._ $q = rho V^2/2$. Crece con el cuadrado de la velocidad y decrece con la densidad, que baja con la altura. El máximo (_Max‑Q = 41.6 kPa a 3.34 s_) ocurre unas décimas antes de la velocidad máxima: el cohete todavía acelera, pero ya subió lo suficiente para que la pérdida de $rho$ empiece a pesar más que la ganancia de $V^2$.
- _Margen estático._ Distancia entre centro de presión y centro de masa en diámetros del cuerpo. Sube durante la combustión porque el propelente (que está atrás) se consume y el CG avanza hacia la nariz. Nunca baja de 1, así que el cohete es estable en todo el tramo.



_Cómo leerla._ Localiza las tres marcas temporales que reaparecen en las demás figuras: burnout (3.9 s), Max‑Q (3.34 s) y velocidad máxima (3.38 s). Nota que las tres se apretujan en menos de un segundo: el tramo crítico para las aletas es muy corto.



_Cifras que salen de aquí._ Apogeo 3287.3 m AGL (4687.3 m ASL); $V$ máxima 286.1 m/s; Max‑Q 41.60 kPa; Mach máximo 0.86; margen mínimo 2.28 calibres al salir del riel.



_No concluir._ Que el cohete “vuela recto”: la figura no muestra trayectoria horizontal ni orientación. Tampoco que $q$ sea una propiedad de la aleta; es una propiedad del flujo que la aleta ve.



== Figura 02 · `02-flutter-history.png` — la gráfica central del proyecto



#figure(image("../../outputs/02-flutter-history.png", width: 92%), caption: [historia de flutter])



_Qué se dibuja._ Tres paneles con el mismo eje de tiempo. Arriba: $V_f$ (verde) y $V$ relativa (azul) en m/s, con las líneas verticales de burnout, Max‑Q y velocidad máxima. Centro: el ratio $V_f/V$, la línea horizontal del límite 1.25 y un punto en el mínimo. Abajo: presión estática $p$ (kPa, eje izquierdo) y velocidad del sonido $a_s$ (m/s, eje derecho).



_La física detrás._



- _Por qué $V_f$ es casi horizontal._ La aleta no cambia durante el vuelo; lo único que varía en la fórmula es la atmósfera. Con $V_f  ∝  a_s/sqrt(p)$, al subir 3.3 km la presión baja de 85.6 kPa a 56.3 kPa y $a_s$ baja de 334.5 a 321.1 m/s. El efecto neto es que $V_f$ _sube_ de 569 m/s en el riel a 673 m/s en el apogeo: el aire enrarecido tiene menos capacidad de “empujar” la aleta hacia la inestabilidad.
- _Por qué el ratio tiene forma de “U” asimétrica._ Al salir del riel $V$ es pequeña (26 m/s) y $R_f = 21.5$, enorme. Conforme el motor acelera, $V$ crece y el ratio se desploma. Después del burnout $V$ decae y $V_f$ sube, así que el ratio vuelve a crecer hasta 25.6 en el apogeo. El mínimo es la única zona que importa.
- _Por qué el mínimo coincide con Max‑Q y no exactamente con la velocidad máxima._ Sustituyendo $a_s^2=gamma p/rho$ en la fórmula (capítulo 02, §9) se obtiene $R_f^2 = gamma G B/(rho V^2) = gamma G B/(2q)$, con $B$ un factor puramente geométrico. Para una aleta dada, _minimizar $R_f$ es exactamente maximizar $q$_. Por eso el mínimo (2.0382) cae a 3.341 s, el instante de Max‑Q, y el ratio en la velocidad máxima (3.384 s) es apenas mayor: 2.0388.
- _Panel inferior._ Muestra las dos entradas atmosféricas de la fórmula. Ambas bajan con la altura; el descenso de $p$ domina porque entra como $p^(-1/2)$ y cae un 34 %, mientras que $a_s$ cae solo un 4 %.



_Cómo leerla._ Primero mira el panel central: ¿la curva toca la línea 1.25? En el caso base no: el mínimo es _2.04_, así que hay 63 % de margen sobre el límite y el doble de margen sobre el flutter nominal. Luego sube al panel superior y comprueba la distancia vertical entre las dos curvas en el instante de Max‑Q: 583 m/s frente a 286 m/s.



_Cifras que salen de aquí._ Mínimo $R_f = 2.0382$ a 3.341 s y 1898 m ASL; $V_f$ en ese instante 583.0 m/s; $V$ en ese instante 286.0 m/s.



_No concluir._ Que “la aleta vibra a 583 m/s”: $V_f$ es una frontera nominal empírica, no una medición. Ni que un ratio de 2 signifique “doble de seguro” en sentido probabilístico: el modelo no tiene incertidumbre asociada.



== Figura 03 · `03-altitude.png` — separar la aleta de la atmósfera



#figure(image("../../outputs/03-altitude.png", width: 92%), caption: [altitud y atmósfera])



_Qué se dibuja._ El eje vertical es altitud ASL de 0 a 10 km, no tiempo. Izquierda: $V_f$ que tendría la aleta base (3 mm) y la aleta delgada (1.2 mm) si el aire local fuese el de esa altitud. Derecha: presión, densidad y velocidad del sonido del modelo atmosférico, divididas por su valor al nivel del mar. La banda sombreada es el tramo que el vuelo base recorre realmente (1.4 km a 4.7 km ASL).



_La física detrás._



- _Atmósfera._ En la troposfera la temperatura baja unos 6.5 K por km, y presión y densidad caen aproximadamente de forma exponencial. La velocidad del sonido depende solo de la temperatura ($a_s = sqrt(gamma R T)$), por eso su curva es casi una recta suave y cae poco (12 % en 10 km), mientras $p$ pierde el 74 % y $rho$ el 66 %.
- _$V_f$ frente a altitud._ Es la misma fórmula evaluada a cada altura con la aleta fija. Crece porque $1/sqrt(p)$ crece más rápido de lo que $a_s$ decrece. La curva de la aleta delgada tiene la misma forma pero está desplazada hacia la izquierda por el factor $(1.2/3)^(3/2) = 0.253$: $V_f$ escala con $(t/c_r)^(3/2)$, y ese exponente 3/2 es la razón de que el espesor sea la variable más poderosa del diseño.



_Cómo leerla._ Sirve para responder “¿y si lanzamos desde otro sitio?”. Un lanzamiento a nivel del mar tendría $V_f = 530$ m/s en el riel en lugar de 569 m/s: algo menos de margen. La banda sombreada recuerda que el resto de la curva es una extrapolación del modelo atmosférico, no parte del vuelo.



_No concluir._ Que el cohete llegue a 10 km, ni que $R_f$ mejore con la altura “automáticamente”: aquí solo se dibuja $V_f$; la rapidez $V$ del cohete también cambia con la altura y no aparece en esta figura.



== Figura 04 · `04-thickness-sweep.png` — la variable de diseño que más pesa



#figure(image("../../outputs/04-thickness-sweep.png", width: 92%), caption: [barrido de espesor])



_Qué se dibuja._ Izquierda: ratio mínimo del vuelo frente a espesor de la aleta (1 a 8 mm), una curva por material, la línea del límite 1.25 y una línea vertical en el espesor base (3 mm). Derecha: barras con el espesor mínimo que cada material necesita para cumplir exactamente $R_f = 1.25$ en la trayectoria base.



_La física detrás._



- _Forma de las curvas._ Como $V_f  ∝  t^(3/2)$ y $V$ no cambia (el barrido reutiliza la trayectoria base), $R_f$ mínimo $∝  t^(3/2)$. Duplicar el espesor multiplica el margen por $2^(1.5) = 2.83$. Por eso las curvas se curvan hacia arriba y no son rectas.
- _Separación entre materiales._ La única propiedad del material en la fórmula es $G$ y entra como $sqrt(G)$. El aluminio (26 GPa) tiene 6.3 veces la $G$ del G10 (4.14 GPa), así que su curva está $sqrt(6.3)=2.5$ veces más alta a igual espesor. Para compensar una $G$ menor hay que aumentar $t$ según $t  ∝  G^(-1/3)$: el G10 necesita $6.3^(1/3) = 1.85$ veces el espesor del aluminio (4.00 mm frente a 2.17 mm), justo lo que muestran las barras.
- _Barras._ Es la fórmula invertida (`required_thickness`, capítulo 02 §7) aplicada a todo el vuelo y tomando el peor instante, que es Max‑Q.



_Cómo leerla._ Busca dónde cada curva cruza la línea 1.25: ese cruce es el mismo número que la barra del panel derecho. Luego mira dónde queda la línea vertical del espesor base: el aluminio de 3 mm está claramente por encima (2.04); con esos mismos 3 mm el G10 daría 0.81 y el contrachapado 0.33, es decir, _por debajo de 1_: flutter nominal antes de Max‑Q.



_Cifras que salen de aquí._ Espesor requerido para $R_f=1.25$: aluminio 6061 2.17 mm; carbono tejido 0/90 3.89 mm; G10 4.00 mm; acrílico/ policarbonato 6.42 mm; contrachapado de abedul 7.23 mm. Aluminio a 1 mm: 0.39; a 2 mm: 1.11; a 3 mm: 2.04.



_No concluir._ Que una aleta más gruesa sea “gratis”: el barrido es algebraico, mantiene la masa y la trayectoria del caso base. Una aleta de 7 mm de madera pesa distinto, mueve el CG y baja el apogeo; eso solo lo muestra una nueva simulación. El caso delgado sí se resimuló y la diferencia con el estimado algebraico fue 1.0 %, lo que da confianza al barrido para comparar, no para certificar. Tampoco concluir que “carbono es peor que G10”: los valores de $G$ son típicos y para un laminado dependen mucho de la orientación de las fibras.



== Figura 05 · `05-geometry-map.png` — tamaño de aleta frente a espesor



#figure(image("../../outputs/05-geometry-map.png", width: 92%), caption: [mapa geométrico])



_Qué se dibuja._ Un mapa de color. Eje horizontal: espesor (1 a 8 mm). Eje vertical: escala uniforme de la planta de la aleta (0.85, 1.0, 1.15). El color es el ratio mínimo del vuelo; la línea blanca es la frontera $R_f = 1.25$. Cada fila usa la trayectoria simulada para esa escala (carga útil y viento base) y recalcula $V_f$ para cada espesor.



_La física detrás._



- _Escalar la planta._ Multiplicar cuerda raíz, cuerda punta, envergadura y flecha por un factor $k$ deja iguales el alargamiento AR, el estrechamiento $lambda$ y $epsilon$; lo único que cambia en la fórmula es $t/c_r$, que se divide por $k$. Por tanto $V_f  ∝  k^(-3/2)$: una aleta 15 % más grande con el mismo espesor pierde un 19 % de $V_f$. Físicamente: una placa más larga y ancha con el mismo grosor es más flexible a torsión.
- _Efecto sobre la trayectoria._ Aletas más grandes generan más arrastre y algo más de masa, así que $V$ máxima baja un poco; ese efecto va en la dirección contraria pero es mucho menor que el de $t/c_r$. El resultado neto para 3 mm es 2.59 (×0.85), 2.04 (×1.0) y 1.66 (×1.15).
- _Forma de la frontera._ Para mantener $R_f$ constante al crecer $k$ hay que crecer $t$ en la misma proporción ($t/c_r$ constante), de modo que la línea blanca sube hacia la derecha casi linealmente.



_Cómo leerla._ Fija una fila (tu tamaño de aleta) y recorre hacia la derecha hasta cruzar la línea blanca: ese espesor es el mínimo. Compara con la figura 06: aletas pequeñas dan más margen de flutter pero menos estabilidad.



_No concluir._ Que las 3 filas representen todo el espacio de diseño (solo hay tres escalas simuladas; el color entre ellas es interpolación visual). Ni que agrandar aletas sea siempre malo: el criterio de flutter empuja hacia aletas pequeñas, el de estabilidad hacia aletas grandes, y el diseño vive en el compromiso.



== Figura 06 · `06-design-space.png` — elegir un diseño con varios criterios



#figure(image("../../outputs/06-design-space.png", width: 92%), caption: [espacio de diseño])



_Qué se dibuja._ Izquierda: apogeo AGL frente a carga útil (0, 3, 6 kg), una línea por escala de aleta, con viento base. Derecha: cada uno de los 18 casos (3 cargas × 3 escalas × 2 vientos) como un punto de apogeo frente a ratio mínimo; los círculos son admisibles y las cruces no; la línea discontinua es el límite 1.25.



_La física detrás._



- _Apogeo frente a carga._ Más masa con el mismo empuje significa menos aceleración ($a = (T - D - m g)/m$) y menos velocidad al burnout; el apogeo cae unos 170 m por kilogramo. Las tres rectas casi paralelas muestran que el tamaño de aleta cuesta poco apogeo (unos 20 m por escalón de escala) por su arrastre adicional.
- _Ratio frente a carga._ Aquí hay un efecto menos intuitivo: los cohetes más pesados vuelan _más lento_, así que $q$ máxima baja y el ratio de flutter _mejora_ (2.04 con 0 kg → 2.38 con 3 kg → 2.74 con 6 kg para la escala 1). La carga útil, sin tocar la aleta, es una forma de ganar margen a costa de altura.
- _Por qué hay cruces._ Los dos casos no admisibles (×0.85, 0 kg) tienen el mejor ratio de flutter (2.59) pero un margen estático de 0.9 calibres, por debajo del límite 1.0: la aleta pequeña no estabiliza suficiente. El flutter no es el único criterio de `Limits`; también hay estabilidad, velocidad de salida del riel, ángulo de ataque y Mach.
- _Viento._ Los pares de puntos casi superpuestos son el mismo diseño con 0 y 4 m/s de viento: el viento cambia poco el apogeo (unos 20 m) y casi nada el ratio, pero sí el ángulo de ataque (1.8° frente a 5.6°).



_Cómo leerla._ La selección automática (`select_best`) escoge el diseño admisible con _mayor apogeo en su peor viento_: escala 1, 0 kg, 3287 m, ratio 2.04. Un punto solo cuenta si todos sus escenarios de viento son admisibles.



_No concluir._ Que el punto más alto sea el mejor: el más alto es una cruz. Ni que 18 puntos sean un diseño “optimizado”: es una malla gruesa de comparación.



== Figura 07 · `07-drag-sensitivity.png` — ¿cuánto depende la conclusión del Cd?



#figure(image("../../outputs/07-drag-sensitivity.png", width: 92%), caption: [sensibilidad al arrastre])



_Qué se dibuja._ El coeficiente de arrastre del cohete se multiplica por 0.85, 1.00 y 1.15 y se vuelve a simular. Izquierda: altura AGL frente a tiempo. Derecha: ratio $V_f/V$ frente a tiempo para las tres trayectorias.



_La física detrás._



- _Altura._ El arrastre $D = q C_D A$ es la fuerza que más incertidumbre tiene en un cohete amateur (depende del acabado, las uniones, el ángulo de ataque). Un 15 % más de $C_D$ resta 154 m de apogeo; un 15 % menos suma 175 m. Las curvas se separan sobre todo después del burnout, cuando el arrastre ya no compite con el empuje.
- _Ratio._ Durante la combustión las tres curvas son indistinguibles: el empuje domina y la velocidad máxima apenas cambia (más arrastre → un poco menos de $V$ máxima → un poco más de margen: 2.02, 2.04, 2.05). Después del burnout las curvas se abren porque el cohete con más arrastre frena antes, pero ahí el ratio ya es alto y no importa.



_Cómo leerla._ Es un análisis de sensibilidad, no de incertidumbre: se prueban tres valores plausibles y se mira si la conclusión cambia. Aquí el mínimo del ratio se mueve ±0.8 % y el veredicto (admisible con margen) no cambia. Eso es lo que se debe reportar: “la conclusión de flutter es robusta frente a ±15 % de $C_D$; el apogeo no lo es (±5 %)”.



_No concluir._ Que el $C_D$ real esté dentro de ±15 %, ni que las tres curvas den una barra de error estadística.



== Cómo se conectan las siete figuras



1. _01_ produce la trayectoria: $V(t)$, $h(t)$, $q(t)$.
2. _03_ explica cómo la atmósfera ($p$, $a_s$) convierte esa altura en una frontera $V_f$ que sube con la altitud.
3. _02_ junta ambas cosas en el tiempo y encuentra el mínimo del ratio en Max‑Q: es el resultado principal.
4. _04_ y _05_ preguntan cómo mover ese mínimo cambiando la aleta: espesor (exponente 3/2), material ($sqrt(G)$) y tamaño ($k^(-3/2)$).
5. _06_ pone el flutter junto a los demás criterios (estabilidad, apogeo, viento) para elegir un diseño.
6. _07_ comprueba que la conclusión no dependa del parámetro más incierto del vuelo.



== Cómo escribir un pie de figura



#block(fill: rgb("#eef3f8"), stroke: 1pt + rgb("#5c7f9e"), radius: 4pt, inset: 9pt, width: 100%)[#text(size: 9.6pt)[_Figura N._ Qué se muestra, con unidades y caso utilizado. El patrón principal es ____, y se explica porque ____ (la ecuación o ley). Esta lectura permite ____, pero no permite concluir ____. La fuente numérica es `archivo.csv` o la clave correspondiente de `results.json`.]]



Ejemplo para la figura 02:



#block(fill: rgb("#eef3f8"), stroke: 1pt + rgb("#5c7f9e"), radius: 4pt, inset: 9pt, width: 100%)[#text(size: 9.6pt)[_Figura 2._ Velocidad de flutter $V_f$ y rapidez relativa al aire $V$ del caso base entre la salida del riel y el apogeo, con el cociente $V_f/V$ y el límite 1.25. El mínimo (2.04) ocurre a 3.34 s, coincidiendo con Max‑Q, porque para una aleta fija $R_f^2  ∝  1/q$. Permite afirmar que el diseño base cumple el margen con la fórmula de Bennett; no permite afirmar que la aleta real no vibrará. Fuente: `baseline.csv`, `results.json → baseline.min_flutter_ratio`.]]

