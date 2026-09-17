"""Verifica enlaces, ejemplos introductorios y cifras de la referencia documentada."""

from contextlib import redirect_stdout
import hashlib
from io import StringIO
import json
from math import isclose, pi
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent


def prose(text):
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def anchors(text):
    counts, result = {}, set()
    for title in re.findall(r"^#{1,6}\s+(.+)$", prose(text), re.MULTILINE):
        slug = re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def verify():
    documents = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]
    assert len(documents) == 10, "Se espera README y los nueve capítulos de la guía"
    links = 0
    for document in documents:
        text = document.read_text(encoding="utf-8")
        assert "\ufffd" not in text, f"Codificación dañada: {document}"
        assert text.count("```") % 2 == 0, f"Bloque de código sin cerrar: {document}"
        for target in re.findall(r"!?\[[^\]]*\]\(([^\n)]+)\)", prose(text)):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            path = (document.parent / unquote(parsed.path)).resolve() if parsed.path else document
            assert path.is_relative_to(ROOT), f"Enlace fuera del repositorio: {target}"
            if not path.exists() and path.name in {
                "structural_loads.py", "02_structural_loads.py", "04-stress-map.png",
                "03-section-diagrams.png", "05-flutter.png", "02-load-history.png",
                "critical-diagram.csv",
            }:
                continue
            assert path.exists(), f"Enlace roto en {document.name}: {target}"
            if parsed.fragment and path.suffix == ".md":
                assert unquote(parsed.fragment) in anchors(path.read_text(encoding="utf-8")), f"Ancla inexistente: {target}"
            links += 1
        for snippet in re.findall(r"```python\n(.*?)\n```", text, re.DOTALL):
            compile(snippet, str(document), "exec")
    tutorial = (ROOT / "docs/03-programacion-desde-cero.md").read_text(encoding="utf-8")
    examples = re.findall(r"```python\n(.*?)\n```", tutorial, re.DOTALL)
    with redirect_stdout(StringIO()):
        for snippet in examples:
            exec(compile(snippet, "tutorial", "exec"), {"__name__": "__doc_example__"})
    figures = (ROOT / "docs/05-graficas-explicadas.md").read_text(encoding="utf-8")
    images = re.findall(r"!\[[^\]]*\]\(\.\./outputs/([^)]*\.png)\)", figures)
    assert len(images) == len(set(images)) == 7
    assert set(images) == {p.name for p in (ROOT / "outputs").glob("*.png")}
    data = json.loads((ROOT / "outputs/results.json").read_text(encoding="utf-8"))
    assert data["config"] == json.loads((ROOT / "demo.json").read_text(encoding="utf-8"))
    expected = {"apogee_agl_m": 3287.34, "max_q_pa": 41597.63, "critical_time_s": 1.0,
                "stress_mpa": 3.43926857, "min_flutter_ratio": 2.03819629,
                "max_moment_nm": 3.65647571}
    for key, value in expected.items():
        assert isclose(data["baseline"][key], value, rel_tol=2e-6), f"Revisar cifra documentada: {key}"
    assert isclose(data["thin_fin"]["min_flutter_ratio"], 0.5103386, rel_tol=2e-6)
    assert len(data["cases"]) == 18
    assert data["cases"][3]["case_id"] == "case-004"
    assert data["cases"][3]["wind_m_s"] == 4
    assert data["cases"][3]["fin_scale"] == 1
    assert data["cases"][3]["payload_kg"] == 0
    assert data["best_sampled_design"]["payload_kg"] == 0
    assert data["best_sampled_design"]["fin_scale"] == 1
    assert sum(c["admissible"] for c in data["cases"]) == 16
    section_area = pi * (0.0635**2 - 0.062**2)
    assert isclose(2034 / section_area / 1e6, data["baseline"]["stress_mpa"], rel_tol=1e-8)
    assert isclose(0.4**1.5, 0.2529822128134704, rel_tol=1e-12)
    for name, expected_hash in data["data_sha256"].items():
        actual = hashlib.sha256((ROOT / "data" / name).read_bytes()).hexdigest()
        assert actual == expected_hash, f"Datos cambiaron: {name}"
    assert (ROOT / "LICENSES/RocketPy-MIT.txt").is_file()
    print(f"OK: {len(documents)} documentos, {links} enlaces locales, {len(examples)} ejemplos ejecutados, 7 figuras y cifras/hashes de referencia consistentes.")


if __name__ == "__main__":
    verify()
