"""Matplotlib-backed figure base class."""
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from mathpaper.figures.base import Figure


class MatplotlibFigure(Figure):
    """A Figure whose content is rendered from a matplotlib Figure object.

    Subclasses build a matplotlib Figure in their __init__ and call
    super().__init__(mpl_fig, filename, width) to render it to SVG and
    register it as a Figure asset. The temp file persists until the process
    exits; collect_assets copies it to the output assets/ directory.
    """

    def __init__(self, mpl_fig: "plt.Figure", filename: str, width: str = "80%"):
        tmpdir = Path(tempfile.mkdtemp())
        path = tmpdir / filename
        mpl_fig.savefig(path, format="svg", bbox_inches="tight")
        plt.close(mpl_fig)
        super().__init__(path=str(path), width=width)
