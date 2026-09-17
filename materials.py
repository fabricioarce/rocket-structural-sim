"""Materiales con valores típicos de referencia, no propiedades certificadas."""

MATERIALS = {
    "aluminio_6061": {
        "nombre": "Aluminio 6061",
        "shear_pa": 26e9,
        "density_kg_m3": 2700,
        "fuente": "Bennett (2023), tabla de módulos de corte; https://www.nakka-rocketry.net/articles/Calculating_Fin_Flutter_Velocity_Bennett-12-23.pdf",
    },
    "fibra_vidrio_g10": {
        "nombre": "Fibra de vidrio G10/FR4 laminada",
        "shear_pa": 5.5e9,
        "density_kg_m3": 1850,
        "fuente": "MatWeb, G10/FR4 glass epoxy laminate, valores típicos",
    },
    "fibra_carbono_laminada": {
        "nombre": "Fibra de carbono laminada (en plano)",
        "shear_pa": 4.5e9,
        "density_kg_m3": 1600,
        "fuente": "Bennett (2023), tabla de materiales compuestos; https://www.nakka-rocketry.net/articles/Calculating_Fin_Flutter_Velocity_Bennett-12-23.pdf",
    },
    "contrachapado_abedul": {
        "nombre": "Contrachapado de abedul aeronáutico",
        "shear_pa": 0.9e9,
        "density_kg_m3": 650,
        "fuente": "Apogee Components, Peak of Flight, tablas de flutter y materiales",
    },
    "acrilico_policarbonato": {
        "nombre": "Acrílico/policarbonato",
        "shear_pa": 1.0e9,
        "density_kg_m3": 1200,
        "fuente": "MatWeb, valores típicos de PMMA y policarbonato",
    },
}


def get_material(slug):
    try:
        return MATERIALS[slug]
    except KeyError as error:
        raise ValueError(f"Material desconocido: {slug}") from error
