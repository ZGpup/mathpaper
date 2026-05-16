"""Build the Algebra 1 linear equations worksheet from the problems library.

Usage::

    conda activate mathpaper-dev
    python examples/algebra_1/build.py

Outputs to ``out/algebra_1/``.
"""
from __future__ import annotations

from pathlib import Path

from mathpaper import ProblemLibrary, Test

PROBLEMS_DIR = Path(__file__).parent.parent.parent / "problems" / "algebra"


def main() -> None:
    lib = ProblemLibrary(PROBLEMS_DIR)

    quiz = Test(title="Linear Equations Worksheet", course="Algebra 1")
    quiz.add(lib.get("alg_linear_solve_001").build())
    quiz.add(lib.get("alg_linear_solve_002").build())
    quiz.add(lib.get("alg_linear_analysis_001").build())
    quiz.build("out/algebra_1")
    print("Built to out/algebra_1/")


if __name__ == "__main__":
    main()
