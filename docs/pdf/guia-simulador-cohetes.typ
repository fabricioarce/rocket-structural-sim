#set page(
  paper: "a4",
  margin: (top: 2.4cm, bottom: 2.6cm, left: 2.2cm, right: 2.2cm),
  numbering: "1",
  header: context {
    if counter(page).get().first() > 1 {
      text(size: 8pt, fill: rgb("#777777"))[Simulador de cohetes con análisis preliminar de cargas — Guía complementaria]
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
  #text(size: 12pt, fill: rgb("#0b5a86"))[ROCKETPY + CARGAS PRELIMINARES + FIN FLUTTER]
  #v(0.6cm)
  #text(size: 27pt, weight: "bold")[Guía complementaria del proyecto]
  #v(0.2cm)
  #text(size: 16pt)[Física, estructuras, programación y lectura de gráficas]
  #v(1.4cm)
  #block(width: 85%, fill: rgb("#fff4e6"), stroke: 1pt + rgb("#e8a33d"), radius: 5pt, inset: 14pt)[
    #text(size: 10.5pt)[
      *Estado del proyecto:* prototipo computacional verificado con pruebas numéricas,
      *no validado experimentalmente*. No autoriza fabricar ni lanzar un cohete real.
      Cubre únicamente el ascenso libre, desde el abandono del riel hasta el apogeo.
    ]
  ]
  #v(1.6cm)
  #text(size: 11pt)[Capítulos incluidos en este PDF: 01 · Física desde cero — 02 · Estructuras y flutter —]
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


= 01 · Física desde cero: del movimiento al vuelo



_Objetivo:_ entender qué representa cada magnitud antes de utilizar fórmulas. Los ejemplos redondos de este capítulo son didácticos; no son resultados medidos de Calisto. Fuentes: F1–F5 y F8.



== 1. Número, magnitud y unidad



Decir «el cohete pesa 20» no basta. ¿20 gramos, kilogramos o newtons? Una _magnitud física_ es algo que podemos cuantificar; la _unidad_ dice con qué referencia lo expresamos.



#table(
  columns: (0.61fr, 1.82fr, 0.57fr),
  align: (left, left, left),
  table.header([*Magnitud*], [*Significado*], [*Unidad usada*]),
  [Tiempo], [Cuánto transcurre], [Segundo, s],
  [Longitud], [Distancia o dimensión], [Metro, m],
  [Masa], [Medida de inercia traslacional], [Kilogramo, kg],
  [Velocidad], [Cambio de posición por tiempo, con dirección], [m/s],
  [Aceleración], [Cambio de velocidad por tiempo], [m/s²],
  [Fuerza], [Interacción capaz de cambiar el movimiento], [Newton, N],
  [Momento de fuerza], [Tendencia de una fuerza a producir giro], [N·m],
  [Presión y esfuerzo], [Fuerza por unidad de área; distintos conceptos físicos], [Pascal, Pa = N/m²],
  [Densidad], [Masa por volumen], [kg/m³],
)



Unidades frecuentes: `1 mm = 0.001 m`, `1 kPa = 1000 Pa`, `1 MPa = 1 000 000 Pa`, `1 GPa = 1 000 000 000 Pa`.



_Error típico:_ escribir 1.5 cuando el campo espera un espesor en metros y se quería introducir 1.5 mm. La entrada correcta sería `0.0015`.



== 2. Cómo leer una fórmula sin asustarse



- `=` significa igualdad, no «causa» por sí sola.
- `Δ` significa cambio: valor final menos valor inicial.
- `Σ` significa sumar varios términos.
- `v²` significa `v × v`; `√x` es la raíz cuadrada.
- `|x|` es el valor absoluto; `‖v‖` es la longitud o magnitud de un vector.
- `∝` significa «es proporcional a», manteniendo constantes las otras condiciones especificadas.
- `q(t)` significa que q depende del instante t.
- `σ(z,t)` depende tanto del lugar dentro del cohete como del instante.



Por ejemplo, si `q = 0.5 ρ v²`, duplicar v con ρ fija multiplica q por cuatro. Si al mismo tiempo la densidad baja a la mitad, q aumenta solamente por un factor de dos. _Nunca elimines la condición “manteniendo lo demás fijo”._



== 3. Posición, velocidad y aceleración son distintas



La posición dice dónde está algo. La velocidad dice qué tan rápido cambia esa posición y hacia dónde. La aceleración dice cómo cambia la velocidad.



Para intervalos finitos:



$ v_("media") = (Delta x)/(Delta t), quad a_("media") = (Delta v)/(Delta t) $



Si en 2 s un objeto pasa de 10 a 30 m/s, su aceleración media en ese intervalo es `(30 − 10)/2 = 10 m/s²`. Eso no significa que su velocidad sea 10 m/s.



Una gráfica de altura puede seguir subiendo mientras la velocidad vertical disminuye. La pendiente de la altura representa la velocidad vertical. Una curva menos inclinada indica que sube más lentamente.



=== Apogeo y fin de combustión



- _Fin de combustión o burnout:_ el motor deja de producir empuje en el modelo.
- _Apogeo:_ punto de mayor altura de la trayectoria, donde la componente vertical de velocidad pasa por cero.



No coinciden necesariamente. Después del burnout el cohete puede seguir subiendo por su velocidad acumulada, mientras gravedad y aerodinámica cambian su movimiento.



En el apogeo _no tienen que ser cero_ la velocidad horizontal, la velocidad relativa al viento ni la presión dinámica. Tampoco tiene que desaparecer la aceleración.



== 4. Escalares y vectores



La masa es un escalar: basta un número y una unidad. La velocidad y la fuerza son vectores: además importan sus componentes y dirección.



Un vector `v = (vx, vy, vz)` puede tener rapidez:



$ V = sqrt(v_x^2 + v_y^2 + v_z^2) $



Ejemplo: componentes perpendiculares de 3 y 4 m/s dan una rapidez de 5 m/s, no 7. Sumar magnitudes no sustituye sumar vectores.



El código usa ambos tipos de cantidades: componentes con signo para calcular fuerzas y giros, y magnitudes para algunas gráficas. Un gráfico de magnitud pierde información sobre la dirección.



== 5. Dos sistemas de coordenadas y dos clases de altura



=== Coordenadas del entorno



RocketPy usa ejes horizontales y un eje vertical positivo hacia arriba. `flight.z(t)` es una altitud usada para consultar la atmósfera.



- _ASL:_ altitud sobre el nivel del mar.
- _AGL:_ altura sobre el terreno de referencia del lanzamiento.



En esta demo, el sitio está a 1400 m ASL:



$ h_("AGL") = h_("ASL") - 1400 "m" $



Por eso un apogeo de aproximadamente 4687 m ASL corresponde a 3287 m AGL. Usar 3287 como altitud atmosférica consultaría condiciones del aire a una cota equivocada.



=== Coordenadas del cuerpo



Para situar motor, nariz, masas y cortes se usa un eje axial solidario al cohete, positivo hacia la nariz. La cola del dominio está en `−1.255 m` y la punta en `+1.278 m`. El cero es una referencia del modelo, _no el nivel del mar ni el suelo_.



A medida que el cohete se inclina, su eje axial deja de coincidir con la vertical. Una fuerza lateral en ejes del cuerpo no se puede sumar directamente a una componente vertical terrestre sin transformar coordenadas.



La matriz de rotación y los cuaterniones del código sirven para traducir entre esos sistemas. No hace falta dominarlos para redactar, pero sí saber para qué están.



== 6. Masa no es peso



La masa se expresa en kg. El peso es la fuerza gravitatoria, aproximadamente:



$ W = m g $



Para un ejemplo de 20 kg y `g = 9.81 m/s²`, el peso sería 196.2 N. La masa no se vuelve 196.2 kg.



El cohete pierde masa al consumir propelente. También cambia dónde se concentra esa masa. El programa necesita actualizar ambas cosas, no solo borrar un porcentaje del peso al final.



_Carga útil añadida de 0 kg_ significa que no añadimos masa al ejemplo de referencia. No significa que el vehículo entero no tenga masa o que se haya identificado toda su carga útil original.



== 7. Las leyes de Newton y las fuerzas principales



Para un sistema de masa constante visto desde un marco inercial:



$ sum bold(F)_("externas") = m bold(a) $



La fuerza _neta_ es la suma vectorial de las fuerzas externas. Más fuerza neta sobre la misma masa implica mayor aceleración; más masa bajo la misma fuerza neta implica menor aceleración. Referencia: OpenStax, F1.



En un cohete intervienen:



