# AGENT.md

## Project overview

This project is a Python-first math document generation package that renders directly to Typst. The goal is to make it easy to create polished math tests, quizzes, worksheets, handouts, and answer keys using Python objects rather than hand-written LaTeX or manually inserted screenshots.

The core idea is:

```text
Python object model
    -> generated figures/assets
    -> generated Typst source
    -> Typst PDF output
```

The package should prioritize reproducibility, clean layout abstractions, reusable problem components, generated answer keys, and easy integration with Python math/graphics tools such as SymPy, NumPy, Matplotlib, Plotly, Manim, and custom SVG generation.

The long-term aim is a publishable Python package for math educators, curriculum writers, and technically inclined teachers who want programmatic control over assessment generation without fighting LaTeX.

## Primary use case

A user should be able to write Python like this:

```python
from mathpaper import Test, MultipartProblem, Part
from mathpaper.content import Math
from mathpaper.layout import PartsGrid, SideFigure
from mathpaper.figures import CoordinatePlane
from mathpaper.math import polynomial_from_roots

poly = polynomial_from_roots([-3, 1, 4])

graph = CoordinatePlane(
    xlim=(-6, 6),
    ylim=(-10, 10),
    grid=True,
    axes=True,
).plot(poly)

quiz = Test(
    title="Polynomial Quiz",
    course="Algebra 2",
    version="A",
)

quiz.add(
    MultipartProblem(
        prompt="Use the graph of $f$ to answer the questions.",
        figure=graph,
        figure_layout=SideFigure(position="right", width="42%"),
        parts=[
            Part("Find all real zeros.", answer=Math(r"-3, 1, 4")),
            Part("Find the y-intercept.", answer=Math(r"12")),
            Part("State the end behavior."),
            Part("Where is $f(x) > 0$?"),
        ],
        layout=PartsGrid(columns=2, answer_space="0.9in"),
        points=8,
    )
)

quiz.build("out/polynomial_quiz")
```

Expected output:

```text
out/polynomial_quiz/
  main.typ
  main.pdf
  answer_key.typ
  answer_key.pdf
  assets/
    graph_001.svg
  manifest.json
```

The package should make common math-document tasks natural:

- Numbered problems.
- Multipart problems with parts `a`, `b`, `c`, etc.
- Multi-column part layouts.
- Answer spaces.
- Side figures and top/bottom figures.
- Student versions and answer keys.
- Generated graphs and diagrams.
- Reproducible random problem variants.
- Clean, inspectable Typst source.

## Major design decision

This package should use **Python -> Typst directly**.

Rationale:

- Typst is the actual page/layout/typesetting engine.
- Direct Typst generation gives better control over tests, worksheets, columns, figures, answer spaces, and page layout.
- Python should own generation, asset creation, seeding, problem selection, and answer-key construction.
- Typst should own page layout, typography, grids, spacing, headers, footers, and PDF rendering.

## Public API philosophy

The stable public API should be the **Python object model**, not raw Typst strings.

Good public API:

```python
Test(...)
Problem(...)
MultipartProblem(...)
Part(...)
PartsGrid(...)
SideFigure(...)
AnswerSpace(...)
Figure(...)
Math(...)
RawTypst(...)
TypstRenderer(...)
TypstTheme(...)
quiz.to_typst()
quiz.write_typst(...)
quiz.build(...)
```

Avoid making low-level renderer functions part of the stable API:

```python
_render_problem(...)
_emit_parts_grid(...)
_escape_typst_string(...)
_render_multipart_problem(...)
```

These can exist internally, but they should be private or explicitly experimental.

### Typst exposure

Typst should not be hidden completely. Advanced users need escape hatches.

Expose:

- `RawTypst(...)` for custom Typst snippets.
- `quiz.to_typst()` for debugging and inspection.
- `quiz.write_typst(path)` for writing source without compiling.
- `TypstRenderer` for advanced renderer control.
- `TypstTheme` or similar for theme/page customization.
- Optional preamble/template overrides.

But the normal user should rarely need to write raw Typst.

## Proposed package structure

