"""Geometry diagrams for related rates and other math problems, backed by ManimCE."""
import numpy as np

from mathpaper.figures.manim import ManimFigure


class TriangleDiagram(ManimFigure):
    """SAS triangle schematic: two labeled sides and an included angle.

    Labels are LaTeX math strings without dollar-sign delimiters,
    e.g. a_label=r"a = 2", theta_label=r"\\theta".
    """

    def __init__(
        self,
        a: float,
        b: float,
        a_label: str | None = None,
        b_label: str | None = None,
        theta_label: str = r"\theta",
        display_angle_deg: float = 60.0,
        width: str = "100%",
        filename: str = "triangle_diagram.png",
    ):
        from manim import Scene, Line, Arc, MathTex, BLACK, DOWN

        _a = float(a)
        _b = float(b)
        _a_label = a_label or f"a = {a}"
        _b_label = b_label or f"b = {b}"
        _theta_label = theta_label
        _angle = display_angle_deg

        class _Scene(Scene):
            def construct(self):
                ang = np.radians(_angle)

                p0 = np.array([0.0, 0.0, 0.0])
                p1 = np.array([_a, 0.0, 0.0])
                p2 = np.array([_b * np.cos(ang), _b * np.sin(ang), 0.0])

                # Scale so longest side ≈ 3 Manim units, then center on centroid
                longest = max(
                    np.linalg.norm(p1 - p0),
                    np.linalg.norm(p2 - p0),
                    np.linalg.norm(p2 - p1),
                )
                s = 3.0 / longest
                p0, p1, p2 = p0 * s, p1 * s, p2 * s
                centroid = (p0 + p1 + p2) / 3
                p0, p1, p2 = p0 - centroid, p1 - centroid, p2 - centroid

                side_a = Line(p0, p1, color=BLACK, stroke_width=2.5)
                side_b = Line(p0, p2, color=BLACK, stroke_width=2.5)
                side_c = Line(p1, p2, color=BLACK, stroke_width=2.5)

                # Label for side a — below the horizontal bottom edge
                lbl_a = MathTex(_a_label, color=BLACK).scale(0.75)
                lbl_a.next_to(side_a, DOWN, buff=0.2)

                # Label for side b — offset perpendicular to the outer left side
                dir_b = (p2 - p0) / np.linalg.norm(p2 - p0)
                perp_b = np.array([-dir_b[1], dir_b[0], 0.0])
                lbl_b = MathTex(_b_label, color=BLACK).scale(0.75)
                lbl_b.move_to((p0 + p2) / 2 + perp_b * 0.42)

                # Angle arc and label at p0 (the angle vertex)
                arc_r = 0.45
                arc = Arc(
                    radius=arc_r,
                    start_angle=0,
                    angle=ang,
                    arc_center=p0,
                    color=BLACK,
                    stroke_width=1.5,
                )
                mid_ang = ang / 2
                lbl_theta = MathTex(_theta_label, color=BLACK).scale(0.8)
                lbl_theta.move_to(
                    p0 + (arc_r + 0.38) * np.array([np.cos(mid_ang), np.sin(mid_ang), 0.0])
                )

                self.add(side_a, side_b, side_c, lbl_a, lbl_b, arc, lbl_theta)

        super().__init__(_Scene, filename, width)


class LadderDiagram(ManimFigure):
    """Ladder-against-wall diagram for related rates problems.

    Labels are LaTeX math strings without dollar-sign delimiters.
    Use r"\\text{ ft}" for unit suffixes, e.g. x_label=r"x = 6 \\text{ ft}".
    """

    def __init__(
        self,
        x: float,
        ladder_len: float,
        x_label: str | None = None,
        y_label: str = "y",
        len_label: str | None = None,
        width: str = "100%",
        filename: str = "ladder_diagram.png",
    ):
        from manim import Scene, Line, Arrow, MathTex, VMobject, BLACK, UP, RIGHT

        _x = float(x)
        _y = float(np.sqrt(ladder_len**2 - x**2))
        _x_label = x_label or f"x = {x}"
        _y_label = y_label
        _len_label = len_label or (
            str(int(ladder_len)) if float(ladder_len).is_integer() else str(ladder_len)
        )

        class _Scene(Scene):
            def construct(self):
                # Scale so the taller dimension ≈ 3.5 Manim units
                sc = 3.5 / max(_y, _x)
                sx = _x * sc
                sy = _y * sc

                O = np.array([0.0, 0.0, 0.0])
                wall_top = np.array([0.0, sy, 0.0])
                floor_end = np.array([sx, 0.0, 0.0])

                ext = 0.3
                wall = Line(O, wall_top + np.array([0.0, ext, 0.0]), color=BLACK, stroke_width=2.5)
                floor = Line(O, floor_end + np.array([ext, 0.0, 0.0]), color=BLACK, stroke_width=2.5)

                # Right-angle marker: open L at the wall-floor junction
                ra_s = 0.22
                ra = VMobject(stroke_color=BLACK, stroke_width=1.2, fill_opacity=0)
                ra.set_points_as_corners([
                    O + np.array([ra_s, 0.0, 0.0]),
                    O + np.array([ra_s, ra_s, 0.0]),
                    O + np.array([0.0, ra_s, 0.0]),
                ])

                ladder = Line(wall_top, floor_end, color=BLACK, stroke_width=2.5)

                # Dots at ladder endpoints
                from manim import Dot
                dot_top = Dot(wall_top, color=BLACK, radius=0.06)
                dot_bot = Dot(floor_end, color=BLACK, radius=0.06)

                # Rate arrows
                arr_dx = Arrow(
                    start=floor_end + np.array([0.1, 0.2, 0.0]),
                    end=floor_end + np.array([0.7, 0.2, 0.0]),
                    color=BLACK, stroke_width=1.5, buff=0,
                    max_tip_length_to_length_ratio=0.4,
                )
                arr_dy = Arrow(
                    start=wall_top + np.array([-0.35, 0.0, 0.0]),
                    end=wall_top + np.array([-0.35, -0.5, 0.0]),
                    color=BLACK, stroke_width=1.5, buff=0,
                    max_tip_length_to_length_ratio=0.4,
                )

                lbl_x = MathTex(_x_label, color=BLACK).scale(0.65)
                lbl_x.move_to(floor_end / 2 + np.array([0.0, -0.42, 0.0]))

                lbl_y = MathTex(_y_label, color=BLACK).scale(0.7)
                lbl_y.move_to(wall_top / 2 + np.array([-0.48, 0.0, 0.0]))

                # Ladder length near midpoint, perpendicular offset (matches matplotlib convention)
                mid_ladder = (wall_top + floor_end) / 2
                perp_angle = np.arctan2(sy, sx) + np.pi / 2
                perp = 0.35 * np.array([np.cos(perp_angle), np.sin(perp_angle), 0.0])
                lbl_len = MathTex(_len_label, color=BLACK).scale(0.65)
                lbl_len.next_to(mid_ladder, UP+RIGHT)

                self.add(wall, floor, ra, ladder, dot_top, dot_bot,
                         arr_dx, arr_dy, lbl_x, lbl_y, lbl_len)

        super().__init__(_Scene, filename, width)



