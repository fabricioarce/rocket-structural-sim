# 03 · Programación desde cero: convertir una ecuación en un estudio

[Índice](../README.md) · [Anterior: flutter](02-flutter-desde-cero.md) ·
[Siguiente: código y datos](04-codigo-y-datos.md)

No necesitas conocer Python para empezar. El objetivo es reconocer entradas,
operaciones, decisiones y resultados.

## 1. Un programa y un módulo

Un programa es una secuencia de instrucciones. Un módulo `.py` guarda
funciones y clases que otros archivos pueden importar. La ejecución de
referencia la coordina `run_demo.py`; la física de la frontera está en
`flutter.py`.

## 2. Variables y unidades

```python
densidad = 1.0
velocidad = 100.0
presion_dinamica = 0.5 * densidad * velocidad**2
print(presion_dinamica)
```

La salida es `5000.0` Pa porque las entradas se expresan en kg/m³ y m/s.
Python no añade unidades automáticamente.

`26e9` significa \(26\times10^9\). En la configuración representa un módulo
de corte en Pa.

## 3. Funciones y objetos

```python
from flutter import Fin, flutter_speed

fin = Fin(0.20, 0.10, 0.12, 0.04, 0.003, 26e9)
vf = flutter_speed(fin, 80000.0, 330.0)
print(f"{vf:.1f} m/s")
```

`Fin` agrupa geometría y propiedad efectiva. `flutter_speed` recibe el objeto
y el estado atmosférico. El resultado es una cifra; su interpretación exige
revisar las hipótesis del capítulo 02.

## 4. Invertir una función

```python
from flutter import Fin, required_thickness

fin = Fin(0.20, 0.10, 0.12, 0.04, 0.003, 26e9)
thickness = required_thickness(fin, 80000.0, 330.0, 1.25 * 250.0)
print(f"{float(thickness) * 1000:.2f} mm")
```

El espesor requerido toma una velocidad objetivo. El programa también acepta
arrays de NumPy para recorrer toda una historia temporal.

## 5. Listas, bucles y barridos

```python
from flutter import Fin, flutter_speed

fin = Fin(0.20, 0.10, 0.12, 0.04, 0.003, 26e9)
for pressure in [100000.0, 80000.0, 60000.0]:
    print(pressure, flutter_speed(fin, pressure, 330.0))
```

`study.py` repite una idea similar para diseños, vientos y espesores. Un
barrido no inventa incertidumbre: solo evalúa las combinaciones que aparecen
en la configuración.

## 6. Diccionarios y resultados

```python
import json

data = json.loads(open("outputs/results.json", encoding="utf-8").read())
base = data["baseline"]
print(base["min_flutter_ratio"], base["required_thickness_mm"])
```

JSON conserva nombres junto con valores. `results.json` es más trazable que
una cifra copiada de una gráfica porque incluye configuración y resúmenes.

## 7. Decisiones y pruebas

```python
from materials import get_material

material = get_material("aluminio_6061")
if material["shear_pa"] > 20e9:
    print("módulo de referencia alto")
else:
    print("módulo de referencia bajo")
```

Las pruebas automáticas comprueban casos concretos: inversión del espesor,
escalado uniforme, selección y propiedades de masa. Una prueba pasada
verifica el código para las entradas elegidas; no convierte el modelo en una
medición.

## 8. Flujo completo

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

**Siguiente paso:** consulta el mapa de archivos en
[código y datos](04-codigo-y-datos.md), y luego aprende a leer las figuras.
