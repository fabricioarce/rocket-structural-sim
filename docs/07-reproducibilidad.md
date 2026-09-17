# 07 · Usar el programa y reproducir resultados

[Índice](../README.md) · [Anterior: metodología](06-metodologia-y-redaccion.md) · [Siguiente: referencias](08-glosario-y-referencias.md)

## 1. Si solo necesitas leer y redactar

No instales herramientas innecesarias. Lee [las gráficas explicadas](05-graficas-explicadas.md) directamente en GitHub. Las siete imágenes están incluidas en el repositorio.

Para usar el informe interactivo, descarga el repositorio completo y abre `outputs/index.html` en un navegador. Mantén el HTML junto a las imágenes y CSV de su carpeta. Un enlace al archivo HTML en GitHub no equivale a una web alojada con GitHub Pages; este proyecto no configura ese servicio.

El HTML no necesita conexión para mostrar los resultados ni filtrar los casos. Los enlaces a fuentes externas sí requieren internet.

## 2. Entorno de referencia

- Python **3.14.7**, comprobado en Linux.
- RocketPy **1.13.0**.
- NumPy **2.5.3**, SciPy **1.18.1**, Matplotlib **3.11.2**.
- Dependencias fijadas en [requirements.txt](../requirements.txt).
- Node.js comprobado en versión **22.22.2**, solo para `verify_report.cjs`.

Estos son datos del entorno usado, no una afirmación de compatibilidad probada con todos los sistemas. La documentación general de RocketPy puede admitir otras versiones de Python; eso no implica que todas las dependencias fijadas aquí funcionen igual en cualquiera de ellas.

No se añaden bibliotecas para leer esta documentación. Los datos de motor, arrastre y perfil ya están en `data/`.

## 3. Instalación nueva en Linux

Requiere Git y Python 3.14 disponibles. Ejecuta esto en una carpeta donde quieras crear una copia nueva, no dentro de otra copia del proyecto:

