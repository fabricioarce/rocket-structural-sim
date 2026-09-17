# 02 · Flutter desde cero: aeroelasticidad de una aleta

[Índice](../README.md) · [Anterior: física](01-fisica-desde-cero.md) ·
[Siguiente: programación](03-programacion-desde-cero.md)

El proyecto es un **estudio de flutter de aletas para un cohete de alta
potencia**. RocketPy es una caja negra de vuelo; este capítulo explica el
cálculo empírico posterior. La fórmula procede de Bennett (2023) y no es una
simulación modal de una estructura real.

## 1. Aeroelasticidad: por qué una aleta puede vibrar

Aeroelasticidad significa que el flujo y la deformación de una estructura se
afectan mutuamente. Una aleta puede flexionarse, torcerse y cambiar el ángulo
con el que encuentra el aire. Esa nueva orientación cambia la fuerza, y la
fuerza puede alimentar la deformación.

El flutter aparece cuando el intercambio de energía del flujo con los
movimientos supera la disipación efectiva. La palabra «aparece» aquí describe
el fenómeno físico; el código solo calcula una frontera nominal de velocidad.

## 2. Vibración, resonancia y flutter no son sinónimos

- **Vibración:** oscilación alrededor de una posición.
- **Resonancia:** respuesta grande ante una excitación cercana a una
  frecuencia natural.
- **Flutter:** inestabilidad aeroelástica autoalimentada por el acoplamiento
  entre flujo y deformación.

Una vibración no implica flutter, y una cuenta de \(V_f\) no entrega
frecuencias, amplitudes ni una película del movimiento.

## 3. Rigidez, \(G\) y torsión

En elasticidad lineal, una tensión tangencial \(\tau\) y una deformación
angular \(\gamma_s\) se relacionan aproximadamente por:

\[
\tau=G\gamma_s.
\]

El módulo de corte \(G\) tiene unidades Pa. El módulo de Young \(E\) describe
otra deformación; no aparece en la fórmula de Bennett usada aquí. **\(G\) es la
única propiedad del material que entra en esa fórmula.** La densidad se usa
para la masa del vuelo, no para calcular \(V_f\) algebraicamente.

Las cifras de `materials.py` son valores típicos de referencia, no propiedades
certificadas. Un fabricante, una orientación de fibras o una unión puede
cambiar mucho \(G\).

## 4. Geometría de la aleta

La aleta trapezoidal se describe con:

- \(c_r\): cuerda raíz.
- \(c_t\): cuerda punta.
- \(s\): barrido axial del borde delantero.
- \(b\): envergadura expuesta.
- \(t\): espesor constante.
- \(S=(c_r+c_t)b/2\): área.
- \(\mathrm{AR}=b^2/S\): relación de aspecto.
- \(\lambda=c_t/c_r\): taper o estrechamiento.

El centroide axial que usa el código es:

\[
C_x=
\frac{c_r^2+c_rc_t+c_t^2+s(c_r+2c_t)}
{3(c_r+c_t)},
\qquad
\epsilon=\frac{C_x}{c_r}-\frac14.
\]

La aproximación exige \(\epsilon>0\). Las propiedades `aspect_ratio` y `taper`
de `Fin` alimentan directamente la fórmula.

## 5. Fórmula de Bennett (2023), término por término

La velocidad nominal de flutter implementada es:

\[
V_f=a_s\sqrt{
\frac{G(\mathrm{AR}+2)(t/c_r)^3}
{(24\epsilon\gamma/\pi)\,p\,\mathrm{AR}^3(1+\lambda)/2}
}.
\]

Aquí:

| Símbolo | Significado | Unidad |
|---|---|---|
| \(V_f\) | frontera nominal de flutter | m/s |
| \(a_s\) | velocidad local del sonido | m/s |
| \(G\) | módulo de corte de la aleta | Pa |
| \(p\) | presión estática | Pa |
| \(t,c_r\) | espesor y cuerda raíz | m |
| AR, \(\lambda,\epsilon\) | relaciones geométricas | 1 |
| \(\gamma\) | razón de calores específicos | 1 |

