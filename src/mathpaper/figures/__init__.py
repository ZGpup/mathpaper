from mathpaper.figures.base import Figure
from mathpaper.figures.matplotlib import MatplotlibFigure
from mathpaper.figures.manim import ManimFigure
from mathpaper.figures.geometry import LadderDiagram, TriangleDiagram
from mathpaper.figures.coordinate_plane import ImplicitCurveFigure

__all__ = [
    "Figure",
    "MatplotlibFigure",
    "ManimFigure",
    "TriangleDiagram",
    "LadderDiagram",
    "ImplicitCurveFigure",
]