- _Empuje:_ intercambio de cantidad de movimiento con los gases expulsados, representado aquí mediante el motor y su curva de empuje. No necesita «empujar contra el aire».
- _Gravedad:_ contribuye al peso.
- _Aerodinámica:_ fuerzas del aire sobre el vehículo.
- _Reacciones del riel:_ mientras está guiado; el módulo estructural actual no las reconstruye.



Para explicar un ascenso vertical idealizado puede escribirse `m a ≈ T − D − m g`, suponiendo que el empuje ya representa correctamente el efecto de la expulsión y que las direcciones son las indicadas. _No es la ecuación completa de vuelo 6-DOF ni una fórmula de la carga axial interna._



El cohete real es un sistema de masa variable. La dinámica de RocketPy considera ese problema con mayor detalle; no se obtiene simplemente aplicando todas las fórmulas de un bloque de masa constante a un cohete sin revisar sus supuestos.



=== ¿Qué son 6 grados de libertad?



Tres movimientos de traslación y tres de rotación. La orientación influye en qué aire encuentra cada superficie y en hacia dónde actúan las fuerzas. El modelo de vuelo y el modelo estructural de este proyecto tienen distinto nivel de detalle.



== 8. La velocidad que “siente” el aire



La aerodinámica depende del movimiento _relativo_ entre cohete y aire:



$ bold(v)_("rel") = bold(v)_("cohete") - bold(v)_("aire"), quad V_("rel") = abs(bold(v)_("rel")) $



Si el cohete avanza a 100 m/s en una dirección y el viento sopla a 10 m/s en la misma dirección, la rapidez relativa sería 90 m/s. Si el viento es perpendicular, se combinan componentes: no se restan 10 m/s a la rapidez directamente.



El código puede usar el vector opuesto, aire menos cohete, para describir el flujo incidente. Ambos tienen la misma magnitud, pero sus direcciones y convenciones de ángulo deben mantenerse consistentes.



Además, un punto alejado del centro de giro tiene velocidad local por la rotación. Por eso nariz y aletas no ven necesariamente el mismo flujo. `get_point_loads` incluye ese efecto al consultar fuerzas por superficie.



== 9. Atmósfera: densidad, presión y temperatura



- _Densidad ρ:_ masa de aire en un volumen.
- _Presión estática p:_ propiedad termodinámica local del aire.
- _Temperatura:_ influye, entre otras cosas, en la velocidad del sonido.



En la atmósfera estándar del ejemplo la densidad disminuye con la altitud. No es un pronóstico para un día real ni contiene ráfagas. El viento transversal de cada escenario es constante.



== 10. Presión dinámica y Max-Q



La presión dinámica se define como:



$ q = 1/2 rho V_("rel")^2 $



Ejemplo: `ρ = 1 kg/m³` y `Vrel = 100 m/s` dan `q = 5000 Pa = 5 kPa`. A 200 m/s, con igual densidad, q sería 20 kPa.



_Max-Q_ es el máximo de q a lo largo del intervalo de vuelo considerado. Al principio aumenta la velocidad; a mayor altitud suele disminuir la densidad. El máximo depende de la combinación, no solo del máximo de velocidad.



q tiene unidades de presión, pero _no es la presión real uniforme sobre toda la piel_, ni la fuerza total, ni un esfuerzo del material. Se usa para expresar la escala de las fuerzas aerodinámicas. Fuente: NASA, F3.



== 11. Arrastre, coeficientes y área de referencia



Una representación habitual del arrastre es:



$ D = q C_D A_("ref") $



- D: fuerza de arrastre en N.
- Cd: coeficiente adimensional; recoge dependencias aerodinámicas.
- Aref: área de referencia compatible con la definición del coeficiente.



Para `q = 5000 Pa`, `Cd = 0.4` y `Aref = 0.01 m²`, D sería 20 N. No se puede sustituir Aref por cualquier área sin cambiar la definición de Cd.



El _área frontal aerodinámica_ no es el _área de material del tubo_ usada para esfuerzos. Ambas se expresan en m², pero representan cosas diferentes.



Cd puede variar con Mach, geometría y otras condiciones. Esta demo lee curvas de Cd del ejemplo de RocketPy. Cambiar aletas no regenera esas curvas. Fuente de la relación: NASA, F4.



== 12. Ángulo de ataque, fuerzas normales y Mach



El _ángulo de ataque α_ representa la desalineación del eje del vehículo respecto al flujo incidente, según la convención utilizada. No es simplemente la inclinación del riel respecto al suelo.



Como intuición de ángulos pequeños, una fuerza normal puede escalar como `q Aref Cα α`. Pero el adaptador llama al cálculo de fuerzas de cada superficie de RocketPy con el flujo local; no usa exclusivamente un único α global. Si se usa la fórmula lineal, α debe estar en radianes cuando el coeficiente está definido por radián.



El _número de Mach_ es:



$ "Ma" = V_("rel") / a_s $



donde `a_s` es la velocidad local del sonido. No es la aceleración. Mach 1 significa que ambas velocidades tienen igual magnitud.



El límite Mach 1.5 configurado es un criterio de alcance del estudio. Estar debajo de ese valor no valida automáticamente todos sus modelos.



== 13. Centro de masa, centro de presión y estabilidad



El _centro de masa_ es una posición media ponderada por masas:



$ z_("CG") = (sum_i m_i z_i) / (sum_i m_i) $



No requiere que haya igual masa a cada lado: importan también las distancias. Puede desplazarse al añadir carga útil o quemar propelente.



El _centro de presión_ es una localización equivalente de la acción aerodinámica bajo una definición y condición de flujo. No es necesariamente el centro geométrico de la silueta y puede depender de Mach.



En la convención positiva hacia la nariz del modelo, el margen estático se expresa como la distancia de CG por delante de CP dividida por el diámetro. «Dos calibres» significa dos diámetros de separación, no dos metros.



Una perturbación pequeña puede producir un momento que tienda a restaurar la orientación si la disposición es apropiada. Esa es la intuición de estabilidad estática de un cohete con aletas [F5]. No garantiza buena estabilidad dinámica, amortiguamiento, trayectoria deseada o resistencia estructural.



El umbral de un calibre de esta demo es una elección de cribado. No debe presentarse como una norma universal de lanzamiento.



== 14. Relaciones que puedes defender, con sus condiciones



#table(
  columns: (0.69fr, 0.73fr, 1.58fr),
  align: (left, left, left),
  table.header([*Cambio*], [*Relación directa*], [*Lo que no se deduce automáticamente*]),
  [Duplicar Vrel con ρ fija], [q se multiplica por 4], [Que el esfuerzo máximo de toda la estructura se multiplique por 4],
  [Aumentar Cd con q y Aref fijas], [Aumenta D], [La nueva trayectoria completa; hay que resolverla],
  [Añadir masa bajo igual fuerza neta], [Disminuye la aceleración instantánea], [Que todo cohete alcance siempre menos altura; también cambian otras relaciones],
  [Cambiar posición de carga útil], [Cambia CG y puede cambiar inercia], [Un resultado universal de estabilidad sin recalcular],
  [Aumentar la altitud], [En el perfil usado disminuye ρ], [Que q siempre disminuya mientras se asciende],
  [Llegar al apogeo], [La velocidad vertical pasa por cero], [Que no haya movimiento horizontal ni cargas],
)



_Siguiente paso:_ explica por qué un cohete puede seguir ganando altura después de que su motor se apaga y por qué Max-Q no es, por definición, el máximo esfuerzo estructural. Después pasa a los cortes internos del capítulo 02.




#pagebreak(weak: true)


= 02 · Estructuras y flutter: de la fuerza externa al esfuerzo interno



Fuentes de fundamentos: F2, F6 y F7. Las simplificaciones descritas son las de structural_loads.py y flutter.py, no propiedades verificadas de un cohete real.



== 1. “Carga estructural” no es una sola magnitud



En conversación se habla de «la carga» como si fuera un número. Para calcular y redactar hay que distinguir:



#table(
  columns: (0.55fr, 1.25fr, 1.29fr),
  align: (left, left, left),
  table.header([*Concepto*], [*Ejemplo intuitivo*], [*Unidad*]),
  [Fuerza externa], [El motor empuja la estructura], [N],
  [Carga axial interna N], [Una sección transmite compresión o tracción a la siguiente], [N],
  [Cortante interno V], [Partes contiguas tienden a deslizarse transversalmente], [N],
  [Momento flector M], [La carga tiende a curvar el cuerpo], [N·m],
  [Esfuerzo normal σ], [Intensidad local de fuerza interna por área], [Pa],
  [Deformación], [Cambio de forma o tamaño], [m para desplazamientos; sin unidad para deformación relativa],
)



