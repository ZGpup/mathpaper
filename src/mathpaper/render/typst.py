from __future__ import annotations
from typing import TYPE_CHECKING, Any

from mathpaper.render.escaping import escape_typst_text

if TYPE_CHECKING:
    from mathpaper.document.test import Test


def _content_to_typst(obj: Any, mode: str) -> str:
    if obj is None:
        return ""
    if hasattr(obj, "to_typst"):
        return obj.to_typst(mode)
    return escape_typst_text(str(obj))


class TypstRenderer:
    def render(self, test: "Test", mode: str = "student") -> str:
        lines: list[str] = []
        lines.append(self._page_setup())
        lines.append(self._header(test))
        lines.append("")
        for i, block in enumerate(test._blocks, start=1):
            lines.append(self._render_block(block, i, mode))
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Page / header
    # ------------------------------------------------------------------

    def _page_setup(self) -> str:
        return (
            "#set page(paper: \"us-letter\", margin: (top: 1in, bottom: 1in, left: 1in, right: 1in))\n"
            "#set text(font: \"New Computer Modern\", size: 11pt)\n"
            "#set par(leading: 0.6em)\n"
            "#show math.equation: set text(size: 11pt)\n"
        )

    def _header(self, test: "Test") -> str:
        parts = [f"*{escape_typst_text(test.title)}*"]
        if test.course:
            parts.append(escape_typst_text(test.course))
        if test.version:
            parts.append(f"Version {escape_typst_text(test.version)}")
        header_text = " #h(1fr) ".join(parts)
        name_line = "#box(width: 3in, line(length: 100%, stroke: 0.5pt))"
        return (
            f"#grid(columns: (1fr, 1fr), align: (left, right))[{parts[0]}][{'  '.join(parts[1:])}]\n"
            f"Name: {name_line}\n\n"
            "#line(length: 100%, stroke: 0.5pt)\n"
            "#v(0.3em)\n"
        )

    # ------------------------------------------------------------------
    # Blocks
    # ------------------------------------------------------------------

    def _render_block(self, block: Any, number: int, mode: str) -> str:
        from mathpaper.document.problem import Problem, MultipartProblem

        if isinstance(block, Problem):
            return self._render_problem(block, number, mode)
        if isinstance(block, MultipartProblem):
            return self._render_multipart(block, number, mode)
        return f"// unknown block type: {type(block).__name__}\n"

    def _render_problem(self, problem: Any, number: int, mode: str) -> str:
        lines: list[str] = []
        pts = f" ({problem.points} pts)" if problem.points else ""
        prompt = _content_to_typst(problem.prompt, mode)
        lines.append(f"*{number}.{pts}* {prompt}")
        lines.append("")

        if mode == "solution" and problem.answer is not None:
            answer = _content_to_typst(problem.answer, mode)
            lines.append(f"#block(fill: luma(230), inset: 6pt, radius: 3pt)[*Answer:* {answer}]")
        elif problem.answer_space:
            lines.append(f"#v({problem.answer_space})")

        lines.append("")
        return "\n".join(lines)

    def _render_multipart(self, problem: Any, number: int, mode: str) -> str:
        lines: list[str] = []
        pts = f" ({problem.points} pts)" if problem.points else ""
        prompt = _content_to_typst(problem.prompt, mode)
        lines.append(f"*{number}.{pts}* {prompt}")
        lines.append("")

        if problem.figure is not None:
            fig_typst = _content_to_typst(problem.figure, mode)
            from mathpaper.document.layout import SideFigure

            if isinstance(problem.figure_layout, SideFigure):
                fl = problem.figure_layout
                body_lines = self._render_parts(problem.parts, mode, problem.layout)
                lines.append(
                    f"#grid(columns: (1fr, {fl.width}), column-gutter: 1em)[\n"
                    f"{body_lines}\n"
                    f"][{fig_typst}]"
                )
            else:
                lines.append(fig_typst)
                lines.append("")
                lines.append(self._render_parts(problem.parts, mode, problem.layout))
        else:
            lines.append(self._render_parts(problem.parts, mode, problem.layout))

        lines.append("")
        return "\n".join(lines)

    def _render_parts(self, parts: list, mode: str, layout: Any) -> str:
        from mathpaper.document.layout import PartsGrid

        columns = layout.columns if isinstance(layout, PartsGrid) else 1
        default_space = layout.answer_space if isinstance(layout, PartsGrid) else "1in"

        labels = "abcdefghijklmnopqrstuvwxyz"
        part_blocks: list[str] = []
        for i, part in enumerate(parts):
            label = labels[i] if i < len(labels) else str(i + 1)
            prompt = _content_to_typst(part.prompt, mode)
            space = part.answer_space or default_space

            if mode == "solution" and part.answer is not None:
                answer = _content_to_typst(part.answer, mode)
                body = (
                    f"*{label}.* {prompt}\n\n"
                    f"#block(fill: luma(230), inset: 4pt, radius: 3pt)[{answer}]"
                )
            else:
                body = f"*{label}.* {prompt}\n\n#v({space})"
            part_blocks.append(body)

        if columns == 1:
            return "\n\n".join(part_blocks)

        col_spec = ", ".join(["1fr"] * columns)
        cells = ",\n".join(f"[\n{b}\n]" for b in part_blocks)
        return f"#grid(columns: ({col_spec}), column-gutter: 1em, row-gutter: 1em,\n{cells}\n)"
