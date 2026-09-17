"""Materiales con valores típicos de referencia, no propiedades certificadas.

El módulo G varía mucho entre fabricantes y laminados; reemplaza estos valores
por los de la ficha técnica del material que se vaya a utilizar.
"""

MATERIALS = {
    "aluminio_6061": {
        "nombre": "Aluminio 6061",
        "shear_pa": 26e9,
        "density_kg_m3": 2700,
        "fuente": "Aluminio 6061-T6, MatWeb / ASM Handbook: G ≈ 26 GPa",
    },
    "fibra_vidrio_g10": {
        "nombre": "Fibra de vidrio G10/FR4 laminada",
        "shear_pa": 4.14e9,
        "density_kg_m3": 1850,
        "fuente": "Bennett (2023) usa 600 000 psi en su ejemplo; cita un rango publicado de 425 000–1 700 000 psi (2.9–11.7 GPa)",
    },
    "fibra_carbono_laminada": {
        "nombre": "Fibra de carbono, tejido 0/90 (cortante en el plano G12)",
        "shear_pa": 4.5e9,
        "density_kg_m3": 1600,
        "fuente": "Orden de magnitud de tablas de laminados tejidos (G12 ≈ 4–5 GPa); un laminado cuasi-isótropo puede superar 20 GPa. Supuesto conservador de demostración",
    },
    "contrachapado_abedul": {
        "nombre": "Contrachapado de abedul aeronáutico",
        "shear_pa": 0.7e9,
        "density_kg_m3": 650,
        "fuente": "Wood Handbook, FPL-GTR-190 (USDA), cap. 12: módulo de cortante en el plano de contrachapado, orden de magnitud 0.6–0.9 GPa",
    },
    "acrilico_policarbonato": {
        "nombre": "Acrílico/policarbonato",
        "shear_pa": 1.0e9,
        "density_kg_m3": 1200,
        "fuente": "Derivado de G = E/(2(1+ν)) con E ≈ 2.4–3.2 GPa y ν ≈ 0.37 (MatWeb, PMMA y policarbonato)",
    },
}


def get_material(slug):
    try:
        return MATERIALS[slug]
    except KeyError as error:
        raise ValueError(f"Material desconocido: {slug}") from error
