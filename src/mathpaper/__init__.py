"""mathpaper — Python-first math document generation with Typst."""

__version__ = "0.1.0"

from mathpaper.document.test import Test
from mathpaper.document.problem import Block, Problem, MultipartProblem
from mathpaper.document.parts import FreeResponse, Parts, Part
from mathpaper.document.layout import AnswerSpace, PartsGrid, SideFigure
from mathpaper.document.templated import TemplatedProblem
from mathpaper.content.text import Text
from mathpaper.content.math import Math
from mathpaper.content.raw import RawTypst
from mathpaper.figures.base import Figure
from mathpaper.render.typst import TypstRenderer
from mathpaper.library import ProblemLibrary, ProblemDef, problem

__all__ = [
    "Test",
    "Block",
    "Problem",
    "MultipartProblem",
    "FreeResponse",
    "Parts",
    "Part",
    "AnswerSpace",
    "PartsGrid",
    "SideFigure",
    "TemplatedProblem",
    "Text",
    "Math",
    "RawTypst",
    "Figure",
    "TypstRenderer",
    "ProblemLibrary",
    "ProblemDef",
    "problem",
]
