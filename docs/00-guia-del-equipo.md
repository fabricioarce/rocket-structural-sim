# 00 · Guía del equipo: qué estamos haciendo y cómo ayudar

[Índice general](../README.md) · [Siguiente: física desde cero](01-fisica-desde-cero.md)

## 1. El proyecto en lenguaje cotidiano

Queremos relacionar dos preguntas diferentes:

1. **¿Cómo volaría un cohete con determinadas características?**
2. **¿Qué cargas tendrían que transmitirse dentro de su estructura durante ese vuelo?**

Luego preguntamos qué cambia al añadir carga útil, modificar aletas o cambiar el viento. Finalmente comparamos los diseños bajo unos límites elegidos. No basta con buscar el que llega más alto: también hay condiciones que debe cumplir.

Una analogía: un programa puede calcular a qué velocidad circula un vehículo sin calcular si se doblará su chasis. La trayectoria y la resistencia estructural son problemas relacionados, pero no son el mismo problema.

Aquí RocketPy resuelve el vuelo. El código adicional estima cargas y esfuerzos con un modelo simplificado, y compara la velocidad con una frontera empírica de flutter de las aletas.

## 2. Cuatro cosas que nunca debemos mezclar

| Categoría | Qué significa | Ejemplo aquí |
|---|---|---|
| Dato de entrada | Un número que entregamos al programa | Masa añadida de 3 kg |
| Supuesto | Una representación elegida sin haberla identificado completamente en el objeto real | Fuselaje como tubo de sección uniforme |
| Resultado calculado | Lo que produce ese modelo con esas entradas | Apogeo de un caso simulado |
| Evidencia experimental | Una observación de un objeto físico, con su método e incertidumbre | Medición con galgas durante un ensayo; **no disponible aquí** |

Una tabla llena de decimales sigue siendo una simulación. No se vuelve experimental por imprimirla en un informe.

También debemos separar:

- **Lo que se pretende conseguir:** herramienta útil para analizar relaciones de diseño.
- **Lo implementado:** demo de vuelo, cargas preliminares, flutter empírico y selección discreta.
- **Lo que falta demostrar:** que las cargas calculadas representan adecuadamente un cohete real y que el criterio de selección tiene límites físicamente justificados.

## 3. ¿Por qué no escribir otro simulador de vuelo desde cero?

Reutilizar RocketPy permite concentrar el trabajo en la relación entre vuelo y cargas, en lugar de volver a implementar atmósfera, propulsión y dinámica de vuelo. La implementación actual importa RocketPy como dependencia; no mantiene un fork.

Eso **no** significa que RocketPy entregue una distribución real de presión o conozca todos los componentes internos del cohete. El módulo estructural necesita supuestos adicionales. Sus errores y su validación son responsabilidad de este proyecto.

## 4. Qué puede aportar una persona que no programa

No necesita mantener el integrador numérico. Sí puede:

- Revisar que cada símbolo tenga definición y unidades.
- Buscar fuentes que respalden una afirmación concreta.
- Comprobar que la fuente dice realmente lo que el texto le atribuye.
- Diferenciar el problema, la justificación, los objetivos, el método y los resultados.
- Leer cada gráfica y describir qué cambia, respecto a qué y bajo qué condiciones.
- Detectar generalizaciones indebidas: de un caso a todos los cohetes, o de verificación numérica a seguridad de vuelo.
- Identificar qué datos físicos faltan y preparar preguntas para quien conoce la estructura.
- Registrar la versión del programa y la configuración de las figuras usadas en el documento.

Eso es trabajo técnico importante, no solo corregir ortografía o agregar texto para completar páginas.

## 5. Ruta de aprendizaje

### Nivel A: explicar sin fórmulas

Lee los capítulos [01](01-fisica-desde-cero.md) y [02](02-estructuras-y-flutter.md). Debes poder distinguir masa de peso, velocidad de aceleración, fuerza de esfuerzo y presión dinámica de carga estructural.

### Nivel B: explicar una relación

Practica frases condicionales: «si la densidad no cambia, duplicar la velocidad cuadruplica la presión dinámica». La condición importa: durante un vuelo cambia tanto la velocidad como la densidad.

### Nivel C: leer la evidencia

Lee [cada figura](05-graficas-explicadas.md). Localiza su variable, unidad, intervalo y limitación. Contrasta una cifra con el archivo de resultados, no solamente con la altura de una línea en la imagen.

### Nivel D: escribir

Usa [la guía de metodología y redacción](06-metodologia-y-redaccion.md). No conviertas las propuestas del capítulo en decisiones ya aprobadas: el equipo debe definir su pregunta y su alcance.

### Nivel E: seguir el programa

Los capítulos [03](03-programacion-desde-cero.md) y [04](04-codigo-y-datos.md) explican cómo una ecuación se convierte en datos y gráficas. Es útil aunque no vayas a modificar el código.

## 6. Una cadena que todos deben poder contar

```text
Carga útil, aletas, motor y ambiente
                  ↓
Masa, centro de masa, inercia y propiedades aerodinámicas
                  ↓
Vuelo: posición, velocidad, orientación y atmósfera local
                  ↓
Fuerzas externas + distribución de masa supuesta
                  ↓
Cargas internas por sección y esfuerzo longitudinal
                  ↓
Comparación con límites + margen de flutter + estabilidad
                  ↓
Selección del mejor diseño entre los casos calculados
```

Las flechas indican dependencias del cálculo. No significan que cada cambio mejore el resultado ni que todas esas dependencias estén modeladas con igual precisión.

## 7. Cómo comprobar si una explicación está completa

Antes de entregar un párrafo sobre una gráfica, responde:

1. ¿Qué pregunta intenta contestar?
2. ¿Qué se mantuvo fijo y qué cambió?
3. ¿Qué significan los ejes, las unidades y las líneas?
4. ¿El resultado es local, un máximo, un mínimo o una comparación entre diseños?
5. ¿Qué relación física puede explicar la tendencia?
6. ¿La relación está implementada aquí o solo sabemos que existe en la realidad?
7. ¿Qué conclusión no permite sacar la figura?
8. ¿Cuál es la fuente del dato o de la ecuación?

**Ejemplo de distinción crucial:** sabemos que modificar aletas puede cambiar el arrastre real; esta demo no recalcula la curva de Cd total para cada geometría. No se puede atribuir una mejora calculada a una reducción de Cd que el programa nunca calculó.

## 8. Preguntas para conversar antes de redactar la justificación

- ¿El objetivo final es una herramienta educativa, una metodología de comparación o una herramienta de diseño real?
- ¿Qué usuario concreto tendría el problema que intentamos resolver?
- ¿Qué información estructural tiene disponible ese usuario?
- ¿Qué significa «carga máxima»: fuerza, momento, esfuerzo o un criterio de fallo?
- ¿Se exige transportar alguna carga útil mínima?
- ¿Qué evidencia necesitaríamos para afirmar que el método mejora una práctica actual?

Las respuestas no están determinadas por el código. Hay que acordarlas y documentarlas; no inventarlas para que la justificación parezca completa.

**Siguiente paso:** cada integrante explica una figura con sus propias palabras usando las ocho preguntas anteriores. El equipo compara esas explicaciones antes de escribir conclusiones generales.