```text
mathpaper/
  pyproject.toml
  environment.yml
  README.md
  LICENSE
  CHANGELOG.md
  AGENT.md
  docs/
  examples/
  tests/

  src/
    mathpaper/
      __init__.py
      cli.py

      document/
        __init__.py
        test.py
        section.py
        problem.py
        parts.py
        solution.py
        layout.py

      content/
        __init__.py
        base.py
        text.py
        math.py
        raw.py

      math/
        __init__.py
        expressions.py
        polynomials.py
        systems.py
        geometry.py
        randomization.py

      figures/
        __init__.py
        base.py
        coordinate_plane.py
        number_line.py
        geometry.py
        stat_plots.py
        svg.py
        matplotlib.py
        manim.py

      render/
        __init__.py
        typst.py
        compiler.py
        escaping.py
        assets.py
        context.py

      templates/
        typst/
          lib.typ
          page.typ
          problems.typ
          parts.typ
          figures.typ
          solutions.typ
          themes/
            default.typ
            compact.typ
            exam.typ

      resources/
        images/

      utils/
        __init__.py
        paths.py
        hashing.py
        cache.py

  examples/
    hello_typst/
      notebook.ipynb
      build.py
    algebra_1/
      linear_equations.py
    algebra_2/
      polynomial_quiz.py
    geometry/
      triangle_worksheet.py

  tests/
    test_problem_model.py
    test_typst_rendering.py
    test_figures.py
    test_builds.py
```

## Implementation roadmap

### Phase 1: Minimal renderer

Implement enough to create a simple PDF from Python objects.

Required objects:

- `Test`
- `Problem`
- `MultipartProblem`
- `Part`
- `Text`
- `Math`
- `RawTypst`
- `AnswerSpace`
- `PartsGrid`
- `Figure`
- `TypstRenderer`

Minimum methods:

```python
quiz.add(block)
quiz.to_typst(mode="student")
quiz.to_typst(mode="solution")
quiz.write_typst(out_dir, mode="student")
quiz.build(out_dir)
```

Minimum output:

- `main.typ`
- `main.pdf`
- `answer_key.typ`
- `answer_key.pdf`
- `assets/` directory

### Phase 2: Typst template library

Create bundled Typst templates/macros.

Needed Typst files:

- `lib.typ`: imports and exports all template helpers.
- `page.typ`: page setup, headers, footers, title block.
- `problems.typ`: problem numbering and problem containers.
- `parts.typ`: part labels, part grids, answer spaces.
- `figures.typ`: image placement helpers, side figures.
- `solutions.typ`: solution/answer-key formatting.
- `themes/default.typ`: default visual style.
- `themes/compact.typ`: denser worksheet style.
- `themes/exam.typ`: test/exam style.

Generated `main.typ` should import bundled template helpers and then use high-level Typst functions, not raw low-level grid/page code everywhere.

Example target Typst:

```typst
#import "mathpaper.typ": *

#show: test-template.with(
  title: "Polynomial Quiz",
  course: "Algebra 2",
  version: "A",
)

#problem(points: 4)[
  Factor completely.

  $x^2 - 7x + 12$

  #answer-space(1.2in)
]

#multipart-problem(points: 8)[
  Use the graph to answer the questions.

  #side-figure(
    figure: image("assets/poly_001.svg", width: 42%),
    body: [
      #parts-grid(columns: 2, answer-space: 0.9in, (
        [Find the zeros.],
        [Find the y-intercept.],
        [State the end behavior.],
        [Where is $f(x) > 0$?],
      ))
    ],
  )
]
```

### Phase 3: Figure generation

Add figure abstractions that normalize different graphics backends into assets.

Initial figure types:

- `Figure(path, width="...")`
- `CoordinatePlane`
- `NumberLine`

Initial backend:

- Matplotlib -> SVG

Later backends:

- custom SVG generation
- Plotly/Kaleido
- Manim still frames
- optional Desmos-style renderer, if truly needed

Default output should prefer vector graphics, especially SVG or PDF. Avoid screenshots as the default.

### Phase 4: Randomized variants and answer keys

Add deterministic seeding.

Useful concepts:

- `seed`
- `variant`
- `ProblemSpec`
- `GeneratedProblem`
- `manifest.json`

A generated output folder should record enough information to reproduce the document.

Example `manifest.json`:

```json
{
  "title": "Polynomial Quiz",
  "version": "A",
  "seed": 12345,
  "created_by": "mathpaper 0.1.0",
  "problems": [
    {
      "id": "poly_roots_001",
      "seed": 101,
      "points": 8,
      "assets": ["assets/graph_001.svg"]
    }
  ]
}
```

### Phase 5: Examples and tests

Examples should double as product demos and integration tests.

Create examples for:

- Algebra 1: linear equations worksheet.
- Algebra 2: polynomial graph quiz.
- Geometry: triangle/circle worksheet.
- Precalculus: trig graphing worksheet.
- Statistics: normal distribution or scatterplot problem set.