N se usa tanto como símbolo de la carga axial como abreviatura de la unidad newton. El contexto importa. V puede designar rapidez en aerodinámica y cortante en estructuras; esta guía usa Vrel para la primera cuando puede haber confusión.



== 2. Por qué mirar el cohete entero no basta



Imagina dos bloques unidos: uno de 3 kg delante y otro de 2 kg detrás. Empujamos el bloque trasero con 100 N, sin rozamiento ni gravedad en la dirección del movimiento.



La aceleración conjunta es `100/(3+2) = 20 m/s²`. Pero la unión no transmite 100 N al bloque delantero: transmite `3 × 20 = 60 N`, suficientes para acelerarlo. El resto de la fuerza acelera el bloque trasero.



_Conclusión:_ conocer la fuerza neta del conjunto no determina, por sí sola, la fuerza interna en cada unión. Hay que saber cómo se distribuyen las masas y las fuerzas.



Un _corte imaginario_ divide el objeto. Al aislar una parte aparecen fuerzas internas en el corte que antes se cancelaban al estudiar el conjunto completo. Esa es la idea detrás de los diagramas por sección.



En el módulo, `axial_force(flight,t)` no ofrece una fuerza única: rechaza esa formulación. La cantidad que interesa es `N(z,t)`.



== 3. Momento de fuerza: la analogía de una puerta



Abrir una puerta empujando cerca de la bisagra cuesta más que empujar lejos, para la misma fuerza y orientación. El efecto de giro depende del brazo perpendicular:



$ M = F d_perp $



Una fuerza perpendicular de 10 N aplicada a 0.5 m produce 5 N·m. En tres dimensiones se escribe `M = r × F`; el producto vectorial conserva la dirección de giro y el brazo efectivo.



Por eso no basta con sumar las magnitudes de las fuerzas de nariz y aletas: sus posiciones y signos afectan el momento. «Momento flector máximo» no significa «instante máximo»; momento es aquí una magnitud mecánica.



== 4. Viga libre, no una regla empotrada



Una regla fijada a una mesa puede transmitir fuerzas y momentos a su soporte. Un cohete después de dejar el riel no tiene ese apoyo: se traslada y gira por las fuerzas externas.



El modelo usa _alivio inercial_ para reconstruir cargas internas compatibles con ese movimiento. No añade un soporte ficticio a la cola.



=== Idea traslacional



Si las fuerzas externas suman F, una distribución de masa total m tiene aceleración específica de alivio `a = F/m`. Se añaden al cálculo fuerzas inerciales equivalentes `−mi a` en las posiciones de las masas.



Así, las cargas efectivas satisfacen:



$ sum bold(F)_("externas") + sum_i (-m_i bold(a)) = 0 $



Esto es una herramienta de cálculo; no significa que las fuerzas externas reales sean cero.



=== También hay que equilibrar el giro



Si queda un momento neto, cancelar solo la fuerza no basta. El módulo calcula una aceleración angular de alivio a partir del momento alrededor del CG y la inercia transversal equivalente. A cada masa se le asocia además la aceleración `αang × ri`.



De forma resumida:



$ bold(f)_(i,"inercial") = -m_i (bold(a) + bold(alpha)_("ang") times bold(r)_i) $



Las cargas efectivas resultantes deben cerrar tanto fuerza como momento. El programa comprueba los residuos y luego suma las fuerzas y sus brazos situados al lado de la nariz de cada corte.



_Límite:_ estas aceleraciones son las de la reconstrucción cuasiestática del módulo. No se leen como una recuperación exacta de todas las aceleraciones y términos de RocketPy. Se omiten giroscopía, centrífugas, modos flexibles y flujo de momento del propelente.



=== ¿Por qué no se añade simplemente otro m·g?



La gravedad aproximadamente uniforme acelera a todas las partes por igual. En caída libre ideal esa aceleración cancela su contribución al alivio inercial. Un objeto flotando en caída libre no soporta internamente su peso como si estuviera sobre una mesa.



RocketPy _sí incluye gravedad en el vuelo_. Lo incorrecto sería usar siempre `empuje − arrastre − peso` como compresión interna de todo el tubo. Con apoyos o gravedad no uniforme habría que revisar el tratamiento.



== 5. Qué es una distribución de masa equivalente



El ejemplo aporta masa, centro de masa e inercia agregados, pero no identifica cada batería, unión o soporte. Distintas distribuciones internas pueden compartir esos mismos valores y producir cargas locales diferentes.



El proyecto construye nodos con masas positivas:



- Una distribución equivalente de la parte seca que reproduce las propiedades agregadas de referencia.
- Masas de aletas y de carga útil añadida en posiciones explícitas.
- Una distribución equivalente del motor que cambia durante la combustión y queda dentro de sus límites axiales.



La cuadratura numérica coloca nodos y pesos para reproducir integrales. _Un nodo no es una pieza descubierta del cohete._ Aumentar el número de nodos refina la representación matemática de los mismos supuestos; no aporta datos experimentales nuevos.



La distribución del motor utiliza una familia beta acotada. Se eligen sus parámetros para reproducir masa, CG e inercia transversal. No se está afirmando que el propelente físico tenga una distribución beta.



== 6. Dos inercias distintas que comparten la letra I



=== Inercia de masa: kg·m²



Mide la resistencia a cambiar el movimiento de rotación. Para masas puntuales respecto a un eje:



$ I_("masa") = sum_i m_i r_(perp,i)^2 $



Importa al calcular cómo gira el vehículo y en el alivio angular. El modelo axial usa distancias al CG para representar la inercia transversal.



=== Segundo momento de área: m⁴



Describe cómo se distribuye el área de material en una sección. Importa en flexión. Para un tubo circular de radio exterior ro e interior ri:



$ A_("material") = pi (r_o^2 - r_i^2), quad I_A = pi/4 (r_o^4 - r_i^4) $



No se mide en kg·m² y no se puede reemplazar por la inercia de masa de RocketPy. La diferencia de unidades permite detectar esa confusión.



== 7. Fuerza, esfuerzo, rigidez y resistencia



=== Esfuerzo axial



Una fuerza axial distribuida de forma uniforme sobre una sección ideal produce:



$ sigma_("axial") = N / A_("material") $



Por ejemplo, 1000 N sobre `0.001 m²` producen 1 MPa. La misma fuerza sobre la mitad de esa área produce 2 MPa.



=== Esfuerzo de flexión



Bajo las hipótesis de viga elástica apropiadas, el esfuerzo longitudinal varía con la distancia al eje neutro:



$ abs(sigma_("flexion"))_("extremo") = (abs(M) r_o) / I_A $



Una cara tiende a comprimirse y la opuesta a traccionarse. El módulo combina las dos componentes de flexión mediante `|M| = √(Mx²+My²)`, adecuado a su sección circular equivalente.



=== Esfuerzo combinado usado



El máximo valor absoluto longitudinal en la sección ideal es:



$ sigma_("max,seccion")(z,t) = abs(N (z,t)) / A_("material") + (sqrt(M_x (z,t)^2 + M_y (z,t)^2) r_o) / I_A $



Después se busca el máximo entre secciones e instantes. No se suman, por ejemplo, una carga axial máxima de un lugar con un momento máximo de otro como si hubieran ocurrido juntos.



_No es un esfuerzo equivalente de von Mises completo._ No incorpora esfuerzo cortante, torsión, concentraciones locales o fallo de uniones. El cortante se grafica, pero no se introduce en esta expresión de esfuerzo normal.



=== Rigidez no significa resistencia



- E, módulo de Young: relaciona esfuerzo normal y deformación longitudinal en el régimen elástico lineal.
- G, módulo de corte: relaciona esfuerzo cortante y deformación angular en el régimen correspondiente.
- Fluencia: comienzo de deformación plástica según un criterio y un material.
- Pandeo: pérdida de estabilidad de una estructura comprimida, posible antes de alcanzar la fluencia.



Una regla delgada puede pandear antes de que su material «se aplaste». Comparar únicamente con fluencia no cubre ese fallo.



En este código E y G del _tubo_ se almacenan, pero no resuelven deformaciones ni aparecen en la expresión de esfuerzo anterior. `yield_strength` solo aparece en la comparación auxiliar del script 02; _no define automáticamente el umbral de selección_. El G de las _aletas_, en cambio, sí entra en flutter. Véase el mapa de parámetros.



== 8. Por qué la demo da casi el mismo esfuerzo máximo para muchos diseños



Este es uno de los resultados más importantes para interpretar honestamente el prototipo:



