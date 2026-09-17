#set page(
  paper: "a4",
  margin: (top: 2.4cm, bottom: 2.6cm, left: 2.2cm, right: 2.2cm),
  numbering: "1",
  header: context {
    if counter(page).get().first() > 1 {
      text(size: 8pt, fill: rgb("#777777"))[Simulador de cohetes con análisis preliminar de cargas — Guía complementaria]
      line(length: 100%, stroke: 0.4pt + rgb("#cccccc"))
    }
  },
)
#set text(lang: "es", size: 10.6pt)
#set par(justify: true, leading: 0.62em)
#set heading(numbering: none)
#set list(indent: 4pt, spacing: 0.65em)
#set enum(indent: 4pt, spacing: 0.65em)
#set table(inset: 6pt, stroke: 0.6pt + rgb("#a0a0a0"))
#show table.cell: set par(justify: false)
#show table.cell: set text(size: 9.6pt)
#set raw(theme: none)
#show raw: it => text(font: "DejaVu Sans Mono", size: 9pt, it)
#show link: it => text(fill: rgb("#0b5a86"))[#underline(it)]
#show figure.caption: it => text(size: 9pt, fill: rgb("#555555"), it)

#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(2pt)
  block(width: 100%, below: 18pt)[
    #line(length: 100%, stroke: 1.4pt + rgb("#0b5a86"))
    #v(6pt)
    #text(size: 19pt, weight: "bold", fill: rgb("#0b5a86"))[#it.body]
    #v(2pt)
    #line(length: 100%, stroke: 0.6pt + rgb("#0b5a86"))
  ]
}
#show heading.where(level: 2): it => block(above: 14pt, below: 8pt, sticky: true)[
  #text(size: 13.5pt, weight: "bold")[#it.body]
]
#show heading.where(level: 3): it => block(above: 10pt, below: 6pt, sticky: true)[
  #text(size: 11.5pt, weight: "bold", style: "italic")[#it.body]
]

// --- Portada ---
#align(center)[
  #v(2.5cm)
  #text(size: 12pt, fill: rgb("#0b5a86"))[ROCKETPY + CARGAS PRELIMINARES + FIN FLUTTER]
  #v(0.6cm)
  #text(size: 27pt, weight: "bold")[Guía complementaria del proyecto]
  #v(0.2cm)
  #text(size: 16pt)[Física, estructuras, programación y lectura de gráficas]
  #v(1.4cm)
  #block(width: 85%, fill: rgb("#fff4e6"), stroke: 1pt + rgb("#e8a33d"), radius: 5pt, inset: 14pt)[
    #text(size: 10.5pt)[
      *Estado del proyecto:* prototipo computacional verificado con pruebas numéricas,
      *no validado experimentalmente*. No autoriza fabricar ni lanzar un cohete real.
      Cubre únicamente el ascenso libre, desde el abandono del riel hasta el apogeo.
    ]
  ]
  #v(1.6cm)
  #text(size: 11pt)[Capítulos incluidos en este PDF: 01 · Física desde cero — 02 · Estructuras y flutter —]
  #v(0.1cm)
  #text(size: 11pt)[03 · Programación desde cero — 05 · Todas las gráficas, explicadas desde sus ejes]
  #v(1.6cm)
  #text(size: 10pt, fill: rgb("#555555"))[
    Repositorio completo, capítulos 00, 04, 06, 07 y 08, código y resultados de referencia: \
    #link("https://github.com/fabricioarce/rocket-structural-sim")[github.com/fabricioarce/rocket-structural-sim]
  ]
  #v(0.3cm)
  #text(size: 9.5pt, fill: rgb("#777777"))[Documento generado a partir de docs/01, docs/02, docs/03 y docs/05 del repositorio (fuente editable en docs/pdf/).]
]

#pagebreak()
#outline(title: [Contenido], indent: auto)
