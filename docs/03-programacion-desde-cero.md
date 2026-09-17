# 03 · Programación desde cero: cómo una idea física se vuelve un cálculo

[Índice](../README.md) · [Anterior: estructuras](02-estructuras-y-flutter.md) · [Siguiente: mapa del código](04-codigo-y-datos.md)

No necesitas conocer Python para empezar. El objetivo no es memorizar todas sus instrucciones, sino reconocer entradas, operaciones, decisiones y resultados. Los ejemplos son didácticos, no un sustituto del simulador.

## 1. ¿Qué es un programa?

Es una secuencia de instrucciones que una computadora ejecuta. No entiende por sí sola qué significa «un cohete seguro» ni conoce las unidades de un número si no las representamos o documentamos.

Un **algoritmo** es el procedimiento: por ejemplo, recorrer varios instantes, calcular esfuerzo en cada sección y conservar el mayor. Python es el lenguaje con el que expresamos parte de ese procedimiento.

Una simulación es un programa que aplica un modelo a unas condiciones iniciales. Una gráfica es una representación de sus datos. Ninguna de las dos constituye una observación física por sí sola.

## 2. Archivos y carpetas

| Extensión | Qué contiene aquí | ¿Es el programa de física? |
|---|---|---|
| `.py` | Instrucciones de Python | Algunas sí; otras solo verifican o dibujan |
| `.json` | Datos estructurados: configuración o resultados | No ejecuta la simulación |
| `.csv` | Tabla de números o resultados | No |
| `.png` | Imagen de una gráfica | No; no conserva toda la información numérica |
| `.html` | Página del informe, con interfaz en JavaScript | Presenta datos; no ejecuta RocketPy en el navegador |
| `.md` | Documentación Markdown, como este capítulo | No |
| `.cjs` | Programa de JavaScript usado para verificar la interfaz | No calcula las cargas |

Un **repositorio** guarda el código, documentación y archivos que el equipo decide versionar. Git registra cambios; GitHub aloja y permite compartir un repositorio. Subir el código no lo convierte automáticamente en una web pública ejecutable.

## 3. Terminal, intérprete y editor

- **Editor:** permite modificar texto de archivos.
- **Terminal:** permite ejecutar comandos del sistema.
- **Intérprete de Python:** lee y ejecuta instrucciones Python.

Desde la raíz del proyecto, el comando de Linux:

```bash
.venv/bin/python 01_learn_api.py
```

significa «usa el Python del entorno `.venv` para ejecutar ese archivo». No debes pegar ese comando dentro de un archivo Python ni dentro del prompt `>>>`.

Los comandos para instalar y para Windows están en [reproducibilidad](07-reproducibilidad.md). Para leer las gráficas ya generadas no se necesita la terminal.

## 4. Variables, asignación y operaciones

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
- `^` **no** es la operación de elevar al cuadrado en Python. En algunas clases de RocketPy se redefine con otro significado; no copies esa notación en números corrientes.

`26e9` significa `26 × 10⁹`, no «26 elevado a 9». En los archivos de configuración representa, por ejemplo, un módulo de corte en Pa.

## 5. Tipos de datos

```python
numero_de_aletas = 4
espesor_m = 0.003
nombre = "caso base"
resultado_admisible = False
sin_candidato = None
```

Son, respectivamente, entero, decimal de punto flotante, texto, booleano y ausencia de un resultado. `False` no es lo mismo que cero metros, y `None` no debería transformarse silenciosamente en «el primer diseño disponible».

Los decimales de punto flotante tienen precisión finita. Un residuo `1e-12` puede ser compatible con cero dentro de una tolerancia, pero eso no justifica ignorar un error físico grande.

## 6. Funciones: dar nombre a una operación

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

## 7. Listas y bucles: repetir sin copiar el cálculo

```python
velocidades = [50.0, 100.0, 150.0]

for velocidad in velocidades:
    q = 0.5 * 1.0 * velocidad**2
    print(velocidad, q)
```

`for` recorre la lista, de una entrada a la siguiente. Las presiones serían 1250, 5000 y 11250 Pa.

El barrido de diseños hace algo conceptualmente similar, pero cada iteración construye un cohete, simula su vuelo y calcula varias métricas. No es simplemente cambiar una etiqueta sobre una misma curva.

## 8. Condiciones: decidir qué casos pasan un criterio

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

## 9. Diccionarios y JSON: poner nombres a los datos

```python
caso = {"payload_kg": 3.0, "fin_scale": 1.0}
print(caso["payload_kg"])
```

Un diccionario relaciona claves con valores. JSON usa una estructura parecida para guardar datos en un archivo. En JSON, los booleanos se escriben `true` y `false`; en Python, `True` y `False`.

`demo.json` describe entradas. `outputs/results.json` contiene resultados, parámetros y metadatos de una ejecución. Modificar `demo.json` **no actualiza por sí solo** un PNG o un HTML que ya se había generado: hay que ejecutar de nuevo.