1. El motor es el mismo en todos los casos del barrido.
2. El empuje se aplica en la estación trasera.
3. Justo delante de esa aplicación, la sección transmite esencialmente el empuje al resto del modelo.
4. La sección tubular de comparación también es la misma.
5. En los casos calculados, esa compresión domina el máximo global, mientras la flexión es relativamente pequeña.



A 1 s el empuje usado es aproximadamente 2034 N. Con `ro = 0.0635 m` y espesor `0.0015 m`, el área de material es aproximadamente `5.91405 × 10⁻⁴ m²`. La razón `2034/A` es aproximadamente _3.439 MPa_, el máximo repetido en la malla.



Eso _no prueba_ que cambiar la masa no afecte las cargas: cambian la aceleración, los diagramas y otras secciones. Muestra que el máximo de esta representación está dominado por una condición común. Tampoco es una validación del soporte real del motor: su camino de carga no está modelado en detalle.



== 9. Vibración, resonancia y flutter no son sinónimos



- _Vibración:_ oscilación alrededor de una configuración.
- _Frecuencia natural:_ frecuencia propia de un modo, determinada por masa, rigidez y condiciones de apoyo.
- _Resonancia forzada:_ respuesta elevada ante una excitación próxima a una frecuencia relevante, dependiendo también del amortiguamiento.
- _Flutter:_ inestabilidad aeroelástica en la que el flujo y la deformación se acoplan y pueden alimentar una oscilación.



Como intuición, un sistema simple masa–resorte tiene frecuencia natural proporcional a `√(rigidez/masa)`. Esa relación _no es el cálculo de flutter implementado_ ni permite hallar por sí sola cuándo se rompe una aleta.



El módulo no anima vibraciones, no calcula frecuencias modales ni predice cuándo se desprende una aleta. Calcula una frontera empírica de velocidad y la compara con el vuelo.



== 10. Geometría de la aleta y fórmula utilizada



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



$ C_x = (c_r^2 + c_r c_t + c_t^2 + s(c_r+2c_t)) / (3(c_r+c_t)), quad epsilon = C_x/c_r - 1/4 $



La versión implementada requiere ε positivo y utiliza la revisión de Bennett [F7]:



$ V_f = a_s sqrt(N_v / D_v), quad N_v = G ("AR"+2) (delta/c_r)^3, quad D_v = (24 epsilon gamma)/pi dot p dot "AR"^3 dot (1+lambda)/2, quad gamma=1.4 $



G y p deben estar en las mismas unidades de presión. El código usa Pa; as y Vf están en m/s. La constante incluye la corrección que evita la sobreestimación por √2 discutida en esa referencia. Una prueba reproduce aproximadamente su ejemplo de 1425 ft/s.



No se debe presentar esta fórmula como válida para cualquier laminado, unión, geometría o régimen de Mach. El criterio Mach de la demo no comprueba automáticamente todas las hipótesis de la fórmula, ni valida una frontera nominal que caiga fuera de su rango de aplicación.



== 11. Relaciones de flutter, siempre con condiciones



Manteniendo la geometría restante y el estado atmosférico:



- `Vf ∝ √G`: multiplicar G por 4 multiplica Vf por 2.
- `Vf ∝ δ^(3/2)`: duplicar espesor multiplica Vf por aproximadamente 2.828.
- Con as fija, `Vf ∝ 1/√p`.
- Aumentar todas las dimensiones del plano de la aleta por un factor k, _sin aumentar su espesor_, conserva AR, λ y ε, pero reduce δ/cr. Entonces Vf escala como `k^(−3/2)` a igual atmósfera.



Eso explica por qué «aletas más grandes» no significa automáticamente «mejor resistencia al flutter». También cambia el vuelo y la masa; el margen final exige recalcular la trayectoria.



El cociente graficado es:



$ R_f (t) = (V_f (t)) / (V_("rel") (t)) $



- `Rf > 1`: velocidad calculada por debajo de la frontera nominal.
- `Rf = 1`: coincidencia con la frontera.
- `Rf < 1`: cruce de la frontera; riesgo según la aproximación.



El umbral de estudio predeterminado es 1.25, una reserva elegida para comparar, _no un requisito de seguridad validado_. Un Rf de 0.51 no significa 51% de probabilidad de fallo.



== 12. Relación especial entre flutter y Max-Q en este modelo



Con geometría y G constantes y aire ideal coherente, `as² = γ p/ρ`. Si llamamos B al factor geométrico adimensional de la fórmula, se tiene:



$ a_s^2 = gamma p/rho, quad V_f^2 = a_s^2 (G B)/p = (gamma G B)/rho, quad R_f^2 = (gamma G B)/(rho V_("rel")^2) = (gamma G B)/(2q) $



B es `(AR+2)(δ/cr)³ / [(24 ε γ/π) AR³(1+λ)/2]`. Por tanto, bajo esas hipótesis, minimizar el margen equivale a maximizar q. Pequeñas diferencias de tiempo pueden deberse al muestreo y a las interpolaciones de las funciones del programa.



_No es un descubrimiento independiente si las dos curvas coinciden:_ en esta aproximación existe esa relación matemática. Tampoco significa que Max-Q determine todos los fenómenos de flutter de una estructura flexible real. La afirmación general de que el instante de flutter «siempre es diferente de Max-Q» sería incorrecta aquí.



_Siguiente paso:_ explica por separado por qué el máximo esfuerzo global casi no cambia entre los diseños actuales y por qué las aletas delgadas reducen fuertemente su margen de flutter. Son mecanismos y métricas diferentes.




#pagebreak(weak: true)


= 03 · Programación desde cero: cómo una idea física se vuelve un cálculo



No necesitas conocer Python para empezar. El objetivo no es memorizar todas sus instrucciones, sino reconocer entradas, operaciones, decisiones y resultados. Los ejemplos son didácticos, no un sustituto del simulador.



== 1. ¿Qué es un programa?



Es una secuencia de instrucciones que una computadora ejecuta. No entiende por sí sola qué significa «un cohete seguro» ni conoce las unidades de un número si no las representamos o documentamos.



Un _algoritmo_ es el procedimiento: por ejemplo, recorrer varios instantes, calcular esfuerzo en cada sección y conservar el mayor. Python es el lenguaje con el que expresamos parte de ese procedimiento.



Una simulación es un programa que aplica un modelo a unas condiciones iniciales. Una gráfica es una representación de sus datos. Ninguna de las dos constituye una observación física por sí sola.



== 2. Archivos y carpetas



#table(
  columns: (0.55fr, 1.43fr, 1.33fr),
  align: (left, left, left),
  table.header([*Extensión*], [*Qué contiene aquí*], [*¿Es el programa de física?*]),
  [`.py`], [Instrucciones de Python], [Algunas sí; otras solo verifican o dibujan],
  [`.json`], [Datos estructurados: configuración o resultados], [No ejecuta la simulación],
  [`.csv`], [Tabla de números o resultados], [No],
  [`.png`], [Imagen de una gráfica], [No; no conserva toda la información numérica],
  [`.html`], [Página del informe, con interfaz en JavaScript], [Presenta datos; no ejecuta RocketPy en el navegador],
  [`.md`], [Documentación Markdown, como este capítulo], [No],
  [`.cjs`], [Programa de JavaScript usado para verificar la interfaz], [No calcula las cargas],
)



Un _repositorio_ guarda el código, documentación y archivos que el equipo decide versionar. Git registra cambios; GitHub aloja y permite compartir un repositorio. Subir el código no lo convierte automáticamente en una web pública ejecutable.



== 3. Terminal, intérprete y editor



- _Editor:_ permite modificar texto de archivos.
- _Terminal:_ permite ejecutar comandos del sistema.
- _Intérprete de Python:_ lee y ejecuta instrucciones Python.



Desde la raíz del proyecto, el comando de Linux:



```bash
.venv/bin/python 01_learn_api.py
```



significa «usa el Python del entorno `.venv` para ejecutar ese archivo». No debes pegar ese comando dentro de un archivo Python ni dentro del prompt `>>>`.



Los comandos para instalar y para Windows están en reproducibilidad. Para leer las gráficas ya generadas no se necesita la terminal.



== 4. Variables, asignación y operaciones



Una variable es un nombre asociado a un valor:



```python
densidad = 1.0
velocidad = 100.0
presion_dinamica = 0.5 * densidad * velocidad**2
print(presion_dinamica)
```



La salida es `5000.0`. Sabemos que son Pa porque usamos kg/m³ y m/s; Python no añade esas unidades automáticamente.



