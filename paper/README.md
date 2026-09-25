# IEEE Paper

Main manuscript: `panini_lab_ieee.tex`

Flowchart image assets:

- `figures/system_flowchart.svg`
- `figures/experiment_flowchart.svg`

## Compile

The manuscript uses XeLaTeX because it contains Devanagari and uses the `svg` package for the flowchart image assets. Install a TeX distribution with XeLaTeX and Inkscape, then run:

```bash
cd paper
xelatex -shell-escape panini_lab_ieee.tex
xelatex -shell-escape panini_lab_ieee.tex
```

For a cleaner build:

```bash
latexmk -xelatex -shell-escape panini_lab_ieee.tex
```

The local development environment did not contain XeLaTeX, latexmk, or Inkscape, so compilation must be performed in a TeX-enabled environment such as TeX Live, MacTeX, or Overleaf.

The paper intentionally distinguishes:

- validated-subset rules,
- simplified experimental-subset rules,
- internal prototype accuracy, and
- claims about the full Aṣṭādhyāyī.

Before submission, replace the placeholder author affiliation/email and verify each bibliography entry against the publisher or library record required by the target venue.
