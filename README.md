# mathpaper

A Python-first toolkit for building math tests, quizzes, and worksheets.
Author each problem as a sibling `.py` / `.typ` pair: the `.typ` owns the
layout, Python owns the figures and answers. Pick problems from a tagged
library, assemble them into a quiz, and produce a print-ready PDF and
answer key.

```
Hand-authored .typ  +  Python @problem fn  →  Staged subdirs  →  PDF (student + answer key)
```

---

## 1. Install

You need:

- **Python 3.11+** (managed by conda below)
- **[Typst](https://typst.app/)** on your `PATH` — used to render PDFs

### macOS / Linux setup

```bash
# 1. clone
git clone https://github.com/your-username/mathpaper
cd mathpaper

# 2. create and activate the conda env (defines all deps)
conda env create -f environment.yml
conda activate mathpaper-dev

# 3. install Typst
brew install typst              # macOS
# or: cargo install typst-cli   # any platform with rust
# or download a binary from https://github.com/typst/typst/releases

# 4. (optional) install the test gate so pytest runs before pushes to main
pre-commit install --hook-type pre-push
```

### Verify everything works

```bash
mathpaper check-typst           # should print: typst found: typst x.y.z
pytest -q                       # should print: N passed
```

If any of the steps fail, jump to **Troubleshooting** at the bottom.

---

## 2. Where to put your own tests and quizzes

The package lives in `src/mathpaper/`. The repo also includes:

```
problems/   ← shared problem library (curriculum-aligned, version-controlled)
examples/   ← example quiz scripts that import from problems/
personal/   ← your private quizzes — git-ignored, never committed
out/        ← build outputs — git-ignored
```

`personal/` is the recommended place for quizzes you're writing for your
own classes. Create one folder per class or unit:

```
personal/
  algebra2_unit3/
    quiz_polynomials.py
    test_chapter_review.py
```

Inside any of those files, write a script that builds a `Test`. Run it:

```bash
mathpaper build personal/algebra2_unit3/quiz_polynomials.py
# or, equivalently
python personal/algebra2_unit3/quiz_polynomials.py
```

Output PDFs land in whatever directory the script passes to `quiz.build(...)`
(by convention, `out/<name>/`).

---

## 3. Using the problem library

`problems/` holds reusable, tagged problem generators. Each one is a Python
function decorated with `@problem(...)` that returns a `TemplatedProblem`,
paired with a sibling `.typ` file of the same name. The library indexes
the Python functions by id, tag, topic, difficulty, and course.

You have three ways to use the library.

### 3a. Browser test builder *(easiest)*

```bash
pip install ".[explore]"        # one-time: install streamlit + pymupdf
mathpaper explore ./problems    # opens a local browser UI
```

In the browser you can:

- Filter problems by topic / course / difficulty / keywords
- Preview any problem as a rendered PDF
- Click **+ Add to test** to assemble a quiz
- Set the title, course, version
- Click **Build PDF** to generate `main.pdf` (student) and `answer_key.pdf`
- Click **Export .py** to download an equivalent Python script you can edit

> Errors: if "preview failed" appears, run `mathpaper check-typst` first.

### 3b. Command line

```bash
mathpaper index ./problems                      # build problems/catalog.json
mathpaper search ./problems --tag derivatives
mathpaper search ./problems --topic "Implicit Differentiation" --difficulty hard
mathpaper search ./problems --course Calculus --keywords "critical points"
```

### 3c. From a Python script

```python
from mathpaper import Test
from mathpaper.library import ProblemLibrary

lib = ProblemLibrary("./problems")

quiz = Test(title="Derivatives Quiz", course="Calculus", version="A")

# Pull by id
quiz.add(lib.get("calc_deriv_poly_001").build())

# Or pull all problems with a tag
for p in lib.search(tags=["implicit-differentiation"]):
    quiz.add(p.build())

quiz.build("out/derivatives_quiz")
# Produces:
#   out/derivatives_quiz/main.typ
#   out/derivatives_quiz/main.pdf          ← student version
#   out/derivatives_quiz/answer_key.typ
#   out/derivatives_quiz/answer_key.pdf    ← answer key (computed)
#   out/derivatives_quiz/mathpaper.typ
#   out/derivatives_quiz/problem_001/...   ← one subdir per problem
#   out/derivatives_quiz/manifest.json
```

Override a problem's defaults to get a different version of the same template:

```python
from sympy import symbols
x = symbols("x")

quiz.add(lib.get("calc_deriv_poly_001").build(expr=x**3 - 3*x))
```

---

## 4. Writing a new problem

A problem is a sibling `(.py, .typ)` pair under `problems/`:

```
problems/calculus/
  my_problem.py
  my_problem.typ
```

### The .py file

```python
# problems/calculus/calc_deriv_poly_002.py
from sympy import symbols
from mathpaper import TemplatedProblem
from mathpaper.library import problem
from mathpaper.math import sympy_to_typst
from mathpaper.math.calculus import derivative

x = symbols("x")

@problem(
    id="calc_deriv_poly_002",
    tags=["calculus", "derivatives", "polynomial"],
    topic="Derivatives",
    description="Find f'(x) for a cubic polynomial",
    difficulty="easy",
    course="Calculus",
)
def calc_deriv_poly_002(expr=None) -> TemplatedProblem:
    e = expr if expr is not None else x**3 - 6*x + 4
    return TemplatedProblem(
        points=4,
        context={
            "expr": sympy_to_typst(e),
            "answers": {
                "derivative": f"f'(x) = {sympy_to_typst(derivative(e))}",
            },
        },
    )
```

### The .typ file

```typst
// problems/calculus/calc_deriv_poly_002.typ
#import "mathpaper.typ": *
#let ctx = json("context.json")

#problem(number: ctx.number, points: ctx.points)[
  Let $f(x) = #math-from-str(ctx.expr)$. Find $f'(x)$.
  #answer-space(1.2in)
  #if-solution[*Answer:* #math-from-str(ctx.answers.derivative)]
]
```

The answer is computed from the expression — change `expr` and both the
student worksheet and the answer key update automatically.

### Rules for writing a problem

A `@problem` function must:

1. Be defined in a `.py` file somewhere under `problems/`.
2. Be decorated with `@problem(id=..., tags=[...], topic=..., description=..., difficulty=..., course=...)`.
3. Take only keyword arguments (with defaults) so it can be called with no args.
4. Return a `TemplatedProblem(...)`.
5. Have a globally unique `id` (use a stable prefix like `<course>_<topic>_<n>`).
6. Have a sibling `{id}.typ` file in the same directory.

The companion `.typ` file should:

1. Start with `#import "mathpaper.typ": *` and `#let ctx = json("context.json")`.
2. Wrap its body in `#problem(number: ctx.number, points: ctx.points)[...]`.
3. Use `#answer-space(<height>)` for blank response areas — it collapses in
   solution mode.
4. Use `#if-solution[...]` to show answers in the answer key only.
5. Use `#math-from-str(ctx...)` to evaluate context-supplied Typst-math
   strings as live math.

The helper library (`src/mathpaper/templates/typst/lib.typ`) provides:
`problem`, `answer-space`, `if-solution`, `set-solution-mode`,
`parts-grid`, `side-figure`, `math-from-str`. For sequential nested parts
use Typst's native `+` enum with `#set enum(numbering: "a.")` — it
auto-indents and auto-labels at any depth.

Parametrize problems via keyword args so the same template can produce
different versions:

```python
@problem(id="alg_factor_001", ...)
def alg_factor_001(leading_coeff=2, roots=None) -> TemplatedProblem:
    roots = roots if roots is not None else [3, -2]
    ...
```

Then call `lib.get("alg_factor_001").build(leading_coeff=3, roots=[1, -4])`.

See [examples/templated/problems/](examples/templated/problems/) for full
working examples.

---

## CLI cheat sheet

```bash
mathpaper check-typst                          # verify typst is on PATH
mathpaper index ./problems                     # rebuild problems/catalog.json
mathpaper search ./problems --tag derivatives  # search the library
mathpaper explore ./problems                   # open browser test builder
mathpaper build path/to/quiz.py                # run a build script
mathpaper build path/to/quiz.py --no-render-figures   # reuse cached figures
mathpaper history --course Calculus            # show problems you've used
```

---

## Figures

The primary figure backend is **Manim**. Figures render to PNG (last frame
of the scene), are auto-cropped, and cached under `.mathpaper_cache/figures/`
keyed by the scene class qualname.

```python
from mathpaper.figures.manim import ManimFigure
from manim import Scene, Circle, BLUE

class CircleFigure(ManimFigure):
    def __init__(self, width="60%"):
        class _Scene(Scene):
            def construct(self):
                self.add(Circle(color=BLUE))
        super().__init__(_Scene, "circle.png", width)
```

In a `TemplatedProblem`, pass figures via the `figures=[...]` argument and
reference them by `asset_name` in the context dict:

```python
return TemplatedProblem(
    figures=[fig],
    context={"figure": fig.asset_name, ...},
)
```

Inside the `.typ` file: `#image(ctx.figure, width: 100%)`.

Skip re-rendering when iterating on a quiz:

```bash
mathpaper build my_quiz.py --no-render-figures
# or:  MATHPAPER_NO_RENDER_FIGURES=1 python my_quiz.py
```

`MatplotlibFigure` (SVG output) is also available for simpler plots.

---

## Development

```bash
conda activate mathpaper-dev
pytest -q                                  # run the test suite
ruff check src/                            # lint
pre-commit install --hook-type pre-push    # install the pre-push test gate
```

The hook runs `pytest` automatically — but only when a `git push` would
update remote `main`. Pushes to feature branches skip it, so you can push
work-in-progress freely. Local commits and merges are never blocked; the
gate runs at push time, which catches fast-forward merges, merge commits,
squash merges, and rebases uniformly.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `mathpaper: command not found` | conda env not active | `conda activate mathpaper-dev` |
| `ModuleNotFoundError: mathpaper` | running outside the conda env, or editable install missing | `conda activate mathpaper-dev`, then `pip install -e .` |
| `typst not found on PATH` | Typst not installed | `brew install typst` (or download a release binary) |
| Browser app: `streamlit not found` | optional deps not installed | `pip install ".[explore]"` |
| Browser app: "preview failed" | typst missing | `mathpaper check-typst` |
| Manim figure errors on first run | `manim` not installed | `pip install ".[manim]"` |
| Build is slow on each run | re-rendering figures every time | add `--no-render-figures` once cached |
| `ChunkType … appeared before IHDR` from Typst | corrupt PNG in a `problem_NNN/` subdir | delete `.mathpaper_cache/figures/` and rebuild |
| Tests didn't run before push to main | pre-push hook not installed | `pre-commit install --hook-type pre-push` (one-time) |

---

## License

GNU General Public License v3.0 (GPL-3.0)