El cociente \(t/c_r\) no tiene unidad. Presión y \(G\) deben expresarse en
las mismas unidades; el programa usa Pa.

La dependencia útil es:

\[
V_f\propto (t/c_r)^{3/2},\qquad
V_f\propto G^{1/2},\qquad
V_f\propto p^{-1/2}.
\]

AR aparece en el numerador y en el denominador, por lo que no basta con decir
«AR grande es mejor» sin evaluar toda la expresión. Bennett publica un ejemplo
de aproximadamente 1425 ft/s; los valores exactos del chequeo local están en
`test_flutter.py` y la prueba conserva esa referencia.

## 6. Ratio, margen 1.25 y Max-Q

El margen graficado es:

\[
R_f(t)=\frac{V_f(t)}{V_{\mathrm{rel}}(t)}.
\]

La demo exige \(R_f\ge 1.25\). Es un límite de comparación, no una
certificación. En la trayectoria base el mínimo es **2.0381962789**. Ocurre
cerca de Max-Q porque, bajo las hipótesis del modelo, la presión dinámica
concentra la condición aerodinámica más exigente.

Para el caso base:

| Métrica | Resultado |
|---|---:|
| \(R_f\) en Max-Q | 2.03819628 |
| \(R_f\) en máxima velocidad | 2.03884546 |

Son instantes y operaciones distintas. La diferencia pequeña no autoriza a
redondearlos como si fueran la misma variable.

## 7. Espesor requerido

`required_thickness` invierte la fórmula para una velocidad objetivo
\(V_\mathrm{objetivo}=R_\mathrm{objetivo}V_\mathrm{rel}\):

\[
t_\mathrm{req}=c_r\left[
\frac{(V_\mathrm{objetivo}/a_s)^2
(24\epsilon\gamma/\pi)p\,\mathrm{AR}^3(1+\lambda)/2}
{G(\mathrm{AR}+2)}
\right]^{1/3}.
\]

El programa aplica la expresión a toda la historia y toma el máximo. Para la
trayectoria base y \(R_\mathrm{objetivo}=1.25\), el aluminio requiere 2.17 mm;
los demás valores aparecen en README y `results.json`.

## 8. Barrido algebraico frente a resimulación

Un barrido de espesor o material reutiliza presión, sonido y rapidez de una
trayectoria y recalcula \(V_f\). Es postprocesado algebraico: **ignora el
cambio de masa de la aleta**. Sirve para comparar rápido, no para sustituir
una nueva trayectoria.

La aleta delgada de 1.2 mm sí se vuelve a simular. Su ratio re-simulado es
0.51033860; el cálculo algebraico da 0.51562740. La diferencia relativa
guardada en `results.json` es 0.01036333, inferior al 2% documentado.

## 9. Escala uniforme y relación con Max-Q

Si todas las dimensiones del plano se multiplican por \(k\), pero \(t\) no,
AR, \(\lambda\) y \(\epsilon\) permanecen iguales y \(t/c_r\) se divide por
\(k\). Por tanto:

\[
V_f\longmapsto V_f k^{-3/2}.
\]

La aleta más grande no es automáticamente más segura frente a flutter.
También cambia área y masa, y una resimulación debe estudiar esos efectos.

Con el factor geométrico \(B\) constante:

\[
a_s^2=\frac{\gamma p}{\rho},\qquad
V_f^2=a_s^2\frac{GB}{p}=\frac{\gamma GB}{\rho},
\qquad
R_f^2=\frac{\gamma GB}{\rho V_{\mathrm{rel}}^2}
=\frac{\gamma GB}{2q}.
\]

Esta es la **relación con Max-Q**: minimizar el ratio equivale a maximizar
\(q\) bajo esas hipótesis. No es una ley universal de estructuras flexibles.

## 10. Qué no dice el modelo

El módulo modela aletas trapezoidales homogéneas, espesor constante y
propiedades efectivas isótropas. No resuelve amplitud, rotura, modos,
uniones, laminados, amortiguamiento ni divergencia. Rebasar la frontera
señala riesgo según el modelo, no una rotura segura.

**Siguiente paso:** practica una evaluación de `Fin`, `flutter_speed` y
`required_thickness` en el capítulo de programación.
