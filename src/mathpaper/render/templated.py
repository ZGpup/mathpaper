"""Renderer for TemplatedProblem: stages per-problem subdirs and assembles main.typ.

Build layout produced for a Test that contains TemplatedProblems::

    out/
      mathpaper.typ            # copy of the helper library (also per-subdir)
      main.typ                 # student mode
      answer_key.typ           # solution mode
      main.pdf
      answer_key.pdf
      problem_001/
        problem.typ            # staged copy of the author's .typ
        context.json           # rendered from the TemplatedProblem.context dict
        mathpaper.typ          # local copy so Tinymist can preview standalone
        <figure assets>        # one PNG per Figure in TemplatedProblem.figures
      problem_002/
        ...

The master ``main.typ`` sets the solution-mode state and ``#include``s each
subdirectory's ``problem.typ``. Each subdir is self-contained, which makes it
trivial to compose tests by simply collecting subdirs into a build root.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from mathpaper.document.templated import TemplatedProblem
from mathpaper.render.escaping import escape_typst_text


# Path to the canonical helper library shipped with the package.
_LIB_TYP = Path(__file__).resolve().parents[1] / "templates" / "typst" / "lib.typ"


def stage_templated_problem(
    problem: TemplatedProblem,
    out_dir: Path,
    number: int,
) -> str:
    """Stage one TemplatedProblem into its own subdir under ``out_dir``.

    Returns the subdir name (e.g. ``"problem_001"``), which the master main.typ
    uses to ``#include`` the problem.
    """
    subdir_name = f"problem_{number:03d}"
    subdir = out_dir / subdir_name
    subdir.mkdir(parents=True, exist_ok=True)

    # Stage the .typ file. The author's filename is irrelevant in the build
    # layout — we always call it problem.typ inside the subdir.
    template_src = problem.resolved_template()
    if not template_src.exists():
        raise FileNotFoundError(
            f"TemplatedProblem template not found: {template_src}"
        )
    shutil.copy2(template_src, subdir / "problem.typ")

    # Copy the helper library so the staged problem is standalone.
    shutil.copy2(_LIB_TYP, subdir / "mathpaper.typ")

    # Stage figures (referenced by filename from the context dict).
    for figure in problem.figures:
        _copy_figure(figure, subdir)

    # Stage extra files verbatim.
    for extra in problem.extra_files:
        src = Path(extra)
        if src.exists():
            shutil.copy2(src, subdir / src.name)

    # Build the context dict — inject ``number`` and ``points`` if absent so
    # the .typ template can read them without the author wiring them through
    # every problem.
    ctx = dict(problem.context)
    ctx.setdefault("number", number)
    if problem.points is not None:
        ctx.setdefault("points", problem.points)

    (subdir / "context.json").write_text(
        json.dumps(ctx, indent=2), encoding="utf-8"
    )

    return subdir_name


def _copy_figure(figure: Any, subdir: Path) -> None:
    """Copy a Figure-like object (anything with .path and .asset_name) into subdir."""
    src = Path(figure.path)
    if not src.exists():
        return
    dest_name = getattr(figure, "asset_name", src.name)
    shutil.copy2(src, subdir / dest_name)


def render_templated_main(
    *,
    title: str,
    course: str = "",
    version: str = "",
    subdirs: list[str],
    solution_mode: bool,
) -> str:
    """Render the master main.typ that #includes each staged problem subdir."""
    title_t = escape_typst_text(title)
    course_t = escape_typst_text(course)
    version_t = escape_typst_text(version)

    right_parts = []
    if course:
        right_parts.append(course_t)
    if version:
        right_parts.append(f"Version {version_t}")
    right_line = "  ".join(right_parts)

    mode_value = "true" if solution_mode else "false"

    lines = [
        '#set page(paper: "us-letter", margin: 1in)',
        '#set text(font: "New Computer Modern", size: 11pt)',
        "#set par(leading: 0.6em)",
        "#show math.equation: set text(size: 11pt)",
        "",
        '#import "mathpaper.typ": set-solution-mode',
        f"#set-solution-mode({mode_value})",
        "",
        f"#grid(columns: (1fr, 1fr), align: (left, right))[*{title_t}*][{right_line}]",
        "Name: #box(width: 3in, line(length: 100%, stroke: 0.5pt))",
        "",
        "#line(length: 100%, stroke: 0.5pt)",
        "#v(0.3em)",
        "",
    ]
    for subdir in subdirs:
        lines.append(f'#include "{subdir}/problem.typ"')
        lines.append("")
    return "\n".join(lines)


def stage_root_lib(out_dir: Path) -> None:
    """Copy the helper library into the build root for the master main.typ."""
    shutil.copy2(_LIB_TYP, out_dir / "mathpaper.typ")
