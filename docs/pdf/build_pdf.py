"""Convierte los capítulos 01, 02, 03 y 05 de docs/ a un PDF único con Typst.

Uso, desde la raíz del repositorio:
  uv venv .venv-docs && uv pip install --python .venv-docs/bin/python typst
  .venv-docs/bin/python docs/pdf/build_pdf.py
  .venv-docs/bin/python -c "import typst; typst.compile('docs/pdf/guia-simulador-cohetes.typ', root='.', output='docs/pdf/guia-simulador-cohetes.pdf')"

Entorno separado del simulador (typst no es una dependencia de cálculo).
Las siete imágenes se referencian directamente desde outputs/ (ruta relativa
../../outputs/), sin duplicar los PNG dentro de docs/pdf/.

Las fórmulas LaTeX delimitadas por \\[ \\] de los capítulos 01 y 02 se traducen
a mano a sintaxis de Typst (listas MATH_01/MATH_02, en el mismo orden en que
aparecen en cada archivo) porque una conversión automática no es fiable para
fórmulas físicas. El Markdown de docs/ sigue siendo la referencia principal.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DOCS = ROOT / "docs"
OUT = Path(__file__).resolve().parent

MATH_01 = [
    r'$ bold(v)_("media") = (Delta bold(r))/(Delta t) $',
    r'$ bold(a)_("media") = (Delta bold(v))/(Delta t) $',
    r'$ V = sqrt(v_x^2 + v_y^2 + v_z^2) $',
    r'$ sum bold(F)_("externas") = m bold(a) $',
    r'$ bold(v)_("rel") = bold(v)_("cohete") - bold(v)_("aire"), quad V_("rel") = abs(bold(v)_("rel")) $',
    r'$ q = 1/2 rho V_("rel")^2 $',
    r'$ D = q C_D A_("ref") $',
    r'$ "Ma" = V_("rel") / a_s $',
    r'$ a_s = sqrt(gamma p/rho) $',
    r'$ V_("f") "∝" a_s sqrt(1/p), quad V_("f") "∝" 1/sqrt(rho) $',
]

MATH_02 = [
    r'$ tau = G gamma_s $',
    r'$ C_x = (c_r^2 + c_r c_t + c_t^2 + s(c_r+2c_t)) / (3(c_r+c_t)), quad epsilon = C_x/c_r - 1/4 $',
    (r'$ V_f = a_s sqrt(N_v / D_v), quad '
     r'N_v = G ("AR"+2) (delta/c_r)^3, quad '
     r'D_v = (24 epsilon gamma)/pi dot p dot "AR"^3 dot (1+lambda)/2, quad gamma=1.4 $'),
    r'$ V_("f") "∝" (t/c_r)^(3/2), quad V_("f") "∝" G^(1/2), quad V_("f") "∝" p^(-1/2) $',
    r'$ R_f (t) = (V_f (t)) / (V_("rel") (t)) $',
    (r'$ t_("req") = c_r ((V_("objetivo")/a_s)^2 '
     r'dot (24 epsilon gamma/pi) dot p dot "AR"^3 dot (1+lambda)/2 '
     r'/ (G dot ("AR"+2)))^(1/3) $'),
    r'$ V_f -> V_f k^(-3/2) $',
    (r'$ a_s^2 = gamma p/rho, quad '
     r'V_f^2 = a_s^2 (G B)/p = (gamma G B)/rho, quad '
     r'R_f^2 = (gamma G B)/(rho V_("rel")^2) = (gamma G B)/(2q) $'),
]

CHAPTERS = [
    ("01-fisica-desde-cero.md", MATH_01),
    ("02-flutter-desde-cero.md", MATH_02),
    ("03-programacion-desde-cero.md", []),
    ("05-graficas-explicadas.md", []),
]


def esc(text):
    """Escapa caracteres especiales de Typst en texto plano (fuera de code/math)."""
    return re.sub(r"([#$@])", r"\\\1", text)


def latex_inline(text):
    """Reduce comandos LaTeX frecuentes a expresiones matemáticas de Typst."""
    text = re.sub(r"\\(?:mathrm|text)\{([^{}]*)\}", r'"\1"', text)
    text = re.sub(r"\\boldsymbol\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\boldsymbol\s*", "", text)
    text = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", text)
    text = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", text)
    text = re.sub(r"([_^])\{([^{}]*)\}", r"\1(\2)", text)
    replacements = {
        r"\min": "min",
        r"\,": " ",
        r"\times": " dot ",
        r"\propto": " ∝ ",
        r"\ge": ">=",
        r"\le": "<=",
        r"\rho": "rho",
        r"\gamma": "gamma",
        r"\lambda": "lambda",
        r"\epsilon": "epsilon",
        r"\tau": "tau",
        r"\pi": "pi",
        r"\ ": " ",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def inline(text):
    """Convierte negrita/cursiva/enlaces/código en una línea o celda a sintaxis Typst."""
    parts = re.split(r"(`[^`]*`)", text)
    for i, part in enumerate(parts):
        if part.startswith("`"):
            continue
        part = esc(part)
        part = re.sub(
            r"\\\((.+?)\\\)",
            lambda match: f"${latex_inline(match.group(1)).strip()}$",
            part,
        )
        part = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'#link("\2")[\1]', part)
        part = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", part)
        part = re.sub(r"\*\*(.+?)\*\*", r"*\1*", part)
        part = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"_\1_", part)
        parts[i] = part
    return "".join(parts)


def table_block(lines):
    rows = [ln.strip() for ln in lines if ln.strip()]
    header = [c.strip() for c in rows[0].strip("|").split("|")]
    aligns = [c.strip() for c in rows[1].strip("|").split("|")]
    body = [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]
    align_map = []
    for a in aligns:
        if a.endswith(":") and a.startswith(":"):
            align_map.append("center")
        elif a.endswith(":"):
            align_map.append("right")
        else:
            align_map.append("left")
    widths = [max(len(re.sub(r"[`*_\[\]()]", "", header[c])),
                  *(len(re.sub(r"[`*_\[\]()]", "", body[r][c])) for r in range(len(body))))
              if body else len(header[c]) for c in range(len(header))]
    total = sum(widths) or len(header)
    cols = ", ".join(f"{max(w / total * len(header), 0.55):.2f}fr" for w in widths)
    out = [f"#table(\n  columns: ({cols}),",
           f"  align: ({', '.join(align_map)}),",
           "  table.header(" + ", ".join(f"[*{inline(h)}*]" for h in header) + "),"]
    for row in body:
        out.append("  " + ", ".join(f"[{inline(c)}]" for c in row) + ",")
    out.append(")")
    return "\n".join(out)


def convert(md_text, math_queue):
    md_text = re.sub(r"^\[Índice\].*\n\n?", "", md_text, flags=re.MULTILINE)
    md_text = md_text.replace("\u20d7", "")  # flecha combinante sobre vectores: sin glifo en el tipo usado para código
    lines = md_text.split("\n")
    out, i, math_i = [], 0, 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            out.append("")
            i += 1
            continue
        if line.startswith("$$") or line.startswith(r"\["):
            closing = "$$" if line.startswith("$$") else r"\]"
            end = i + 1
            while not lines[end].startswith(closing):
                end += 1
            out.append(math_queue[math_i])
            math_i += 1
            i = end + 1
            continue
        if line.startswith("```"):
            end = i + 1
            while not lines[end].startswith("```"):
                end += 1
            out.append("\n".join(lines[i:end + 1]))
            i = end + 1
            continue
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            text = line[level:].strip()
            out.append(("=" * level) + " " + inline(text))
            i += 1
            continue
        if line.startswith("!["):
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            name = Path(m.group(2)).name
            alt = re.sub(r"^Figura\s*\d+\s*:\s*", "", m.group(1))
            out.append(f'#figure(image("../../outputs/{name}", width: 92%), caption: [{esc(alt)}])')
            i += 1
            continue
        if line.startswith("> "):
            body = []
            while i < len(lines) and lines[i].startswith(">"):
                body.append(lines[i][1:].strip())
                i += 1
            out.append(callout(inline(" ".join(body)), "cita"))
            continue
        if line.strip().startswith("|"):
            end = i
            while end < len(lines) and lines[end].strip().startswith("|"):
                end += 1
            out.append(table_block(lines[i:end]))
            i = end
            continue
        if re.match(r"^(-|\d+\.)\s", line):
            end = i
            while end < len(lines) and (re.match(r"^(-|\d+\.)\s", lines[end]) or
                                        (lines[end].startswith("  ") and lines[end].strip())):
                end += 1
            block = lines[i:end]
            items = []
            for ln in block:
                if re.match(r"^\s*(-|\d+\.)\s", ln):
                    items.append(ln)
                else:
                    items[-1] += " " + ln.strip()
            out.append("\n".join(re.sub(r"^(\s*)(-|\d+\.)\s+(.*)$", lambda m: f"{m.group(1)}{m.group(2)} {inline(m.group(3))}", ln) for ln in items))
            i = end
            continue
        para = [line]
        j = i + 1
        while j < len(lines) and lines[j].strip() and not lines[j].startswith(("#", "```", "$$", "![", "|", "- ", "> ")) and not re.match(r"^\d+\.\s", lines[j]):
            para.append(lines[j])
            j += 1
        text = inline(" ".join(s.strip() for s in para))
        if text.startswith("*No concluir:*") or text.startswith("*Detalle de los extremos:*"):
            out.append(callout(text, "aviso"))
        elif text.startswith("*Siguiente paso:*"):
            out.append(callout(text, "paso"))
        else:
            out.append(text)
        i = j
    assert math_i == len(math_queue), f"Sobraron {len(math_queue) - math_i} fórmulas sin usar"
    return "\n\n".join(out)


def callout(body, kind):
    colors = {
        "aviso": ("#fff4e6", "#e8a33d"),
        "paso": ("#eaf6ee", "#3f9f5f"),
        "cita": ("#eef3f8", "#5c7f9e"),
    }
    fill, stroke = colors[kind]
    return f'#block(fill: rgb("{fill}"), stroke: 1pt + rgb("{stroke}"), radius: 4pt, inset: 9pt, width: 100%)[#text(size: 9.6pt)[{body}]]'


def main():
    preamble = (OUT / "preamble.typ").read_text(encoding="utf-8")
    body = [preamble]
    for filename, math_queue in CHAPTERS:
        text = (DOCS / filename).read_text(encoding="utf-8")
        body.append(f"\n#pagebreak(weak: true)\n")
        body.append(convert(text, list(math_queue)))
    (OUT / "guia-simulador-cohetes.typ").write_text("\n\n".join(body), encoding="utf-8")
    print("Escrito docs/pdf/guia-simulador-cohetes.typ")


if __name__ == "__main__":
    main()