- `=` asigna un valor.
- `*` multiplica; `/` divide; `**` eleva a una potencia.
- `print` muestra un resultado.
- `==` compara igualdad, distinto de asignar.
- `^` _no_ es la operación de elevar al cuadrado en Python. En algunas clases de RocketPy se redefine con otro significado; no copies esa notación en números corrientes.



`26e9` significa `26 × 10⁹`, no «26 elevado a 9». En los archivos de configuración representa, por ejemplo, un módulo de corte en Pa.



== 5. Tipos de datos



```python
numero_de_aletas = 4
espesor_m = 0.003
nombre = "caso base"
resultado_admisible = False
sin_candidato = None
```



Son, respectivamente, entero, decimal de punto flotante, texto, booleano y ausencia de un resultado. `False` no es lo mismo que cero metros, y `None` no debería transformarse silenciosamente en «el primer diseño disponible».



Los decimales de punto flotante tienen precisión finita. Un residuo `1e-12` puede ser compatible con cero dentro de una tolerancia, pero eso no justifica ignorar un error físico grande.



== 6. Funciones: dar nombre a una operación



Una función recibe entradas y devuelve una salida:



```python
def calcular_q(densidad, velocidad):
    return 0.5 * densidad * velocidad**2

q_100 = calcular_q(1.0, 100.0)
q_200 = calcular_q(1.0, 200.0)
print(q_100, q_200)
```



Imprime `5000.0 20000.0`. Los argumentos son los valores entre paréntesis. `return` entrega el resultado a quien llamó la función; no es lo mismo que imprimirlo.



La sangría agrupa instrucciones en Python. El espacio delante de `return` no es decoración: forma parte de la estructura del programa.



== 7. Listas y bucles: repetir sin copiar el cálculo



```python
velocidades = [50.0, 100.0, 150.0]

for velocidad in velocidades:
    q = 0.5 * 1.0 * velocidad**2
    print(velocidad, q)
```



`for` recorre la lista, de una entrada a la siguiente. Las presiones serían 1250, 5000 y 11250 Pa.



El barrido de diseños hace algo conceptualmente similar, pero cada iteración construye un cohete, simula su vuelo y calcula varias métricas. No es simplemente cambiar una etiqueta sobre una misma curva.



== 8. Condiciones: decidir qué casos pasan un criterio



```python
esfuerzo_mpa = 3.4
limite_mpa = 4.0

if esfuerzo_mpa <= limite_mpa:
    print("Cumple este criterio de esfuerzo")
else:
    print("Supera este criterio de esfuerzo")
```



Este ejemplo comprueba un solo criterio. El proyecto también compara flutter, estabilidad, velocidad de salida del riel y límites del alcance del modelo.



La frase correcta es «cumple los criterios definidos», no «el programa demostró que es seguro». El sentido físico de esos criterios lo establece una persona y necesita justificación.



== 9. Diccionarios y JSON: poner nombres a los datos



```python
caso = {"payload_kg": 3.0, "fin_scale": 1.0}
print(caso["payload_kg"])
```



Un diccionario relaciona claves con valores. JSON usa una estructura parecida para guardar datos en un archivo. En JSON, los booleanos se escriben `true` y `false`; en Python, `True` y `False`.



`demo.json` describe entradas. `outputs/results.json` contiene resultados, parámetros y metadatos de una ejecución. Modificar `demo.json` _no actualiza por sí solo_ un PNG o un HTML que ya se había generado: hay que ejecutar de nuevo.



La configuración exige campos concretos; inventar una clave `velocidad_maxima` no obliga al cohete a volar a esa velocidad. Ese parámetro no existe en la interfaz actual.



== 10. Bibliotecas, módulos y API



Un _módulo_ suele ser un archivo Python importable. Una _biblioteca_ reúne herramientas reutilizables. Una _API_ es la interfaz que indica cómo usar esas herramientas: nombres de clases y funciones, argumentos y resultados.



- RocketPy: ambiente, motor, cohete y dinámica de vuelo.
- NumPy: arrays y operaciones numéricas.
- SciPy: herramientas numéricas; aquí también cuadraturas para las masas equivalentes.
- Matplotlib: genera gráficas.
- `json`, `csv`, `pathlib`, `unittest`: módulos de la biblioteca estándar de Python.



Escribir `import numpy as np` permite llamar `np.array` sin repetir el nombre completo. No significa que hayamos escrito NumPy ni que sus capacidades validen nuestras ecuaciones.



== 11. Clases y objetos: agrupar información y comportamiento



Una clase define una estructura. Un objeto es una instancia concreta. Puedes pensar en la clase como la definición de una ficha y en el objeto como una ficha rellenada.



```python
from simulation import Design

base = Design()
mas_carga = Design(payload_kg=3.0)
print(base.payload_kg, mas_carga.payload_kg)
print(mas_carga.fin_geometry)
```



`Design` es la ficha de un diseño. `base` y `mas_carga` son objetos distintos. Aún _no_ se ha simulado un vuelo con ese fragmento.



Las propiedades calculadas como `fin_geometry` y `fin_mass` derivan valores de otros campos. La anotación `payload_kg: float` comunica el tipo esperado; la validación adicional del código revisa restricciones como no aceptar una masa negativa.



En RocketPy:



```text
Environment → atmósfera, viento, sitio
SolidMotor → curva de empuje y propiedades del motor
Rocket → geometría y propiedades agregadas del vehículo
Flight → ejecución del vuelo y acceso a resultados
```



Al crear un `Flight`, RocketPy realiza la simulación. Después `flight.z(t)` permite consultar altitud a un instante, y `flight.dynamic_pressure(t)` permite consultar presión dinámica. No todas las funciones reciben tiempo: algunas curvas aerodinámicas reciben Mach. Hay que revisar la API antes de pasar un argumento.



== 12. Arrays: muchas muestras de una misma magnitud



```python
import numpy as np

velocidades = np.array([50.0, 100.0, 150.0])
presiones = 0.5 * 1.0 * velocidades**2
indice = int(np.argmax(presiones))
print(indice, presiones[indice])
```



El índice es 2 porque Python empieza a contar en cero. El máximo es 11250 Pa.



Un array de fuerzas de forma `(n, 3)` guarda n vectores de tres componentes. Un array de esfuerzos de forma `(nt, nz)` puede representar varios instantes y secciones. Confundir filas, columnas o unidades puede producir una imagen visualmente convincente pero físicamente incorrecta.



`np.max` devuelve el mayor valor. `np.argmax` devuelve su índice. Se usa ese índice para recuperar el tiempo o la posición donde ocurrió.



== 13. Cómo “avanza” una simulación



Las ecuaciones relacionan posición, velocidad, aceleración, fuerzas y estado del motor. Un método numérico aproxima su evolución con pasos temporales.



Como intuición muy básica, con una aceleración conocida durante un paso pequeño podríamos actualizar `v_nueva ≈ v_anterior + a Δt`. Esa explicación introduce la integración, pero _RocketPy no está limitado a ese sencillo paso de Euler_: usa un integrador con control de error y pasos adaptativos en esta ejecución.



Un paso adaptativo cambia su tamaño según el problema. Por eso 180 muestras solicitadas no implican 180 filas finales. El análisis añade nodos del integrador, puntos de la curva de empuje y eventos de interés.



=== Interpolación



Si tenemos dos muestras conocidas, una interpolación estima valores entre ellas. Ayuda a consultar funciones y a dibujar. No crea una medición nueva ni elimina errores del modelo. La curva suave y el mapa de color incluyen decisiones de representación numérica.



== 14. Errores y pruebas



- Error de sintaxis: la instrucción está mal escrita.
- Excepción: durante la ejecución aparece una condición inválida, por ejemplo un espesor mayor que el radio exterior.
- Error lógico o físico: el código corre, pero calcula algo incorrecto.



Una prueba verifica un comportamiento concreto:



```python
from math import isclose

q = 0.5 * 1.0 * 100.0**2
assert isclose(q, 5000.0)
```



Si la condición no se cumple, `assert` produce un error. No se debe ejecutar la verificación de este proyecto con `python -O`, porque esa opción elimina las aserciones de varios verificadores.



Las pruebas físicas del repositorio incluyen cuerpos libres que deben cerrar fuerzas y momentos y un caso axial donde la fuerza interna cambia según el corte. Pasarlas es necesario; no demuestra que la distribución interna supuesta coincida con la del cohete real.



== 15. Git, commits y colaboración



Un _commit_ registra una versión. Antes de redactar sobre resultados, el equipo debe saber a qué commit y configuración pertenecen. Cambiar el código sin regenerar las figuras puede mezclar versiones incompatibles.



