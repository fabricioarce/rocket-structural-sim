# 07 · Reproducibilidad y uso

[Índice](../README.md) · [Anterior: metodología](06-metodologia-y-redaccion.md) ·
[Siguiente: glosario](08-glosario-y-referencias.md)

## 1. Qué significa reproducir

Reproducir aquí significa usar el mismo código, configuración, archivos
locales y entorno para obtener los mismos resultados de referencia. No
significa que el resultado sea una medición del cohete real.

## 2. Entorno Python

Las versiones fijadas requieren un Python reciente. En Linux:

```bash
uv venv --python 3.14 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python --version
```

El entorno de referencia usó Python 3.14.7, RocketPy 1.13.0, NumPy 2.5.3,
SciPy 1.18.1 y Matplotlib 3.11.2. `uv` puede elegir un parche compatible
distinto; anótalo al publicar.

Para verificar el informe HTML se necesita Node:

```bash
node --version
node verify_report.cjs
```

## 3. Comandos de referencia

Desde la raíz:

```bash
.venv/bin/python -m unittest discover -v
.venv/bin/python run_demo.py
.venv/bin/python verify_outputs.py
node verify_report.cjs
.venv/bin/python verify_docs.py
```

`run_demo.py --quick` sirve para una comprobación rápida. `--config` permite
otra configuración y `--output` cambia la carpeta. La fase documental no
debe regenerar `outputs/`: los resultados usados aquí están congelados.

## 4. Qué comprueban los verificadores

`verify_outputs.py` confirma 18 CSV finitos y ordenados, muestras, ratios,
selección reproducible, barridos crecientes y siete PNG válidos.
`verify_report.cjs` comprueba el HTML offline, sus recursos locales, filtros y
72 curvas del inspector. `verify_docs.py` comprueba diez documentos, enlaces,
ejemplos Python, siete imágenes, cifras y hashes.

En `results.json`, las comprobaciones principales son:

| Clave | Significado |
|---|---|
| `unit_tests_passed` | pasó el gate de unittest |
| `refinement_below_5_percent` | apogeo, rapidez y ratio cambian menos de 5% |
| `algebraic_vs_resimulated_thin_fin` | comparación de aleta delgada dentro de 2% |

## 5. Salidas que se deben conservar

`results.json`, `effective-config.json`, `cases.csv`, `case-001.csv` a
`case-018.csv`, `baseline.csv`, `thin-fin.csv`, `thickness-sweep.csv`,
`material-sweep.csv`, `tests.txt`, `index.html` y las siete figuras PNG.

Los hashes de `data/` están dentro de `results.json`. Si cambian los datos del
motor, curvas de arrastre o perfil aerodinámico, la cifra deja de ser la
referencia publicada y hay que regenerar deliberadamente.

## 6. Convergencia

La prueba repite el caso base con el doble de muestras y `max_time_step=0.06`.
Compara:

- apogeo AGL;
- máxima rapidez relativa;
- ratio mínimo de flutter.

No compara una verdad analítica ni certifica una tolerancia física. La
referencia documenta el resultado de esta prueba de resolución.

## 7. Problemas habituales

- Ejecutar desde otra carpeta rompe rutas relativas de `data/`.
- Abrir el HTML sin clonar `outputs/` deja al inspector sin recursos.
- Confundir `max_speed_m_s` con `max_airspeed_m_s` cambia la interpretación.
- Cambiar `demo.json` sin regenerar resultados produce una configuración
  incoherente.
