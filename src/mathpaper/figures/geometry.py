"""Simple geometry diagrams for math problems (related rates, etc.)."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from mathpaper.figures.matplotlib import MatplotlibFigure


class TriangleDiagram(MatplotlibFigure):
    """SAS triangle schematic: two labeled sides and an included angle.

    The triangle is drawn with the angle vertex at the origin, side *a*
    along the positive x-axis, and side *b* at the given display_angle
    (default 60°). Labels and the exact values of a/b are independent of
    the drawn angle — this is a conceptual schematic, not a scale drawing.
    """

    def __init__(
        self,
        a: float,
        b: float,
        a_label: str | None = None,
        b_label: str | None = None,
        theta_label: str = "θ",
        display_angle_deg: float = 60.0,
        width: str = "100%",
    ):
        a_label = a_label or f"$a = {a}$"
        b_label = b_label or f"$b = {b}$"
        ang = np.radians(display_angle_deg)

        p0 = np.array([0.0, 0.0])
        p1 = np.array([float(a), 0.0])
        p2 = np.array([float(b) * np.cos(ang), float(b) * np.sin(ang)])

        fig, ax = plt.subplots(figsize=(2.8, 2.8))
        tri = plt.Polygon([p0, p1, p2], fill=False, edgecolor="black", linewidth=1.8)
        ax.add_patch(tri)

        # Side labels
        mid_a = (p0 + p1) / 2
        mid_b = (p0 + p2) / 2
        ax.text(mid_a[0], mid_a[1] - 0.28, a_label, ha="center", va="top", fontsize=11)
        ax.text(mid_b[0] - 0.32, mid_b[1], b_label, ha="right", va="center", fontsize=11)

        # Angle arc and label
        arc = mpatches.Arc(p0, 0.6, 0.6, angle=0, theta1=0, theta2=display_angle_deg,
                           color="black", linewidth=1.2)
        ax.add_patch(arc)
        arc_mid = np.radians(display_angle_deg / 2)
        ax.text(0.44 * np.cos(arc_mid), 0.44 * np.sin(arc_mid),
                f"${theta_label}$", ha="center", va="center", fontsize=11)

        pad = 0.5
        ax.set_xlim(-pad, max(p1[0], p2[0]) + pad * 0.5)
        ax.set_ylim(-pad, p2[1] + pad * 0.5)
        ax.set_aspect("equal")
        ax.axis("off")
        fig.tight_layout(pad=0.1)

        super().__init__(fig, "triangle_diagram.svg", width=width)


class LadderDiagram(MatplotlibFigure):
    """Ladder-against-wall diagram for related rates problems.

    Draws the wall (left), floor (bottom), right-angle marker, ladder, and
    rate arrows. Labels x (base distance), y (wall height), and ladder length.
    """

    def __init__(
        self,
        x: float,
        ladder_len: float,
        x_label: str | None = None,
        y_label: str = "y",
        len_label: str | None = None,
        width: str = "28%",
    ):
        x_label = x_label or f"$x = {x}$ ft"
        len_label = len_label or f"{ladder_len} ft"
        y_val = float(np.sqrt(ladder_len**2 - x**2))

        fig, ax = plt.subplots(figsize=(2.5, 3.2))

        # Wall and floor
        wall_h = y_val + 0.6
        ax.plot([0, 0], [0, wall_h], "k-", linewidth=2)
        ax.plot([0, x + 0.7], [0, 0], "k-", linewidth=2)

        # Right-angle marker
        s = 0.25
        ax.plot([s, s, 0], [0, s, s], "k-", linewidth=1)

        # Ladder
        ax.plot([0, x], [y_val, 0], "k-", linewidth=2.5)

        # Rate arrows
        arr = dict(arrowstyle="->", color="black", lw=1.4)
        ax.annotate("", xy=(x + 0.65, 0.18), xytext=(x + 0.1, 0.18), arrowprops=arr)
        ax.annotate("", xy=(-0.3, y_val - 0.55), xytext=(-0.3, y_val - 0.05), arrowprops=arr)

        # Labels
        ax.text(x / 2, -0.35, x_label, ha="center", va="top", fontsize=9.5)
        ax.text(-0.5, y_val / 2, f"${y_label}$", ha="center", va="center", fontsize=11)
        # Ladder length near midpoint, offset slightly above the line
        mid_x, mid_y = x / 2, y_val / 2
        perp_angle = np.arctan2(y_val, x) + np.pi / 2
        offset = 0.28
        ax.text(
            mid_x + offset * np.cos(perp_angle),
            mid_y + offset * np.sin(perp_angle),
            len_label,
            ha="center",
            va="center",
            fontsize=9.5,
        )

        # Dot at each endpoint
        ax.plot([0, x], [y_val, 0], "ko", markersize=4)

        ax.set_xlim(-0.75, x + 1.0)
        ax.set_ylim(-0.65, wall_h + 0.1)
        ax.set_aspect("equal")
        ax.axis("off")
        fig.tight_layout(pad=0.1)

        super().__init__(fig, "ladder_diagram.svg", width=width)