Un trabajo útil para quien redacta es revisar cambios de documentación: comprobar que una limitación no se haya perdido al resumirla y que una cifra todavía corresponda al archivo citado.



El repositorio incluye una ejecución de referencia en `outputs/`. Guarda tus experimentos en carpetas como `outputs-local` para no sobrescribirla involuntariamente.



== 16. Qué no tienes que aprender todavía



Para colaborar en el texto no necesitas derivar cuaterniones, implementar LSODA ni dominar cuadraturas de Gauss-Jacobi. Sí debes reconocer que esos procedimientos existen, para qué se usan y dónde está el límite entre conocer el algoritmo y conocer físicamente el cohete.



La documentación oficial de Python F9 es una referencia posterior; advierte que su tutorial supone experiencia general de programación. Este capítulo proporciona el puente inicial.



_Siguiente paso:_ identifica en un archivo del proyecto una entrada, una operación física, una condición de descarte y una salida. Después sigue una variable completa en el capítulo 04.




#pagebreak(weak: true)


= 05 · Todas las gráficas, explicadas desde sus ejes



== Antes de interpretar cualquier curva



1. Lee qué hay en el eje horizontal y en el vertical: _no todos los gráficos tienen tiempo en horizontal_.
2. Lee las unidades; 1 kPa es 1000 Pa y 1 MPa es un millón de Pa.
3. Identifica si la curva representa un lugar fijo, el máximo entre muchos lugares o un diseño completo.
4. Revisa si el eje empieza en cero, si una curva se sale del rango o si hay puntos superpuestos.
5. Diferencia la línea dibujada, las muestras numéricas y un fenómeno físico observado.



Todas las imágenes de este capítulo provienen de la ejecución de referencia en outputs. Su configuración efectiva está aquí. El caso base es `case-004` en esta configuración: carga añadida 0 kg, aletas ×1, espesor 3 mm y viento constante de 4 m/s. Las propiedades estructurales son supuestas.



_Intervalo:_ después de salir del riel, alrededor de 0.368 s, hasta el apogeo, alrededor de 25.807 s. No interpretar el máximo mostrado como máximo de toda la misión, incluyendo riel o recuperación.



#table(
  columns: (0.55fr, 1.50fr, 1.34fr),
  align: (left, left, left),
  table.header([*Figura*], [*Pregunta principal*], [*Fuente numérica*]),
  [01], [¿Cómo evoluciona el vuelo?], [`baseline.csv`, resumen base],
  [02], [¿Cuándo son mayores las métricas de cargas?], [`baseline.csv`],
  [03], [¿Dónde se transmiten las cargas a un instante fijo?], [`critical-diagram.csv`],
  [04], [¿Cómo se distribuye el esfuerzo en espacio y tiempo?], [Matriz calculada e interpolada para visualización],
  [05], [¿Cómo se compara la velocidad con una frontera de flutter?], [`baseline.csv`, `thin-fin.csv`],
  [06], [¿Cómo se comparan diseños y por qué se descartan?], [`cases.csv`, ranking de `results.json`],
  [07], [¿Cuánto cambia el resultado al perturbar Cd?], [`drag_sensitivity` de `results.json` y vuelos adicionales],
)



Las funciones que dibujan todos los paneles están en report.py. Sus nombres de archivo y columnas están explicados en el capítulo 04.



== Figura 01: vuelo, velocidad, presión dinámica y estabilidad



#figure(image("../../outputs/01-flight.png", width: 92%), caption: [cuatro paneles de vuelo del caso base])



=== Panel superior izquierdo: altura AGL frente a tiempo



- _Horizontal:_ segundos desde la ignición.
- _Vertical:_ altura sobre el sitio de lanzamiento, en metros.
- _Curva:_ el caso base, no una comparación entre diseños.



La altura aumenta hasta aproximadamente _3287.34 m AGL_. La curva inicialmente se hace más inclinada; más tarde sigue subiendo pero se aplana. Su pendiente representa la velocidad vertical: cerca del apogeo la pendiente tiende a cero.



Que la altura continúe aumentando cuando disminuye la rapidez no es contradictorio. El cohete aún se mueve hacia arriba, pero cada vez más despacio. El final de combustión, fijado en 3.9 s para el motor del ejemplo, ocurre mucho antes del apogeo.



_No concluir:_ que el cohete alcanza 3287 m sobre el mar. Su apogeo ASL es aproximadamente _4687.34 m_, porque el sitio está a 1400 m ASL. Tampoco sabemos aquí cuánto dura su descenso.



=== Panel superior derecho: rapidez respecto al aire y al suelo



- _Horizontal:_ tiempo, s.
- _Vertical:_ rapidez, m/s.
- _Líneas:_ magnitud de velocidad relativa al aire y magnitud respecto al suelo, diferenciadas por leyenda y estilo.



Las curvas son parecidas porque el viento de 4 m/s es pequeño frente a una rapidez de unos 286 m/s, pero no son idénticas. La máxima rapidez terrestre reportada es aproximadamente _285.82 m/s_ y la máxima relativa muestreada _286.12 m/s_.



La velocidad puede empezar a disminuir antes del fin nominal de combustión: el empuje no es constante y la aceleración depende del balance de fuerzas, no solo de si el motor está encendido.



Al apogeo la rapidez total no llega necesariamente a cero. La velocidad vertical sí pasa por cero, pero quedan componentes horizontales y movimiento relativo al viento.



_No concluir:_ que son componentes verticales o que la diferencia entre las dos curvas es siempre exactamente 4 m/s. Las velocidades se restan como vectores.



=== Panel inferior izquierdo: presión dinámica



- _Horizontal:_ tiempo, s.
- _Vertical:_ q, en _kPa_.
- _Línea vertical:_ instante de Max-Q.



El máximo es aproximadamente _41.598 kPa en 3.341 s_. La relación es `q = ρ Vrel²/2`: la rapidez creciente favorece q, mientras la disminución de densidad con altitud tiende a reducirla. Después, al disminuir también la rapidez, q cae.



Esta curva explica la escala aerodinámica disponible para producir fuerzas. Para pasar de q a una fuerza se necesitan coeficientes, áreas y direcciones; para pasar a esfuerzos internos se necesitan además geometría estructural, masas y caminos de carga.



_No concluir:_ «el esfuerzo máximo es 41.598 kPa». Presión dinámica y esfuerzo del sólido no son la misma variable.



=== Panel inferior derecho: margen estático



- _Horizontal:_ tiempo, s.
- _Vertical:_ margen estático en calibres.
- _Línea horizontal:_ criterio mínimo de un calibre usado en la demo.



El mínimo del caso base es aproximadamente _2.277 calibres_, por encima del criterio. La curva puede cambiar porque se consume propelente, cambia el CG y el CP aerodinámico depende de Mach. No debe atribuirse toda la variación a una sola de esas causas sin examinarlas.



_No concluir:_ que una curva alta demuestra ausencia de flutter o de fallo del tubo. El margen estático describe una relación de estabilidad de orientación, no resistencia estructural. Tampoco «más calibres siempre es mejor» para todos los objetivos de vuelo.



_Frase posible para el informe:_ «El caso base mantiene un margen estático superior al criterio de cribado durante las muestras analizadas; este resultado no evalúa por sí solo estabilidad dinámica ni integridad estructural».



== Figura 02: historias de cargas máximas



#figure(image("../../outputs/02-load-history.png", width: 92%), caption: [esfuerzo, momento y compresión máximos a lo largo del tiempo])



Todos los paneles comparten tiempo en horizontal, pero representan métricas distintas. Cada valor de una curva es un máximo entre secciones; _la sección que lo produce puede cambiar con el tiempo_.



=== Panel superior: máximo esfuerzo longitudinal combinado



- _Vertical:_ máximo valor absoluto del esfuerzo longitudinal por sección, MPa.
- _Línea horizontal:_ límite supuesto de estudio, 4 MPa.
- _Líneas verticales:_ máximo esfuerzo y Max-Q, no dos materiales diferentes.



El máximo es aproximadamente _3.439 MPa a 1.000 s_, mientras Max-Q aparece después, cerca de 3.341 s. El mayor esfuerzo se encuentra justo delante de la estación de aplicación del empuje en la cola equivalente.



¿Por qué domina esa región? Debe transmitir esencialmente el empuje a la estructura situada delante. Con el mismo motor y área del tubo, la compresión asociada produce el máximo. La caída posterior acompaña la reducción del empuje; tras la combustión persisten otras cargas, aunque sean mucho menores.



_No concluir:_ que el límite de 4 MPa viene de un ensayo del material. Es un valor de estudio configurado. Tampoco se calculó un factor de seguridad global por estar debajo de él.



