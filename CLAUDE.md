# AGENT.md

## Project overview

This project is a Python-first math document generation package that renders
to Typst. The goal is to make it easy to create polished math tests, quizzes,
worksheets, handouts, and answer keys by pairing hand-authored Typst layouts
with Python that computes their data (figures, answers, randomized values).

The core idea is:

```text
Hand-authored .typ layout    (durable, edited with Tinymist)
       +
Python @problem function     (computes figure(s) + answer values)
       ↓
Per-problem staged subdir    (problem.typ + context.json + assets)
       ↓
Typst PDF (student + answer key)
```

The package prioritizes reproducibility, reusable problem components,
generated answer keys, and easy integration with Python math/graphics tools
such as SymPy, NumPy, Matplotlib, and Manim.

The long-term aim is a publishable Python package for math educators,
curriculum writers, and technically inclined teachers who want programmatic
control over assessment generation without fighting LaTeX.

## Major design decision

Every problem is a sibling `(.py, .typ)` pair.

- The **`.typ` file** is the durable, hand-edited artifact. It owns layout,
  typography, spacing, columns, and figure placement. Opened in VSCode with
  Tinymist for highlighting, autocomplete, hover, and live preview.
- The **`.py` file** is the Python harness. It computes figures, answers,
  and any other context values, and ships them to the `.typ` via
  `context.json`.

Rationale:

- Typst is the actual page/layout/typesetting engine. Authoring layouts
  directly in `.typ` gives the full editor experience and avoids the
  Python-string-generation tax.
- Python owns generation, asset creation, seeding, problem selection, and
  answer-key construction — the parts that benefit from being code.
- Each staged problem subdir is fully self-contained, so "building a test"
  is just "pick pre-staged problem subdirs and assemble them."

## TemplatedProblem — the only authoring path

### Authoring layout

A templated problem lives as two sibling files. The `.typ` filename matches
the `@problem` id:

```text
examples/templated/problems/
  triangle_rate_001.py     # @problem fn → TemplatedProblem(context=..., figures=...)
  triangle_rate_001.typ    # hand-authored Typst document
  mathpaper.typ            # copy of the helper library for Tinymist preview
```

### The .py file

```python
from mathpaper import TemplatedProblem
from mathpaper.figures.geometry import TriangleDiagram
from mathpaper.library import problem

@problem(id="triangle_rate_001", tags=["calculus"], topic="Related Rates",
         description="Rate of change of triangle area", difficulty="medium",
         course="Calculus")
def triangle_rate_001(seed=None) -> TemplatedProblem:
    fig = TriangleDiagram(a=4, b=5, ...)
    return TemplatedProblem(
        points=10,
        figures=[fig],
        context={"figure": fig.asset_name, "answers": {...}},
    )
```

The decorator resolves the sibling `.typ` at decoration time by looking for
`{id}.typ` next to the `.py`.

### The .typ file

```typst
#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  The area of a triangle … is $A = 1/2 a b sin(theta)$.

  #side-figure(image(ctx.figure, width: 100%), position: right, width: 35%)[
    + Find a formula for $(d A) / (d t)$ …
      #answer-space(1.6in)
      #if-solution[*Answer:* #math-from-str(ctx.answers.formula_a)]
  ]
]
```

The helper library (`src/mathpaper/templates/typst/lib.typ`) provides:
`problem`, `answer-space`, `if-solution`, `set-solution-mode`,
`parts-grid`, `side-figure`, `math-from-str`. For sequential nested parts
use Typst's native `+` enum with `#set enum(numbering: ...)` — it
auto-indents and auto-labels at any depth.

### Building a test

```python
from mathpaper import ProblemLibrary, Test

lib = ProblemLibrary("./problems")

quiz = Test(title="Algebra Quiz", course="Algebra 2", version="A")
quiz.add(lib.get("polynomial_zeros_001").build())
quiz.add(lib.get("triangle_rate_001").build())
quiz.build("out/quiz")
```

`Test.add()` accepts only `TemplatedProblem` instances (or values produced
by `ProblemDef.build()`). Anything else raises `TypeError`.

### Build layout (per-subdir, content-agnostic)

`Test.build()` stages each `TemplatedProblem` into its own subdir, making
the problem fully self-contained:

```text
out/
  main.typ              # student version
  answer_key.typ        # solution version
  main.pdf
  answer_key.pdf
  mathpaper.typ         # helper lib
  problem_001/
    problem.typ         # staged copy of the author's .typ
    context.json        # rendered from TemplatedProblem.context
    mathpaper.typ
    <figure assets>
  problem_002/
    ...
  manifest.json
```

The master `main.typ` `#include`s each subdir's `problem.typ`. This makes
"building a test" mean "picking pre-staged problem subdirs and assembling
them" — each problem dir is fully portable.

### Randomization

Randomization of *values* (zeros, coefficients) is trivial — just vary the
context dict. Randomization of *structure* (number of parts) is not a
first-class feature; for structural variants, write multiple `.typ`
templates and select between them in the `.py` function.

## Public API

The full stable API:

```python
Test(...)
TemplatedProblem(...)
ProblemLibrary(...)
ProblemDef
@problem(...)            # decorator
Figure(...)              # base; pass paths/assets straight to Typst
quiz.add(...)
quiz.build(...)
```

## Figure backend

The primary figure backend is **ManimCE**. Figures render as static PNGs
(last frame of the scene), with white background and automatic whitespace
cropping applied. Rendered files are cached in `.mathpaper_cache/figures/`.

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