La configuración exige campos concretos; inventar una clave `velocidad_maxima` no obliga al cohete a volar a esa velocidad. Ese parámetro no existe en la interfaz actual.

## 10. Bibliotecas, módulos y API

Un **módulo** suele ser un archivo Python importable. Una **biblioteca** reúne herramientas reutilizables. Una **API** es la interfaz que indica cómo usar esas herramientas: nombres de clases y funciones, argumentos y resultados.

- RocketPy: ambiente, motor, cohete y dinámica de vuelo.
- NumPy: arrays y operaciones numéricas.
- SciPy: herramientas numéricas; aquí también cuadraturas para las masas equivalentes.
- Matplotlib: genera gráficas.
- `json`, `csv`, `pathlib`, `unittest`: módulos de la biblioteca estándar de Python.

Escribir `import numpy as np` permite llamar `np.array` sin repetir el nombre completo. No significa que hayamos escrito NumPy ni que sus capacidades validen nuestras ecuaciones.

## 11. Clases y objetos: agrupar información y comportamiento

Una clase define una estructura. Un objeto es una instancia concreta. Puedes pensar en la clase como la definición de una ficha y en el objeto como una ficha rellenada.

```python
from simulation import Design

base = Design()
mas_carga = Design(payload_kg=3.0)
print(base.payload_kg, mas_carga.payload_kg)
print(mas_carga.fin_geometry)
```

`Design` es la ficha de un diseño. `base` y `mas_carga` son objetos distintos. Aún **no** se ha simulado un vuelo con ese fragmento.

Las propiedades calculadas como `fin_geometry` y `fin_mass` derivan valores de otros campos. La anotación `payload_kg: float` comunica el tipo esperado; la validación adicional del código revisa restricciones como no aceptar una masa negativa.

En RocketPy:

```text
Environment → atmósfera, viento, sitio
SolidMotor → curva de empuje y propiedades del motor
Rocket → geometría y propiedades agregadas del vehículo
Flight → ejecución del vuelo y acceso a resultados
```

Al crear un `Flight`, RocketPy realiza la simulación. Después `flight.z(t)` permite consultar altitud a un instante, y `flight.dynamic_pressure(t)` permite consultar presión dinámica. No todas las funciones reciben tiempo: algunas curvas aerodinámicas reciben Mach. Hay que revisar la API antes de pasar un argumento.

## 12. Arrays: muchas muestras de una misma magnitud

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

## 13. Cómo “avanza” una simulación

Las ecuaciones relacionan posición, velocidad, aceleración, fuerzas y estado del motor. Un método numérico aproxima su evolución con pasos temporales.

Como intuición muy básica, con una aceleración conocida durante un paso pequeño podríamos actualizar `v_nueva ≈ v_anterior + a Δt`. Esa explicación introduce la integración, pero **RocketPy no está limitado a ese sencillo paso de Euler**: usa un integrador con control de error y pasos adaptativos en esta ejecución.

Un paso adaptativo cambia su tamaño según el problema. Por eso 180 muestras solicitadas no implican 180 filas finales. El análisis añade nodos del integrador, puntos de la curva de empuje y eventos de interés.

### Interpolación

Si tenemos dos muestras conocidas, una interpolación estima valores entre ellas. Ayuda a consultar funciones y a dibujar. No crea una medición nueva ni elimina errores del modelo. La curva suave y el mapa de color incluyen decisiones de representación numérica.

## 14. Errores y pruebas

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

## 15. Git, commits y colaboración

Un **commit** registra una versión. Antes de redactar sobre resultados, el equipo debe saber a qué commit y configuración pertenecen. Cambiar el código sin regenerar las figuras puede mezclar versiones incompatibles.

Un trabajo útil para quien redacta es revisar cambios de documentación: comprobar que una limitación no se haya perdido al resumirla y que una cifra todavía corresponda al archivo citado.

El repositorio incluye una ejecución de referencia en `outputs/`. Guarda tus experimentos en carpetas como `outputs-local` para no sobrescribirla involuntariamente.

## 16. Qué no tienes que aprender todavía

Para colaborar en el texto no necesitas derivar cuaterniones, implementar LSODA ni dominar cuadraturas de Gauss-Jacobi. Sí debes reconocer que esos procedimientos existen, para qué se usan y dónde está el límite entre conocer el algoritmo y conocer físicamente el cohete.

La documentación oficial de Python [F9](08-glosario-y-referencias.md#fuentes) es una referencia posterior; advierte que su tutorial supone experiencia general de programación. Este capítulo proporciona el puente inicial.

**Siguiente paso:** identifica en un archivo del proyecto una entrada, una operación física, una condición de descarte y una salida. Después sigue una variable completa en el capítulo 04.