=== Panel central: mayor magnitud de momento flector



- _Vertical:_ `max_z √(Mx²+My²)`, N·m.
- _Curva:_ envolvente temporal de la flexión resultante, no esfuerzo ni desplazamiento.



El máximo de todo el intervalo es aproximadamente _3.656 N·m_. Las variaciones rápidas iniciales son variaciones de las cargas reconstruidas a partir de un vuelo con orientación y flujo local variables. Como se grafica una magnitud y además un máximo espacial, no se ve directamente el signo de cada componente ni necesariamente un único modo de giro.



_Crucial:_ estas oscilaciones _no son una simulación de las aletas vibrando_. La estructura del modelo no tiene modos flexibles. Para atribuir una frecuencia concreta a un mecanismo habría que analizar también orientación, velocidades angulares, fuerzas por superficie y resolución numérica.



La flexión puede crecer algo al final aunque q sea pequeña: también importan orientación, flujo local y brazos. No se puede deducir una fuerza normal únicamente de q. Las hipótesis aerodinámicas a ángulos grandes requieren cautela.



=== Panel inferior: máxima compresión axial



- _Vertical:_ máximo N entre cortes, en N, positivo en compresión.
- _No es:_ fuerza neta de todo el cohete, ni peso, ni esfuerzo en MPa.



El máximo inicial ronda _2034 N_ a 1 s. Que se parezca al empuje se explica por la sección trasera dominante de esta representación. Eso no implica que toda unión interior transmita exactamente esa fuerza: el corte entre dos masas muestra por qué N depende de la sección.



Se grafica máxima compresión, no máxima tracción en valor absoluto. Una curva próxima a cero no demuestra ausencia de toda carga axial en cualquier punto.



_Conclusión conjunta:_ los máximos de esfuerzo, momento y presión dinámica no son conceptos intercambiables y no deben sumarse como si ocurrieran simultáneamente en el mismo lugar.



== Figura 03: diagramas a un instante fijo



#figure(image("../../outputs/03-section-diagrams.png", width: 92%), caption: [carga axial, cortante, momento y esfuerzo por sección a 1 s])



Aquí cambia la lectura fundamental:



- _Horizontal en los cuatro paneles:_ estación axial dentro del modelo, en m.
- _Todo ocurre a un instante fijo:_ `t = 1.000 s`, elegido por el máximo esfuerzo.
- Hacia la derecha está la nariz; las posiciones negativas no son alturas bajo tierra.



=== Superior izquierdo: carga axial



Muestra cuánto esfuerzo de transmisión axial corresponde a cada corte, expresado como fuerza N. Es grande inmediatamente delante de la aplicación del empuje y cambia al atravesar las masas equivalentes y otras cargas.



Los escalones provienen de masas y fuerzas representadas en puntos. No son juntas físicas medidas. Refinar los nodos cambia la discretización de los mismos supuestos.



_Detalle de los extremos:_ se incluyen cortes numéricos ligeramente fuera y dentro de las aplicaciones puntuales. Un corte exterior puede tener resultante nula y el inmediatamente interior transmitir el empuje. Ser una viga sin empotramiento no significa que una sección donde hay fuerza aplicada deba transmitir cero carga.



=== Superior derecho: cortante resultante



- _Vertical:_ `√(Vx²+Vy²)`, N.
- Expresa la transmisión transversal interna.



Los cambios bruscos aparecen al cruzar cargas puntuales equivalentes. El cálculo conserva signos de componentes; esta gráfica muestra solamente la magnitud. Por eso no debes interpretar cada mínimo como un cambio de signo de un diagrama plano.



=== Inferior izquierdo: momento flector resultante



- _Vertical:_ magnitud del momento, N·m.
- Depende de las fuerzas y de las distancias a cada corte.



En este instante su máximo es del orden de _0.67 N·m_, mucho menor que el máximo de _3.656 N·m_ de toda la historia en la figura 02. No hay contradicción: se ha elegido el instante de mayor _esfuerzo combinado_, no el de mayor momento.



En diagramas firmados de un plano existen relaciones entre carga, cortante y pendiente del momento. No apliques mecánicamente esas relaciones a las magnitudes resultantes de dos planos representadas aquí.



=== Inferior derecho: esfuerzo longitudinal combinado



- _Vertical:_ MPa.
- Se calcula N y M en la misma sección, con A e IA del tubo supuesto.



Su máximo cerca de la cola está dominado por compresión. Una zona de mayor momento no tiene por qué ser la de mayor esfuerzo combinado si N cambia entre cortes.



_No concluir:_ que la nariz o un acople real tienen ese esfuerzo, porque el modelo compara todas las estaciones con una sección equivalente uniforme. No identifica la unión real que fallaría primero.



_Frase posible:_ «A 1 s, el modelo concentra el máximo esfuerzo longitudinal cerca de la transferencia del empuje; esta localización está condicionada por la sección uniforme y el camino de carga adoptados».



== Figura 04: mapa de esfuerzo



#figure(image("../../outputs/04-stress-map.png", width: 92%), caption: [esfuerzo longitudinal en función de estación axial y tiempo])



- _Horizontal:_ tiempo desde ignición, s.
- _Vertical:_ estación axial, m.
- _Color:_ esfuerzo longitudinal combinado, MPa, según la barra lateral.
- _Punto marcado:_ sección e instante del máximo calculado.



Una columna vertical representa el estado a un instante. Una fila horizontal permite seguir una estación a través del tiempo. Una región clara indica mayor esfuerzo, no calor, vibración, daño acumulado o probabilidad de fallo.



La región inferior temprana es más intensa porque allí domina el esfuerzo relacionado con la aplicación del empuje. Más tarde, las magnitudes disminuyen bajo las mismas hipótesis. Un color muy oscuro no distingue a simple vista entre cero y un valor pequeño.



El mapa se interpola a _101 estaciones_ para dibujar. Los cortes originales incluyen puntos a ambos lados de discontinuidades. El color no tiene la misma resolución exacta que el máximo numérico; para la cifra crítica usa el JSON o el diagrama, no el píxel más claro.



_No concluir:_ que se trata de un resultado de elementos finitos o una distribución de presión sobre una superficie tridimensional. Es un mapa de la viga axial equivalente.



== Figura 05: frontera de flutter y atmósfera



#figure(image("../../outputs/05-flutter.png", width: 92%), caption: [velocidades, márgenes de flutter, altitud ASL y densidad])



=== Superior izquierdo: velocidad frente a frontera nominal



- _Horizontal:_ tiempo, s.
- _Vertical:_ velocidad, m/s.
- _Curvas:_ rapidez relativa del caso base, frontera Vf base, frontera con espesor ×0.4 y rapidez relativa del caso delgado.



Compara siempre la rapidez y la frontera _del mismo caso_. Las aletas delgadas tienen espesor _1.2 mm_ en lugar de 3 mm. Cambian tanto la frontera empírica como la masa de aletas, por lo que se vuelve a simular su vuelo.



La reducción de espesor por un factor 0.4 reduce Vf por `0.4^(3/2) ≈ 0.253` a iguales condiciones atmosféricas y resto de geometría. El margen final no baja exactamente por ese factor porque también cambia ligeramente la trayectoria.



El cruce de líneas señala que la velocidad relativa supera la frontera nominal del caso. _No es una animación ni una predicción de desprendimiento_.



=== Superior derecho: margen Vf/Vrel



- _Vertical:_ cociente sin unidad.
- _Línea 1:_ frontera nominal.
- _Línea 1.25:_ criterio elegido para el cribado.



El caso base tiene un mínimo aproximado de _2.038_. El caso delgado tiene _0.510_, por debajo de 1. La figura muestra claramente cómo una buena altura o un esfuerzo bajo en el tubo no bastan para cumplir el chequeo de aletas.



El eje vertical está limitado para ampliar la región crítica. Cerca del inicio y del apogeo, el cociente puede superar la parte superior del dibujo porque Vrel es pequeña. Que la línea salga del marco no significa que el cálculo se interrumpa.



Bajo geometría y G constantes y atmósfera ideal coherente, la fórmula conduce a `Rf² ∝ 1/q`. Por eso el mínimo de margen se encuentra cerca de Max-Q en estos casos. La derivación y sus condiciones impiden presentarlo como un hallazgo experimental independiente.



=== Inferior izquierdo: velocidades frente a altitud



- _Horizontal:_ _altitud ASL_, m, no tiempo ni altura AGL.
- _Vertical:_ velocidad, m/s.
- _Curvas:_ rapidez relativa y Vf del caso base.