```bash
git clone https://github.com/fabricioarce/rocket-structural-sim.git
cd rocket-structural-sim
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

`venv` crea un entorno aislado. `pip` instala las dependencias en ese entorno. La descarga inicial necesita internet; el análisis estándar posterior utiliza datos locales.

Si tu instalación de Python no incluye `venv` o `ensurepip`, resuelve ese requisito con las instrucciones de tu distribución. No cambies el Python del sistema ni elimines entornos existentes para intentar corregirlo a ciegas.

### Si ya utilizas uv

En una copia nueva, la alternativa es:

```bash
uv venv --python 3.14
uv pip install --python .venv/bin/python -r requirements.txt
```

No ejecutes ambos métodos para recrear un entorno que ya funciona. En la máquina de desarrollo el entorno `.venv` ya existe; allí basta usar su intérprete.

## 4. Equivalentes en Windows / PowerShell

Con Git y Python 3.14 instalados, en una copia nueva:

```powershell
git clone https://github.com/fabricioarce/rocket-structural-sim.git
cd rocket-structural-sim
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_demo.py --output outputs-local --open
```

Usar directamente el ejecutable del entorno evita depender de la activación de scripts de PowerShell. Estos son los comandos equivalentes por plataforma; **la ejecución de referencia se verificó en Linux, no en Windows**. Si un paquete fijado no tiene distribución compatible con tu sistema, no lo sustituyas silenciosamente: registra el problema y acuerda otro entorno reproducible.

## 5. Ejecutar y no sobrescribir la referencia

Desde la raíz del proyecto en Linux:

```bash
.venv/bin/python run_demo.py --output outputs-local --open
```

- `run_demo.py`: coordina todo el estudio.
- `--output outputs-local`: guarda una ejecución nueva en esa carpeta.
- `--open`: intenta abrir su HTML al terminar.

La carpeta versionada `outputs/` es una ejecución de referencia. El comando sin `--output` escribe allí y puede reemplazar resultados anteriores. Para experimentar, usa `outputs-local`, `outputs-mi-prueba` u otra carpeta separada. Reutilizar el mismo nombre de salida vuelve a escribir sus archivos; el programa no mantiene automáticamente un historial de ejecuciones.

Si no se abre el navegador, abre manualmente `outputs-local/index.html`. El cálculo puede haber terminado correctamente aunque el sistema no tenga un navegador predeterminado.

### Ejecución rápida

```bash
.venv/bin/python run_demo.py --quick --output outputs-quick --open
```

La opción rápida evalúa solamente el diseño base en los vientos configurados; no realiza la malla geométrica completa. Sigue incluyendo los ejemplos adicionales de sensibilidad, aletas delgadas y refinamiento. No la describas como un barrido de 18 casos.

### Ejemplos de aprendizaje

```bash
.venv/bin/python 01_learn_api.py
.venv/bin/python 02_structural_loads.py
```

El primero muestra el caso introductorio sin viento. El segundo produce `structural_loads_calisto.png`, una figura auxiliar de cargas. No son intercambiables con la ejecución completa ni deben mezclarse sus números sin revisar condiciones.

## 6. Cambiar una variable de forma controlada

1. Abre `demo.json` en un editor de texto.
2. Guarda una copia como `demo-mi-prueba.json` si necesitas preservar la configuración.
3. Cambia un parámetro y anota tu predicción antes de ejecutar.
4. Usa una carpeta de salida distinta.

```bash
.venv/bin/python run_demo.py --config demo-mi-prueba.json --output outputs-mi-prueba --open
```

La copia debe mantener todos los campos exigidos por el cargador. Usa punto decimal y las unidades del [diccionario de parámetros](04-codigo-y-datos.md).

Primeros experimentos útiles:

- Comparar `case-003` y `case-004` de la referencia para aislar el cambio de viento.
- Comparar `case-004`, `case-010` y `case-016` para la masa añadida con aletas y viento fijos.
- Comparar `case-002`, `case-004` y `case-006` para escala de aletas con masa añadida y viento fijos, recordando la limitación de Cd.
- Cambiar solo un umbral en el HTML y comprobar que las trayectorias no cambian: solo se filtran resultados.

Los identificadores anteriores solo corresponden al orden de la configuración de referencia. En otra ejecución identifica los casos por sus parámetros.

## 7. Verificaciones y lo que comprueban

### Código de cálculo

```bash
.venv/bin/python -m unittest discover -v
```

Las pruebas originales del núcleo suman 29 casos. La fuente de verdad del estado de una versión es la salida de su ejecución, no un número escrito en una página. Los nombres describen qué comportamiento se comprueba.

### Resultados exportados

```bash
.venv/bin/python verify_outputs.py outputs-local
```

Revisa series finitas, tiempos ordenados, consistencia de máximos y mínimos, reproducción de la selección, cortes exteriores y siete PNG válidos.

### Documentación y referencia versionada

```bash
.venv/bin/python verify_docs.py
```

Comprueba enlaces locales y anclas Markdown, sintaxis y ejecución de los ejemplos introductorios definidos en el capítulo 03, presencia de las siete imágenes explicadas y cifras didácticas asociadas a la ejecución de referencia. No evalúa la calidad de la justificación por el equipo ni sustituye revisión física.

### Interfaz del HTML

```bash
node verify_report.cjs outputs-local
```

Comprueba recursos, datos incrustados, lógica de selección y curvas del inspector mediante una representación DOM simplificada. **No** toma capturas de un navegador ni demuestra que todos los navegadores rendericen igual.

No uses `python -O` para verificar, porque elimina aserciones que estos verificadores necesitan.

## 8. Refinamiento numérico incluido

La demo vuelve a ejecutar el caso base con:

- El doble de muestras uniformes solicitadas.
- El doble de nodos por grupo de masa equivalente.
- Paso temporal máximo de vuelo reducido de 0.12 a 0.06 s.

Compara esfuerzo máximo, momento máximo, apogeo y margen mínimo de flutter. El cambio relativo se calcula respecto al resultado refinado. Superar el umbral del 5% produce un aviso de error al finalizar; no lo ignores aunque se hayan escrito archivos.

Cambiar simultáneamente varias resoluciones es una comprobación conjunta, no un estudio exhaustivo de convergencia temporal y espacial por separado. Tampoco establece exactitud experimental.

## 9. Registrar una ejecución para el informe escrito

Conserva:

1. Commit del código: `git rev-parse HEAD`, si se está trabajando en un clon Git.
2. `effective-config.json`, con todos los parámetros.
3. `results.json`, que contiene fecha UTC, versiones, datos resumidos, fuentes y checksums.
4. CSV originales y PNG, no solamente capturas recortadas.
5. Salida de pruebas y cualquier advertencia.
6. Una descripción de qué se cambió respecto a la referencia.

Un checksum SHA-256 ayuda a detectar si un archivo cambió. No demuestra que su contenido sea físicamente correcto ni que venga de una medición validada.

La configuración fija la fecha del ambiente en 2026-09-15 para reproducibilidad; `generated_utc` indica cuándo se ejecutó realmente el programa. Son conceptos diferentes. No se consulta un pronóstico nuevo cada vez que se ejecuta.

## 10. Problemas comunes

| Síntoma | Qué revisar |
|---|---|
| `ModuleNotFoundError: rocketpy` | Se está usando otro Python o faltó instalar dependencias en `.venv` |
| «No such file» al ejecutar un script | Carpeta actual y nombre de archivo; ejecutar desde la raíz |
| JSON inválido | Comas, comillas dobles, punto decimal; JSON no admite comentarios |
| Ningún diseño admisible | Motivos de descarte; puede ser un resultado correcto, no un fallo |
| E no cambia las figuras | E del tubo no está acoplado al cálculo de deformaciones en esta versión |
| Se cambió la configuración pero se ve la misma figura | Abrir la carpeta de la nueva ejecución y comprobar su configuración efectiva |
| Faltan imágenes del HTML | Se descargó solo el HTML o se alteró la estructura de carpetas |
| Los CSV aparecen en una sola columna | Configurar coma como separador y punto como decimal al importarlos |
| Se dice que falta un escenario de viento | Mantener listas sin duplicados y el viento base incluido en la lista |
| No se conoce el material | No inventarlo: conservar el carácter de demostración y registrar el dato pendiente |

## 11. Publicación y privacidad

Se versionan código, documentación, datos de ejemplo y resultados de referencia. No se incluyen el entorno `.venv`, cachés ni todas las ejecuciones de experimentación. Antes de añadir futuros archivos, revisa que no contengan contraseñas, tokens, información privada del equipo o material ajeno sin permiso de redistribución.

El [aviso de RocketPy](../LICENSES/RocketPy-MIT.txt) conserva la licencia de los materiales derivados de ese proyecto. Elegir una licencia para nuevas aportaciones es una decisión adicional del titular, no una consecuencia automática de subirlas a GitHub.

**Siguiente paso:** reproduce un caso o abre la referencia sin instalar nada, registra qué versión estás leyendo y verifica una cifra contra su CSV antes de incorporarla al documento del equipo.
