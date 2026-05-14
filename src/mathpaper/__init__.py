"""mathpaper — Python-first math document generation with Typst."""

__version__ = "0.1.0"

from mathpaper.document.test import Test
from mathpaper.document.problem import Problem, MultipartProblem
from mathpaper.document.parts import Part
from mathpaper.document.layout import AnswerSpace, PartsGrid, SideFigure
from mathpaper.content.text import Text
from mathpaper.content.math import Math
from mathpaper.content.raw import RawTypst
from mathpaper.figures.base import Figure
from mathpaper.render.typst import TypstRenderer

__all__ = [
    "Test",
    "Problem",
    "MultipartProblem",
    "Part",
    "AnswerSpace",
    "PartsGrid",
    "SideFigure",
    "Text",
    "Math",
    "RawTypst",
    "Figure",
    "TypstRenderer",
]