Testing strategy:

1. Unit tests for the object model.
2. Snapshot tests for generated Typst.
3. Compile tests that call `typst compile`, marked separately because they require Typst installed.

## Important layout requirements

The package should eventually support:

- Automatic problem numbering.
- Part labels `a`, `b`, `c`, etc.
- Multi-column parts.
- Side-by-side layouts.
- Figures placed left, right, top, bottom, or full-width.
- Explicit answer spaces.
- Point values.
- Page breaks.
- Keep-together problem blocks.
- Compact and spacious variants.
- Student-only and solution-only content.

True floating/wrapped figures should not be a core requirement at first. Prefer explicit side-by-side layouts because they are more robust for tests and worksheets.

## Content model guidance

Do not represent every piece of content as a bare string.

Use content objects such as:

```python
Text("Explain your reasoning.")
Math(r"x^2 - 7x + 12")
RawTypst("#v(1in)")
Figure("assets/graph.svg")
StudentOnly(...)
SolutionOnly(...)
```

This makes rendering safer and keeps the door open for future non-Typst backends.

## Typst rendering guidance

Generated Typst should be:

- readable,
- debuggable,
- reasonably high-level,
- backed by template macros,
- stable enough for users to inspect.

The renderer should escape user text properly. Raw Typst should only be inserted when explicitly wrapped in `RawTypst`.

The output directory should contain all assets needed by Typst. Avoid referencing files outside the Typst project root unless the user explicitly configures this.

## Development environment

All Python work must be done inside the `mathpaper-dev` conda environment:

```bash
conda activate mathpaper-dev
python3 ...
```

The package is installed in editable mode there (`pip install -e .`), so imports like `from mathpaper import ...` resolve correctly. Running Python outside this environment will fail with import errors.

## Dependencies

Core package dependencies should stay modest.

Likely core dependencies:

- `sympy`
- `numpy`
- `matplotlib`
- `jinja2`
- `pydantic` or dataclasses only
- `platformdirs`

Dev dependencies:

- `pytest`
- `ruff`
- `mypy`
- `build`
- `twine`
- `pre-commit`

Optional dependencies:

- `plotly`
- `kaleido`
- `manim`

Typst itself is assumed to be installed separately and available on `PATH` as `typst`.

## CLI ideas

A CLI is useful, but it should not be overbuilt early.

Possible commands:

```bash
mathpaper build path/to/script.py
mathpaper new algebra-quiz
mathpaper clean out/
mathpaper check-typst
```

Initial implementation can be much simpler. The Python API matters more than the CLI.

## Development principles

1. Build the object model first.
2. Keep Typst generation direct and inspectable.
3. Use Typst for layout; use Python for generation.
4. Prefer vector graphics.
5. Avoid screenshot workflows as defaults.
6. Make answer keys first-class.
7. Make deterministic randomization easy.
8. Do not add Quarto to the core pipeline.
9. Keep raw Typst available as an advanced escape hatch.
10. Keep early scope small but design for expansion.

## First serious milestone

Build one Algebra 2 quiz from Python with:

- title/header/name line,
- numbered problems,
- one ordinary free-response problem,
- one multipart problem with parts `a` through `d`,
- two-column part layout,
- one generated coordinate graph as SVG,
- side-figure layout,
- answer spaces,
- student PDF,
- answer-key PDF.

This milestone should drive the first real API and template decisions.

## Open design questions

- Should `Math(...)` accept LaTeX-like syntax and convert to Typst math, or should users write Typst math directly?
- How much LaTeX compatibility should be supported?
- Should `Part.answer_space` override the parent layout answer space?
- Should answer keys mirror student layout or use a compact solution layout?
- How should custom themes be defined: Python objects, Typst overrides, or both?
- Should figure generation be eager or lazy?
- Should assets be content-addressed by hash to avoid regeneration?
- Should problem generators live in the main package or in optional curriculum modules?

## Current immediate next steps

1. Create the minimal package skeleton under `src/mathpaper/`.
2. Implement a very small `TypstRenderer` that writes `hello.typ` from Python.
3. Add `Test`, `Problem`, and `Text` objects.
4. Add `to_typst()` and `build()` methods.
5. Add a bundled `templates/typst/lib.typ` file, even if it starts nearly empty.
6. Add a notebook or script that builds a one-page PDF.
7. Add PDF preview helper using PyMuPDF for notebooks.
8. Add first multipart problem and parts grid.
9. Add first SVG coordinate graph asset.
10. Add answer-key mode.
