"""Build the demo quiz from two TemplatedProblems.

Discovers problems via ProblemLibrary (the same path a real curriculum would
take) and assembles them into a Test.

Usage::

    conda activate mathpaper-dev
    python examples/templated/build_quiz.py

Outputs to ``examples/templated/_out/`` :
  - main.pdf, main.typ            (student version)
  - answer_key.pdf, answer_key.typ
  - problem_001/, problem_002/    (staged per-subdir problem contents)
  - manifest.json
"""
from __future__ import annotations

from pathlib import Path

from mathpaper import ProblemLibrary, Test

HERE = Path(__file__).parent
OUT = HERE / "_out"


def main() -> None:
    lib = ProblemLibrary(HERE / "problems")

    quiz = Test(title="Templated Problem Demo", course="Algebra 2 / Calculus", version="A")
    quiz.add(lib.get("polynomial_zeros_001").build())
    quiz.add(lib.get("triangle_rate_001").build())
    quiz.build(OUT)
    print(f"built {OUT / 'main.pdf'}")


if __name__ == "__main__":
    main()