The inner class closes over constructor parameters. The cache is
content-addressed: the cache key is sha1(`construct`'s source + its closure
variables). Editing either the construct body OR the constructor arguments
invalidates the cache automatically, so the next build re-renders without
any manual intervention. Scene classes whose source can't be introspected
fall back to a qualname-namespaced cache path (less precise — set
`MATHPAPER_FORCE_RENDER_FIGURES=1` to override in that case).

### Rendering control

```bash
MATHPAPER_NO_RENDER_FIGURES=1 python my_quiz.py        # skip render, use cached PNG
mathpaper build my_quiz.py --no-render-figures          # same via CLI flag

MATHPAPER_FORCE_RENDER_FIGURES=1 python my_quiz.py      # ignore cache, re-render everything
mathpaper build my_quiz.py --force-render-figures       # same via CLI flag
```

When no cached file exists and rendering is skipped, a gray placeholder PNG
is produced automatically.

Matplotlib SVG is also supported via `mathpaper.figures.matplotlib` for
simpler graphs.

## Problem library and @problem decorator

Problems are `@problem`-decorated functions. The decorator attaches metadata
and registers the function in the module's `_PROBLEMS` list. `ProblemLibrary`
scans directories, loads files dynamically, and indexes problems by id.

```python
@problem(
    id="triangle_rate_001",
    tags=["calculus", "related-rates"],
    topic="Related Rates",
    description="Rate of change of triangle area",
    difficulty="medium",
    course="Calculus",
)
def triangle_rate_001(seed=None) -> TemplatedProblem:
    ...
    return TemplatedProblem(context={...}, points=10)
```

The function must return a `TemplatedProblem`; the decorator raises a
`TypeError` if anything else is returned. The sibling `{id}.typ` template
is resolved at decoration time; missing siblings raise `FileNotFoundError`
when `build()` is called.

## Planned repository split

Once the engine API is stable, problem content will live in a separate repo
(`mathpaper-problems`) that depends on `mathpaper` as a package. The
`problems/` directory in this repo is the transitional home for content
under development. The `personal/` directory holds private/experimental
problems.

The split is deferred until the following are stable:
- The `TemplatedProblem` context schema conventions
- The `ManimFigure` cache strategy
- The per-subdir staging layout

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
      app.py             # Streamlit-based "mathpaper explore" UI

      document/
        __init__.py
        test.py          # Test class — stages TemplatedProblems and builds PDFs
        templated.py     # TemplatedProblem dataclass

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
        compiler.py       # typst compile + availability check
        escaping.py       # escape_typst_text helper
        templated.py      # per-subdir staging + master main.typ rendering

      library/
        __init__.py
        decorator.py      # @problem decorator; ProblemDef dataclass
        registry.py       # ProblemLibrary
        usage.py

      templates/
        typst/
          lib.typ         # helper library shipped to every staged subdir

      utils/
        __init__.py
        paths.py
        hashing.py
        cache.py

  examples/
    templated/
      build_quiz.py
      problems/
        polynomial_zeros_001.py / .typ
        triangle_rate_001.py / .typ
        mathpaper.typ   # local copy for Tinymist preview
```

## Development environment

All Python work must be done inside the `mathpaper-dev` conda environment:

```bash
conda activate mathpaper-dev
python3 ...
```

The package is installed in editable mode there (`pip install -e .`), so
imports like `from mathpaper import ...` resolve correctly. Running Python
outside this environment will fail with import errors.

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
- `streamlit` + `pymupdf` (for the `mathpaper explore` browser app)

Typst is assumed to be installed separately and available on `PATH` as
`typst`.

## Development principles

1. Hand-authored `.typ` files own layout; Python owns data and figures.
2. Each problem stages into a self-contained subdir.
3. Use Typst for layout; use Python for generation.
4. Prefer vector graphics; Manim is the primary figure backend.
5. Make answer keys first-class (driven by a single solution-mode flag).
6. Make deterministic randomization easy.
7. Keep early scope small but design for expansion.

## Resolved design decisions

- **Single authoring path.** Every problem is a sibling `(.py, .typ)`
  pair returning a `TemplatedProblem`. The previous Python-recursive
  `Block`/`Problem`/`MultipartProblem`/`Parts`/`Part` model has been
  removed.
- **Per-subdir staging.** Each problem stages into `problem_NNN/` with
  its own `problem.typ`, `context.json`, helper lib, and figure assets.
  This makes problems portable and tests composable.
- **Solution mode is a single Typst state.** `set-solution-mode(true)` in
  the master `answer_key.typ` flips `#if-solution[...]` blocks on across
  every staged problem; `answer-space(...)` collapses to zero in solution
  mode automatically.
- **Manim is the primary figure backend.** PNG output, white background,
  auto-cropped, cached in `.mathpaper_cache/figures/`.
- **Manim figure cache is content-addressed.** Cache key is sha1(construct's
  source + closure values), so edits to the scene body or constructor args
  invalidate the cache automatically. `MATHPAPER_FORCE_RENDER_FIGURES=1`
  is the always-available override.

## Open design questions

- Should answer keys mirror student layout or use a compact solution layout?
- How should custom themes be defined: Python objects, Typst overrides, or
  both?
- Should figure generation be eager or lazy?
- Should problem generators live in the main package or in optional
  curriculum modules? (Planned: separate `mathpaper-problems` repo.)
- What is the standard `seed` parameter convention for randomized problem
  variants?

## Current immediate next steps

1. Port the legacy reference problems in `examples/` and `problems/` to the
   `TemplatedProblem` pattern (they remain in-tree as reference material
   but no longer import successfully against the current API).
2. Add `seed: int | None = None` as a standard `@problem` parameter
   convention for randomized variants.
3. Document the conventions for `context.json` keys (`number`, `points`,
   `figure`, `answers`).
4. Split content into a separate `mathpaper-problems` repository once the
   conventions are stable.
