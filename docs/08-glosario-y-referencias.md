# 08 · Glosario y referencias

[Índice](../README.md) · [Anterior: reproducibilidad](07-reproducibilidad.md)

## Glosario

| Término | Definición |
|---|---|
| Aeroelasticidad | Interacción entre flujo, movimiento y deformación de una superficie |
| AGL | Altura sobre el sitio de lanzamiento |
| ASL | Altitud sobre el nivel del mar |
| AR | Relación de aspecto, \(b^2/S\) |
| Arrastre | Acción aerodinámica opuesta al movimiento relativo |
| Barrido algebraico | Postprocesado que reutiliza una trayectoria |
| Burnout | Fin de combustión del motor según el modelo |
| Calibre | Diámetro de referencia usado en el margen estático |
| CG | Centro de masa |
| CP | Centro de presión aerodinámico |
| Divergencia | Inestabilidad estática aeroelástica; no la calcula este proyecto |
| Espesor requerido | Espesor inverso para alcanzar un ratio objetivo |
| Flutter | Inestabilidad aeroelástica autoalimentada por el flujo |
| \(G\) | Módulo de corte, en Pa |
| Mach | \(V_{\mathrm{rel}}/a_s\) |
| Max-Q | Máximo de la presión dinámica \(q\) |
| Ratio | \(V_f/V_{\mathrm{rel}}\) |
| Resonancia | Respuesta elevada ante una excitación cercana a una frecuencia natural |
| \(s\) | Barrido axial de la aleta |
| Taper \(\lambda\) | \(c_t/c_r\), estrechamiento |
| \(V_f\) | Frontera nominal de velocidad de flutter |
| \(V_{\mathrm{rel}}\) | Rapidez relativa al aire |
| \(\epsilon\) | Factor geométrico derivado del centroide \(C_x\) |

## Símbolos y unidades

| Símbolo | Significado | Unidad |
|---|---|---|
| \(p\) | Presión estática | Pa |
| \(q\) | Presión dinámica | Pa |
| \(\rho\) | Densidad del aire | kg/m³ |
| \(a_s\) | Velocidad del sonido | m/s |
| \(c_r,c_t\) | Cuerdas raíz y punta | m |
| \(b\) | Envergadura | m |
| \(S\) | Área de la aleta | m² |
| \(t\) | Espesor | m |
| \(\gamma\) | Razón de calores específicos | 1 |

## Referencias principales

### Bennett (2023)

John K. Bennett, *Fin Flutter Analysis Revisited (Again)*.

- https://www.nakka-rocketry.net/articles/Calculating_Fin_Flutter_Velocity_Bennett-12-23.pdf
- Fórmula corregida, geometría y ejemplo de aproximadamente 1425 ft/s.
- Verificación local: [test_flutter.py](../test_flutter.py).

### RocketPy

RocketPy Team, documentación oficial:

- https://docs.rocketpy.org/en/latest/user/first_simulation.html
- https://docs.rocketpy.org/en/latest/reference/classes/Flight.html
- https://github.com/RocketPy-Team/RocketPy

RocketPy proporciona el vuelo de la caja negra: trayectoria, rapidez, altitud,
atmósfera, Mach y estabilidad. Los archivos locales y su licencia aparecen en
`data/` y `LICENSES/`.

### MatWeb

- https://www.matweb.com/
- Fuente de consulta para órdenes de magnitud de materiales.
- No certifica las propiedades usadas en esta demostración.

### Wood Handbook

USDA Forest Products Laboratory, *Wood Handbook FPL-GTR-190*:

- https://www.fpl.fs.usda.gov/documnts/fplgtr/fpl_gtr190.pdf
- Referencia de orden de magnitud para el módulo de corte del contrachapado.

### Rama archivada

La versión histórica de alcance completo está preservada en:

https://github.com/fabricioarce/rocket-structural-sim/tree/archive/full-structural-sim

## Evidencia propia

- [Configuración efectiva](../outputs/effective-config.json)
- [Resultados congelados](../outputs/results.json)
- [Casos](../outputs/cases.csv)
- [Pruebas](../outputs/tests.txt)

Estas salidas describen una ejecución concreta. No son una garantía sobre un
vehículo físico.
