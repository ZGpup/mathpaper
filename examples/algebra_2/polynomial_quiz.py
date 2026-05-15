"""Algebra 2 polynomial analysis quiz."""
from pathlib import Path

from mathpaper import Test
from mathpaper.library import ProblemLibrary

PROBLEMS_DIR = Path(__file__).parent.parent.parent / "problems" / "algebra"

lib = ProblemLibrary(PROBLEMS_DIR)

quiz = Test(title="Polynomial Functions Quiz", course="Algebra 2", version="A")

quiz.add(lib.get("alg_factor_quadratic_001").build(leading_coeff=2, roots=[1, -3]))
quiz.add(lib.get("alg_quadratic_analysis_001").build(roots=[-4, 1]))
quiz.add(lib.get("alg_cubic_analysis_001").build(roots=[-1, 2, 4]))
quiz.add(lib.get("alg_vertex_form_001").build(a=-2, h=3, k=8))

quiz.build("out/algebra_2")
print("Built to out/algebra_2/")
