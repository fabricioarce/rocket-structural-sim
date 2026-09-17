# 00 · Guía del equipo: estudiar flutter desde cero

[Índice](../README.md) · [Siguiente: física](01-fisica-desde-cero.md)

## 1. Qué pregunta responde el proyecto

La pregunta es: **¿cómo cambia el margen nominal de flutter de las aletas
cuando cambia su espesor, material, escala o trayectoria?** El título completo
es «Estudio de flutter de aletas para un cohete de alta potencia».

RocketPy funciona como caja negra: entrega trayectoria, rapidez relativa,
altitud, presión, velocidad del sonido, Mach y estabilidad. Este repositorio
no reconstruye cargas internas ni un fuselaje equivalente. La versión anterior
se conserva en la [rama archivada](https://github.com/fabricioarce/rocket-structural-sim/tree/archive/full-structural-sim).

## 2. Roles pequeños y verificables

| Rol | Entrega |
|---|---|
| Física de vuelo | Explica unidades, atmósfera, \(q\), Max-Q y velocidad relativa |
| Aeroelasticidad | Explica geometría, \(G\), Bennett, ratio y espesor requerido |
| Programación | Mantiene ejemplos ejecutables y describe las funciones |
| Datos y gráficas | Comprueba JSON/CSV y redacta las siete figuras |
| Reproducibilidad | Registra entorno, comandos, checksums y límites |
| Integración | Revisa enlaces, cifras congeladas y cambios de alcance |

Cada contribución debe indicar qué dato usa, qué ecuación aplica y qué no
permite concluir.

## 3. Orden de lectura

1. **00:** alcance y responsabilidades.
2. **01:** movimiento, atmósfera y presión dinámica.
3. **02:** aeroelasticidad y fórmula de flutter.
4. **03:** Python mínimo para leer el código.
5. **04:** mapa de archivos y salidas.
6. **05:** lectura crítica de las figuras.
7. **06:** hipótesis, método y redacción.
8. **07:** reproducción de la ejecución congelada.
9. **08:** glosario y referencias.

## 4. Regla para redactar

Una cifra simulada debe escribirse como «el caso base produce…», no como
«el cohete tiene…». Una tendencia numérica no es una ley universal. Si la
documentación no puede decir qué variable está en cada eje, todavía no está
lista.

## 5. Primera sesión del equipo

```bash
.venv/bin/python -m unittest discover -v
.venv/bin/python verify_docs.py
```

Después, cada persona lee una figura y localiza su fuente en
`outputs/results.json` o en un CSV. No se ejecuta `run_demo.py` para editar
documentación: los resultados de esta fase son datos congelados.

**Siguiente paso:** pasa a [física desde cero](01-fisica-desde-cero.md) y
separa rapidez respecto al suelo de rapidez respecto al aire.
