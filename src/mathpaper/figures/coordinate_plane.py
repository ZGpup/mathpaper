"""Coordinate-plane figures backed by ManimCE."""
import numpy as np

from mathpaper.figures.manim import ManimFigure


class ImplicitCurveFigure(ManimFigure):
    """Plots an implicit curve F(x, y) = 0 with an optional tangent line and marked point.

    Parameters
    ----------
    curve_fn:
        Callable f(x, y) -> float whose zero set is the curve.
    x_range:
        (x_min, x_max) for the axes.
    y_range:
        (y_min, y_max) for the axes.
    tangent_fn:
        Optional callable x -> y for the tangent line.
    tangent_x_range:
        (x_min, x_max) segment of the tangent line to draw.
    highlight_point:
        Optional (x, y) to mark with a dot.
    highlight_label:
        LaTeX string for the dot label (placed upper-right of dot).
    pi_x_labels:
        If True, replace numeric x-axis labels with multiples of π.
    title:
        LaTeX string placed below the axes.
    filename:
        Output PNG filename stored in the temp asset directory.
    width:
        Typst width string passed through to the image tag.
    """

    def __init__(
        self,
        curve_fn,
        x_range: tuple,
        y_range: tuple,
        *,
        tangent_fn=None,
        tangent_x_range: tuple | None = None,
        highlight_point: tuple | None = None,
        highlight_label: str | None = None,
        pi_x_labels: bool = False,
        title: str | None = None,
        filename: str = "implicit_curve.png",
        width: str = "100%",
    ):
        from manim import (
            Scene, Axes, MathTex, Dot, DashedVMobject, VGroup,
            RED, BLUE, BLACK, UR, DOWN, LEFT,
        )

        x_min, x_max = x_range
        y_min, y_max = y_range

        # Capture all parameters for closure — avoids late-binding surprises
        _curve_fn = curve_fn
        _tangent_fn = tangent_fn
        _tangent_x_range = tangent_x_range
        _highlight_point = highlight_point
        _highlight_label = highlight_label
        _pi_x_labels = pi_x_labels
        _title = title

        class _Scene(Scene):
            def construct(self):
                axes = Axes(
                    x_range=[x_min, x_max],
                    y_range=[y_min, y_max],
                    x_length=7.5,
                    y_length=3.8,
                    tips=False,
                    axis_config={
                        "color": BLACK,
                        "include_numbers": False,
                        "stroke_width": 1.5,
                    },
                )

                curve = axes.plot_implicit_curve(
                    _curve_fn,
                    color=RED,
                    stroke_width=7.5,
                )

                items = [axes, curve]

                if _tangent_fn is not None:
                    tx_min, tx_max = _tangent_x_range if _tangent_x_range else (x_min, x_max)
                    tangent_path = axes.plot(
                        _tangent_fn,
                        x_range=[tx_min, tx_max],
                        color=BLUE,
                        stroke_width=5,
                    )
                    items.append(DashedVMobject(tangent_path, num_dashes=18, dashed_ratio=0.5))

                if _highlight_point is not None:
                    dot = Dot(axes.c2p(*_highlight_point), color=BLACK, radius=0.07)
                    items.append(dot)
                    if _highlight_label:
                        lbl = MathTex(_highlight_label, color=BLACK).scale(0.65)
                        lbl.next_to(dot, UR, buff=0.15)
                        items.append(lbl)

                # x-axis labels
                x_labels = VGroup()
                if _pi_x_labels:
                    max_n = int(x_max / np.pi)
                    for n in range(0, max_n + 1):
                        xv = n * np.pi
                        if xv < x_min - 0.01 or xv > x_max + 0.01:
                            continue
                        tex = "0" if n == 0 else (r"\pi" if n == 1 else rf"{n}\pi")
                        lbl = MathTex(tex, color=BLACK).scale(0.55)
                        lbl.next_to(axes.c2p(xv, 0), DOWN, buff=0.22)
                        x_labels.add(lbl)
                else:
                    for xv in np.arange(
                        np.ceil(x_min), np.floor(x_max) + 1, 1.0
                    ):
                        if xv == 0:
                            continue
                        lbl = MathTex(str(int(xv)), color=BLACK).scale(0.55)
                        lbl.next_to(axes.c2p(xv, 0), DOWN, buff=0.22)
                        x_labels.add(lbl)
                if len(x_labels) > 0:
                    items.append(x_labels)

                # y-axis integer labels
                y_labels = VGroup()
                for yv in range(int(np.ceil(y_min)), int(np.floor(y_max)) + 1):
                    if yv == 0:
                        continue
                    lbl = MathTex(str(yv), color=BLACK).scale(0.55)
                    lbl.next_to(axes.c2p(0, yv), LEFT, buff=0.2)
                    y_labels.add(lbl)
                if len(y_labels) > 0:
                    items.append(y_labels)

                if _title:
                    title_mob = MathTex(_title, color=BLACK).scale(0.75)
                    title_mob.next_to(axes, DOWN, buff=0.3)
                    items.append(title_mob)

                self.add(*items)

        super().__init__(_Scene, filename, width)




