"""Build the calculus derivatives and implicit differentiation quiz from the library.

Usage::

    conda activate mathpaper-dev
    python examples/calculus/derivatives_quiz.py

Outputs to ``out/calculus/``.
"""
from __future__ import annotations

from pathlib import Path

from mathpaper import ProblemLibrary, Test

PROBLEMS_DIR = Path(__file__).parent.parent.parent / "problems" / "calculus"

lib = ProblemLibrary(PROBLEMS_DIR)

quiz = Test(title="Derivatives Quiz", course="Calculus", version="A")
quiz.add(lib.get("calc_deriv_poly_001").build())
quiz.add(lib.get("calc_deriv_poly_multipart_001").build())
quiz.add(lib.get("calc_implicit_circle_001").build())
quiz.add(lib.get("calc_implicit_mixed_001").build())

quiz.build("out/calculus")
print("Built to out/calculus/")
