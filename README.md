# mathpaper

A math problem library and test builder for educators. Search a growing bank of tagged, curriculum-aligned problems, preview them rendered, and assemble a print-ready PDF quiz — without writing code. When you need a new problem type, write one Python function and it joins the library permanently.

---

## Setup

**Requirements:** [Typst](https://typst.app/) installed and on your PATH.

```bash
git clone https://github.com/your-username/mathpaper
cd mathpaper
conda env create -f environment.yml   # creates the mathpaper-dev environment
conda activate mathpaper-dev
```

For the browser test builder, also install the explore extras:

```bash
pip install ".[explore]"
```

Verify everything is working:

```bash
mathpaper check-typst
mathpaper index ./problems
```

---

## Browser test builder

The fastest way to build a quiz. No code required.

```bash
conda activate mathpaper-dev
mathpaper explore ./problems
```

This opens a local browser UI where you can:

- Search problems by topic, tag, course, difficulty, or keyword
- Preview any problem as a rendered PDF
- Select problems and arrange them into a test
- Set the title, course, and version
- Click **Build PDF** to produce student and answer-key PDFs in one step
- Click **Export .py** to get a Python script you can customize further

> Requires the `explore` extras (`pip install ".[explore]"`)

---

## Problem library

Problems are stored as tagged Python functions in the `problems/` directory. The library loads them at startup — no database to maintain, no migration scripts, just Python files you can version-control and share.

### Search from the command line

```bash
mathpaper search --tag derivatives
mathpaper search --topic "Implicit Differentiation" --difficulty hard
mathpaper search --course Calculus --keywords "critical points"
```

### Use from a script

```python
from mathpaper import Test
from mathpaper.library import ProblemLibrary

lib = ProblemLibrary("./problems")

quiz = Test(title="Derivatives Quiz", course="Calculus", version="A")
for p in lib.search(tags=["derivatives"]):
    quiz.add(p.build())

quiz.build("out/quiz")
# out/quiz/main.pdf        ← student version
# out/quiz/answer_key.pdf  ← answer key (computed, not hand-written)
```

Swap a problem's values without editing the library:

```python
from sympy import symbols
x = symbols("x")

lib.get("calc_deriv_poly_001").build(expr=x**3 - 3*x)
```

Track what you've used in past quizzes:

```bash
mathpaper history --course Calculus
```

---

## Writing a new problem

Add a `@problem`-decorated function to any `.py` file under `problems/`. Run `mathpaper index ./problems` afterward and it appears in search immediately.

```python
# problems/calculus/derivatives.py
from mathpaper import Problem, Text, Math
from mathpaper.library import problem
from mathpaper.math.calculus import derivative
from mathpaper.math import sympy_to_typst
from sympy import symbols

x = symbols("x")

@problem(
    id="calc_deriv_poly_001",
    tags=["calculus", "derivatives", "polynomial"],
    topic="Derivatives",
    description="Find f'(x) for a degree-4 polynomial",
    difficulty="easy",
    course="Calculus",
)
def calc_deriv_poly_001(expr=None):
    e = expr or x**4 - 8*x**2 + 7
    return Problem(
        prompt=Text(f"Let $f(x) = {sympy_to_typst(e)}$. Find $f'(x)$."),
        answer=Math(f"f'(x) = {sympy_to_typst(derivative(e))}"),
        answer_space="1.2in",
        points=4,
    )
```

The answer is computed from the expression — change `expr` and both the student worksheet and the answer key update automatically.

---

## Public API

```python
# Documents
Test(title, course="", version="")
Problem(prompt, answer=None, answer_space=None, points=None)
MultipartProblem(prompt, parts, figure=None, figure_layout=None, layout=None, points=None)
Part(prompt, answer=None, answer_space=None)

# Layout
PartsGrid(columns=1, answer_space="1in")
SideFigure(position="right", width="42%")
AnswerSpace(height="1in")

# Content
Text("plain text")
Math(r"x^2 - 4")          # Typst math syntax
RawTypst("#v(0.5in)")      # raw Typst escape hatch
Figure("path/to/file.svg")

# Problem library
ProblemLibrary("./problems")
@problem(id, tags, topic, description, difficulty, course)
lib.search(tags, topic, course, difficulty, keywords)
lib.get("problem_id").build(**kwargs)
lib.build_catalog("catalog.json")

# Renderer (advanced)
quiz.to_typst(mode="student")
quiz.write_typst(out_dir, mode)
quiz.build(out_dir)
```

---

## Examples

| Example | File |
|---|---|
| Calculus derivatives quiz | [examples/calculus/derivatives_quiz.py](examples/calculus/derivatives_quiz.py) |
| Algebra 2 polynomial quiz | [examples/algebra_2/polynomial_quiz.py](examples/algebra_2/polynomial_quiz.py) |
| Calculus problem library | [problems/calculus/derivatives.py](problems/calculus/derivatives.py) |

```bash
python examples/calculus/derivatives_quiz.py
```

---

## Development

```bash
conda activate mathpaper-dev
pytest
ruff check src/
```

## License

GNU General Public License v3.0 (GPL-3.0)