Se consultan presión y velocidad del sonido a cada altitud. En este ambiente, la frontera nominal aumenta al ascender, mientras la rapidez primero aumenta y luego disminuye. El resultado debe interpretarse junto a la trayectoria, no como una única velocidad máxima admisible en cualquier altura.



El instante crítico de flutter base se sitúa alrededor de _1898.49 m ASL_, es decir, unos _498.49 m sobre el lanzamiento_. Confundir ambas cotas alteraría la consulta de atmósfera.



=== Inferior derecho: densidad frente a altitud ASL



- _Vertical:_ densidad del aire, kg/m³.
- _Curva:_ perfil atmosférico usado, no mediciones meteorológicas de ese día.



La densidad disminuye con la altitud en el intervalo mostrado. Esa disminución influye en q y, mediante la relación termodinámica de la fórmula, en Vf. La función de flutter recibe p y velocidad del sonido, no una densidad independiente desconectada de ellas.



_No concluir:_ que la densidad de la aleta está cambiando ni que un único perfil estándar representa toda la variabilidad atmosférica real.



== Figura 06: comparación de diseños



#figure(image("../../outputs/06-design-space.png", width: 92%), caption: [apogeo frente a carga útil y frente a esfuerzo máximo])



=== Panel izquierdo: apogeo frente a carga útil añadida



- _Horizontal:_ carga adicional de 0, 3 y 6 kg.
- _Vertical:_ apogeo AGL, m.
- _Líneas:_ tres escalas de aleta.
- _Viento fijo:_ 4 m/s.



Los puntos son simulaciones distintas. Los segmentos solo ayudan a ver tendencias: _no demuestran que se hayan simulado todos los valores intermedios_.



Con aletas ×1, los apogeos son aproximadamente:



#table(
  columns: (1.09fr, 0.91fr),
  align: (right, right),
  table.header([*Masa añadida*], [*Apogeo AGL*]),
  [0 kg], [3287.34 m],
  [3 kg], [2736.00 m],
  [6 kg], [2257.13 m],
)



La tendencia es compatible con el aumento de masa bajo el mismo motor y condiciones, junto con los demás cambios acoplados que calcula el programa. No prueba una ley universal de altura decreciente para cualquier diseño.



Las aletas pequeñas alcanzan más altura en esta malla, pero _no se calculó una reducción específica de su Cd total_. No atribuir el resultado a una aerodinámica de arrastre que no se ha modelado. Además, el mejor apogeo bruto no siempre pasa los criterios.



=== Panel derecho: apogeo frente a máximo esfuerzo



- _Horizontal:_ máximo esfuerzo de cada caso, MPa.
- _Vertical:_ apogeo AGL, m.
- _Símbolos:_ casos que pasan o incumplen algún criterio.
- _Línea vertical:_ límite supuesto de 4 MPa.



Se incluyen _los dos vientos_. Hay puntos que prácticamente se superponen. Todos los máximos de esfuerzo están alrededor de _3.439 MPa_, formando una columna casi vertical; no es una frontera de Pareto estructural demostrada.



Las cruces no significan necesariamente que se superó 4 MPa. Los casos de 0 kg y aletas ×0.85 se descartan por margen estático de aproximadamente _0.903 calibres_, menor al criterio de 1, aunque su esfuerzo pase el límite.



El ranking por menor apogeo entre los dos vientos es:



#table(
  columns: (0.92fr, 0.77fr, 1.31fr),
  align: (left, right, left),
  table.header([*Diseño*], [*Menor apogeo AGL*], [*Estado relevante*]),
  [+0 kg, aletas ×0.85], [3309.70 m], [Descartado por estabilidad],
  [+0 kg, aletas ×1], [3287.34 m], [Mejor admisible de la malla],
  [+0 kg, aletas ×1.15], [3263.89 m], [Admisible, menor altura],
)



Los diseños con más masa añadida también están en el ranking completo. Si la misión requiere transportar al menos 3 kg adicionales, el criterio debe decirlo: de otro modo es esperable que una selección por altura favorezca no añadir carga.



_Conclusión honesta:_ esta figura demuestra la mecánica de filtrado y las relaciones del modelo, pero el máximo estructural global no discrimina significativamente los diseños actuales. Para justificar optimización estructural real harían falta un modelo y unos límites que representen los mecanismos relevantes.



== Figura 07: sensibilidad al Cd



#figure(image("../../outputs/07-drag-sensitivity.png", width: 92%), caption: [cambios de altura y esfuerzo al perturbar el coeficiente de arrastre])



Estos no son tres motores ni tres materiales. Se multiplica toda la curva de Cd del caso base por 0.85, 1 y 1.15, conservando las demás entradas correspondientes.



=== Panel izquierdo: altura frente a tiempo



- _Horizontal:_ tiempo, s.
- _Vertical:_ altura AGL, m.
- _Líneas:_ tres factores de Cd.



Los apogeos resultantes son aproximadamente:



#table(
  columns: (1.09fr, 0.91fr),
  align: (right, right),
  table.header([*Factor de Cd*], [*Apogeo AGL*]),
  [0.85], [3462.76 m],
  [1.00], [3287.34 m],
  [1.15], [3133.13 m],
)



A igualdad de q y área, mayor Cd significa mayor arrastre. Al resolver el vuelo completo, esa perturbación cambia la trayectoria y las propias condiciones de q. En estos tres casos, mayor Cd reduce el apogeo. Los tiempos finales difieren porque cada curva termina en su propio apogeo.



_No concluir:_ que ±15% es una incertidumbre estadística medida. Es una perturbación elegida para examinar sensibilidad, sin distribución de probabilidad asociada.



=== Panel derecho: esfuerzo máximo frente a tiempo



- _Vertical:_ esfuerzo longitudinal máximo, MPa.
- _Líneas:_ los mismos tres factores de Cd.



Las curvas iniciales prácticamente coinciden porque domina el mismo empuje transmitido por la misma sección. El máximo global sigue alrededor de _3.439 MPa_; tras la combustión se aprecian diferencias relacionadas con las cargas aerodinámicas y su transmisión en el modelo.



No se ha variado aquí la posición de aplicación del arrastre. Por tanto, este gráfico por sí solo no prueba una sensibilidad a distintos soportes o caminos de carga. Estudia _Cd_, manteniendo la aplicación de cargas definida.



_Conclusión:_ una entrada puede afectar bastante a la altura y poco al máximo global de esfuerzo que domina esta representación. «Resultado poco sensible» siempre debe acompañarse de qué métrica, qué intervalo y qué perturbación se evaluaron.



== Inspector interactivo, tabla y figura auxiliar



=== Curvas del inspector del HTML



El selector permite cambiar entre altura, rapidez relativa, esfuerzo máximo y margen de flutter para cada caso calculado. El eje horizontal es tiempo. Las unidades están en el nombre de la variable seleccionada.



Usa un subconjunto de hasta 240 muestras por caso para visualización. Para máximos precisos usa los CSV y resúmenes completos. Cambiar el selector no recalcula física.



=== Controles de selección



Modificar el límite de esfuerzo, el margen mínimo de flutter o la carga útil mínima filtra la malla existente. Las figuras PNG y el JSON guardado no cambian al mover los controles. Si nada pasa, «ningún diseño admisible» es un resultado válido; no hay que escoger uno por defecto.



La tabla combina todos los vientos definidos por diseño. Un punto verde de un escenario aislado no basta si otro escenario del mismo diseño incumple un criterio.



=== `structural_loads_calisto.png`



La genera `02_structural_loads.py` y no pertenece a las siete figuras versionadas del informe. Sus tres paneles representan esfuerzo máximo frente al tiempo, momento máximo frente al tiempo y momento frente a estación axial en el instante crítico. _El eje horizontal del tercero es posición, no tiempo._ Sus conceptos se interpretan como en las figuras 02 y 03.



== Plantilla breve para un pie de figura



#block(fill: rgb("#eef3f8"), stroke: 1pt + rgb("#5c7f9e"), radius: 4pt, inset: 9pt, width: 100%)[#text(size: 9.6pt)[_Figura X._ [Magnitud y unidad] en función de [variable y unidad] para [caso y condiciones]. Los datos se obtuvieron con [versión/configuración]. [Línea o criterio relevante]. La representación corresponde a [alcance del modelo]; no evalúa [limitación importante].]]



No dejar solamente «Gráfica de resultados». El lector debe identificar qué se calculó sin tener que reconstruir todo el programa.



_Siguiente paso:_ cada integrante redacta un pie y un párrafo de interpretación de una figura. Comprueben juntos que el párrafo distingue dato, mecanismo propuesto y límite de la conclusión.

