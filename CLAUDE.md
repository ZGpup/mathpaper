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
from mathpaper import Test, MultipartProblem, Part, Parts, PartsGrid, SideFigure
from mathpaper.content import Math, Text
from mathpaper.figures.manim import ManimFigure
from mathpaper.math import polynomial_from_roots, sympy_to_typst

poly = polynomial_from_roots([-3, 1, 4])

class PolyGraph(ManimFigure):
    def __init__(self):
        from manim import Scene, Axes, BLUE
        class _Scene(Scene):
            def construct(self):
                ax = Axes(x_range=[-6, 6], y_range=[-10, 10])
                self.add(ax, ax.plot(lambda x: (x+3)*(x-1)*(x-4), color=BLUE))
        super().__init__(_Scene, "poly_graph.png", width="100%")

quiz = Test(
    title="Polynomial Quiz",
    course="Algebra 2",
    version="A",
)

quiz.add(
    MultipartProblem(
        prompt=Text("Use the graph of $f$ to answer the questions."),
        figure=PolyGraph(),
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
    poly_graph.png
  manifest.json
```

## Major design decision

This package uses **Python -> Typst directly**.

Rationale:

- Typst is the actual page/layout/typesetting engine.
- Direct Typst generation gives better control over tests, worksheets, columns, figures, answer spaces, and page layout.
- Python should own generation, asset creation, seeding, problem selection, and answer-key construction.
- Typst should own page layout, typography, grids, spacing, headers, footers, and PDF rendering.

## Document tree — the recursive Block model

Every item added to `Test.add()` is a `Block`. `Problem` and `MultipartProblem` are plain constructor functions that return `Block`; they are not separate classes. The renderer only needs to handle one type at the top level.

```
Test._blocks: list[Block]

Block
  stem: Any                    # the top-level prompt (Text, Math, etc.)
  body: FreeResponse | Parts   # leaf or recursive container
  answer: Any | None           # top-level answer for solution mode
  figure: Any | None           # optional figure (orthogonal to body)
  figure_layout: Any | None    # SideFigure, etc.
  points: int | None
  keep_together: bool

FreeResponse
  height: str                  # e.g. "1in"

Parts
  parts: list[Part]
  layout: Any                  # PartsGrid or None
  labels: str                  # "alpha" | "roman" | "numeric"
  indent: bool                 # wrap in #pad(left: 1.5em) when nested; default True

Part
  prompt: Any
  body: FreeResponse | Parts   # FreeResponse built in __post_init__ if None
  answer: Any | None           # shown in solution mode
  answer_space: str | None     # backwards-compat shorthand → FreeResponse(height)
```

### Why `Problem` and `MultipartProblem` are functions, not classes

`Problem(...)` returns `Block(stem=prompt, body=FreeResponse(answer_space), ...)`.
`MultipartProblem(...)` returns `Block(stem=prompt, body=Parts(parts=..., layout=...), ...)`.

All existing call sites are unchanged. The renderer does a single `isinstance(block, Block)` check and then walks `block.body` recursively. Adding a new answer region type (e.g. `MultipleChoice`, `TableResponse`) does not require changes to the problem-level rendering logic.

### Label schemes

The `Parts.labels` field controls the label prefix assigned to each child `Part`. The label is injected by the parent `Parts` container at render time — the `Part` itself is label-agnostic.

| `labels=`   | Output         |
|-------------|----------------|
| `"alpha"`   | a, b, c, …     |
| `"roman"`   | i, ii, iii, …  |
| `"numeric"` | 1, 2, 3, …     |

### Indentation

When `Part.body` is a `Parts` node and `parts.indent` is `True` (the default), the renderer wraps the sub-block in `#pad(left: 1.5em)[...]`. Each nesting level stacks another 1.5em. Set `indent=False` to suppress.

### Grid layout at any nesting level

`PartsGrid(columns=N)` on a `Parts` node renders its parts in an N-column Typst grid. This works at any depth:

```python
Part(
    prompt=Text("Find the key features."),
    body=Parts(
        labels="roman",
        layout=PartsGrid(columns=2, answer_space="0.9in"),
        parts=[...],   # i, ii in row 1; iii, iv in row 2
    ),
)
```

Produces:

```
a.  Find the key features.

    ┌──────────────────┬──────────────────┐
    │ i.  …            │ ii.  …           │
    │iii.  …           │ iv.  …           │
    └──────────────────┴──────────────────┘
```

## Public API philosophy

The stable public API should be the **Python object model**, not raw Typst strings.

Stable public API:

```python
Test(...)
Block(...)
Problem(...)          # constructor function → Block
MultipartProblem(...) # constructor function → Block
FreeResponse(...)
Parts(...)
Part(...)
PartsGrid(...)
SideFigure(...)
AnswerSpace(...)
Figure(...)
Math(...)
Text(...)
RawTypst(...)
TypstRenderer(...)
quiz.to_typst()
quiz.write_typst(...)
quiz.build(...)
```

Keep private or explicitly experimental:

```python
_render_block(...)
_render_parts_node(...)
_render_part(...)
_generate_labels(...)
_escape_typst_string(...)
```

### Typst exposure

Typst should not be hidden completely. Advanced users need escape hatches.

Expose:

- `RawTypst(...)` for custom Typst snippets.
- `quiz.to_typst()` for debugging and inspection.
- `quiz.write_typst(path)` for writing source without compiling.
- `TypstRenderer` for advanced renderer control.
- Optional preamble/template overrides.

But the normal user should rarely need to write raw Typst.

## Figure backend

The primary figure backend is **ManimCE**. Figures render as static PNGs (last frame of the scene), with white background and automatic whitespace cropping applied. Rendered files are cached in `.mathpaper_cache/figures/`.

### ManimFigure pattern

```python
from mathpaper.figures.manim import ManimFigure
from manim import Scene

class MyFigure(ManimFigure):
    def __init__(self, param, width="80%"):
        class _Scene(Scene):
            def construct(self):
                ...  # param accessible via closure
        super().__init__(_Scene, "my_figure.png", width)
```

The inner class closes over constructor parameters. The cache key is the filename — two scenes with the same filename will collide. Content-addressed caching (hash-based) is a planned improvement.

### Rendering control

```bash
MATHPAPER_NO_RENDER_FIGURES=1 python my_quiz.py   # skip render, use cached PNG
mathpaper build my_quiz.py --no-render-figures     # same via CLI flag
```

When no cached file exists and rendering is skipped, a gray placeholder PNG is produced automatically.

Matplotlib SVG is also supported via `mathpaper.figures.matplotlib` for simpler graphs.

## Problem library and @problem decorator

Problems are `@problem`-decorated functions. The decorator attaches metadata and registers the function in the module's `_PROBLEMS` list. `ProblemLibrary` scans directories, loads files dynamically, and indexes problems by id.

```python
@problem(
    id="calc_deriv_poly_001",
    tags=["calculus", "derivatives"],
    topic="Derivatives",
    description="Find f'(x) for a degree-4 polynomial",
    difficulty="easy",    # "easy" | "medium" | "hard"
    course="Calculus",
)
def calc_deriv_poly_001(expr=None) -> Problem | MultipartProblem:
    ...
    return Problem(...)
```

The function should return a `Problem` or `MultipartProblem` (both produce `Block`). Default parameters serve as the canonical example; callers can override them via `.build(expr=...)`.

## Planned repository split

Once the engine API is stable, problem content will live in a separate repo (`mathpaper-problems`) that depends on `mathpaper` as a package. The `problems/` directory in this repo is the transitional home for content under development. The `personal/` directory holds private/experimental problems.

The split is deferred until the following are stable:
- The `@problem` return type contract
- The `Block`/`Parts`/`Part`/`FreeResponse` recursive structure
- The `ManimFigure` cache strategy

## Package structure

```text
mathpaper/
  pyproject.toml
  environment.yml
  README.md
  LICENSE
  CHANGELOG.md
  CLAUDE.md
  docs/
  examples/
  tests/

  src/
    mathpaper/
      __init__.py
      cli.py
      app.py

      document/
        __init__.py
        test.py
        problem.py       # Block dataclass; Problem() and MultipartProblem() constructors
        parts.py         # FreeResponse, Parts, Part
        section.py
        solution.py
        layout.py        # PartsGrid, SideFigure, AnswerSpace

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
        calculus.py
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
        manim.py          # ManimFigure base class; primary backend

      render/
        __init__.py
        typst.py          # TypstRenderer; recursive _render_parts_node/_render_part
        compiler.py
        escaping.py
        assets.py
        context.py

      library/
        __init__.py
        decorator.py      # @problem decorator; ProblemDef dataclass
        registry.py       # ProblemLibrary
        usage.py

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

      utils/
        __init__.py
        paths.py
        hashing.py
        cache.py

  examples/
    algebra_2/
      polynomial_quiz.py  # includes nested sub-parts demo (Parts(labels="roman", columns=2))
  problems/
    calculus/
      derivatives.py
  personal/
    test3/
      scratch.py
```

## Development environment

All Python work must be done inside the `mathpaper-dev` conda environment:

```bash
conda activate mathpaper-dev
python3 ...
```

The package is installed in editable mode there (`pip install -e .`), so imports like `from mathpaper import ...` resolve correctly. Running Python outside this environment will fail with import errors.

## Dependencies

Core:

- `sympy`
- `numpy`
- `matplotlib`
- `jinja2`
- `platformdirs`

Dev:

- `pytest`
- `ruff`
- `mypy`
- `build`
- `twine`
- `pre-commit`

Optional:

- `manim` (primary figure backend)
- `plotly` + `kaleido`

Typst is assumed to be installed separately and available on `PATH` as `typst`.

## Development principles

1. Build the object model first.
2. Keep Typst generation direct and inspectable.
3. Use Typst for layout; use Python for generation.
4. Prefer vector graphics; Manim is the primary figure backend.
5. Make answer keys first-class.
6. Make deterministic randomization easy.
7. Do not add Quarto to the core pipeline.
8. Keep raw Typst available as an advanced escape hatch.
9. Keep early scope small but design for expansion.
10. The document tree is recursive — `Part.body` can be `FreeResponse` or `Parts`.

## Resolved design decisions

- **`Problem` and `MultipartProblem` are constructor functions, not classes.** Both return `Block`. The renderer handles one type.
- **The document tree is recursive.** `Part.body` is either `FreeResponse` (leaf) or `Parts` (nested). Label scheme (`alpha`, `roman`, `numeric`) lives on the `Parts` container, not on individual `Part` objects.
- **Indentation at each nesting level.** `Parts.indent=True` (default) wraps the sub-block in `#pad(left: 1.5em)` in Typst. Stacks automatically with depth.
- **Grid layout works at any nesting depth.** `PartsGrid(columns=N)` on an inner `Parts` node produces a multi-column grid inside an indented block.
- **Manim is the primary figure backend.** PNG output, white background, auto-cropped, cached in `.mathpaper_cache/figures/`.
- **`Part.answer_space` is a backwards-compatible shorthand.** It initializes `Part.body = FreeResponse(answer_space)` in `__post_init__`. Existing problem code is unaffected.

## Open design questions

- Should `Math(...)` accept LaTeX-like syntax and convert to Typst math, or should users write Typst math directly? (Currently: Typst math directly.)
- Should answer keys mirror student layout or use a compact solution layout?
- How should custom themes be defined: Python objects, Typst overrides, or both?
- Should figure generation be eager or lazy?
- Should assets be content-addressed by hash to avoid regeneration? (Currently: filename-based; collision risk.)
- Should problem generators live in the main package or in optional curriculum modules? (Planned: separate `mathpaper-problems` repo.)
- What is the standard `seed` parameter convention for randomized problem variants?
- Should `MultipleChoice`, `TableResponse`, and other answer region types be added? (Planned, not yet implemented.)

## Current immediate next steps

1. Lock down the `@problem` return type (annotate `-> Block`, validate in decorator).
2. Add `seed: int | None = None` as a standard `@problem` parameter convention.
3. Content-address the Manim figure cache (hash-based filename, not user-supplied).
4. Add `MultipleChoiceProblem` / `MultipleChoice` answer region type.
5. Add `TableResponse` answer region type (fill in a table of values).
6. Split content into a separate `mathpaper-problems` repository once the above are stable.
