"""mathpaper — Python-first math document generation with Typst."""

__version__ = "0.1.0"

from mathpaper.document.test import Test
from mathpaper.document.templated import TemplatedProblem
from mathpaper.figures.base import Figure
from mathpaper.library import ProblemLibrary, ProblemDef, problem

__all__ = [
    "Test",
    "TemplatedProblem",
    "Figure",
    "ProblemLibrary",
    "ProblemDef",
    "problem",
]
