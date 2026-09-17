# 01 · Física desde cero: del vuelo al aire que ve la aleta

[Índice](../README.md) · [Anterior: equipo](00-guia-del-equipo.md) ·
[Siguiente: flutter](02-flutter-desde-cero.md)

Este capítulo construye el vocabulario mínimo para leer una trayectoria. No
se necesita aceptar una cifra porque «parece razonable»: primero se revisan
unidades, intervalo y definición.

## 1. Unidades y magnitudes

| Magnitud | Símbolo | Unidad |
|---|---|---|
| Tiempo | \(t\) | s |
| Posición | \(x,y,z\) | m |
| Masa | \(m\) | kg |
| Velocidad | \(\boldsymbol v\) | m/s |
| Aceleración | \(\boldsymbol a\) | m/s² |
| Fuerza | \(\boldsymbol F\) | N |
| Presión | \(p\) o \(q\) | Pa |
| Densidad | \(\rho\) | kg/m³ |

El Pascal es \(1\ \mathrm{Pa}=1\ \mathrm{N/m^2}\). Presión atmosférica y
presión dinámica tienen la misma unidad, pero no son la misma magnitud.

## 2. Posición, velocidad y aceleración

La velocidad media entre dos instantes es:

\[
\boldsymbol v_{\mathrm{media}} =
\frac{\Delta\boldsymbol r}{\Delta t}.
\]

La aceleración media es:

\[
\boldsymbol a_{\mathrm{media}} =
\frac{\Delta\boldsymbol v}{\Delta t}.
\]

RocketPy integra ecuaciones de movimiento y proporciona muestras de la
trayectoria. El proyecto consulta esas muestras; no reemplaza el integrador.

La rapidez es el tamaño de la velocidad:

\[
V = \lVert\boldsymbol v\rVert =
\sqrt{v_x^2+v_y^2+v_z^2}.
\]

## 3. Fuerzas y motor

La segunda ley resume la relación:

\[
\sum \boldsymbol F = m\boldsymbol a.
\]

En un cohete la masa cambia durante la combustión y el empuje no es
constante. Por eso una cuenta de «empuje dividido por masa inicial» solo es
una intuición. El motor local `Cesaroni_M1670.eng` y RocketPy resuelven el
vuelo de referencia.

La gravedad, el empuje y el arrastre afectan la trayectoria. La simulación
analizada empieza después de abandonar el riel y termina en el apogeo.

## 4. Velocidad respecto al aire

El viento hace que la velocidad del cohete y la del aire no sean iguales:

\[
\boldsymbol v_{\mathrm{rel}} =
\boldsymbol v_{\mathrm{cohete}}-\boldsymbol v_{\mathrm{aire}},
\qquad
V_{\mathrm{rel}}=\lVert\boldsymbol v_{\mathrm{rel}}\rVert.
\]

Flutter depende de lo que ve la aleta: \(V_{\mathrm{rel}}\), no simplemente de
la velocidad respecto al suelo. En el caso base el viento es 4 m/s, pequeño
frente a unos 286 m/s, pero no se descarta por definición.

## 5. Atmósfera y presión dinámica

La atmósfera local aporta presión estática \(p\), densidad \(\rho\) y
velocidad del sonido \(a_s\). La presión dinámica es:

\[
q=\frac12\rho V_{\mathrm{rel}}^2.
\]

Max-Q es el máximo de \(q\) en el intervalo elegido. No es una fuerza total,
ni una presión uniforme sobre toda la superficie, ni un margen de flutter.
Para convertirla en arrastre hacen falta coeficiente y área:

\[
D=q C_D A_{\mathrm{ref}}.
\]

En el caso base Max-Q es aproximadamente 41.60 kPa a 3.341 s. El valor de
salida de las funciones atmosféricas cambia con la altitud.

## 6. Ángulo de ataque, Mach y estabilidad

El ángulo de ataque describe la orientación del vehículo respecto al flujo.
Mach compara la rapidez relativa con el sonido:

\[
\mathrm{Ma}=\frac{V_{\mathrm{rel}}}{a_s}.
\]

El centro de masa (CG) resume la distribución de masa; el centro de presión
(CP) resume la acción aerodinámica del modelo. Una diferencia entre ambos,
expresada en calibres, es el margen estático. Es un criterio de orientación,
no una garantía de flutter.

## 7. Qué entrega RocketPy y qué añade este proyecto

RocketPy entrega vuelo, \(V_{\mathrm{rel}}\), altitud, \(p\), \(a_s\), Mach y
estabilidad. `flutter.py` usa esas señales para calcular \(V_f\). `study.py`
calcula el ratio, el espesor requerido y resúmenes. La aleta no se deforma
en la simulación de trayectoria.

## 8. Velocidad del sonido y por qué importa para el flutter

Para un gas ideal en la aproximación usada:

\[
a_s=\sqrt{\frac{\gamma p}{\rho}}.
\]

Al ganar altitud disminuyen \(p\) y \(\rho\), y la velocidad del sonido cambia
de forma más suave que la presión. En la fórmula de Bennett, manteniendo la
geometría:

\[
V_f\propto a_s\sqrt{\frac1p}
\quad\Longrightarrow\quad
V_f\propto\frac1{\sqrt{\rho}}.
\]

Por eso \(V_f\) puede aumentar mientras el cohete asciende aunque la presión
estática baje. El ratio final también depende de \(V_{\mathrm{rel}}\), así que
no se debe interpretar la altitud aislada.

**Siguiente paso:** en el capítulo 02 se construye la frontera de flutter
desde la geometría y el módulo de corte \(G\).
