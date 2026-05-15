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


_LABEL_SCHEMES: dict[str, list[str]] = {
    "alpha": list("abcdefghijklmnopqrstuvwxyz"),
    "roman": [
        "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x",
        "xi", "xii", "xiii", "xiv", "xv", "xvi", "xvii", "xviii", "xix", "xx",
    ],
    "numeric": [str(i) for i in range(1, 27)],
}


def _generate_labels(scheme: str, count: int) -> list[str]:
    pool = _LABEL_SCHEMES.get(scheme, _LABEL_SCHEMES["alpha"])
    return [pool[i] if i < len(pool) else str(i + 1) for i in range(count)]


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
        name_line = "#box(width: 3in, line(length: 100%, stroke: 0.5pt))"
        return (
            f"#grid(columns: (1fr, 1fr), align: (left, right))[{parts[0]}][{'  '.join(parts[1:])}]\n"
            f"Name: {name_line}\n\n"
            "#line(length: 100%, stroke: 0.5pt)\n"
            "#v(0.3em)\n"
        )

    # ------------------------------------------------------------------
    # Top-level block
    # ------------------------------------------------------------------

    def _render_block(self, block: Any, number: int, mode: str) -> str:
        from mathpaper.document.problem import Block
        from mathpaper.document.parts import FreeResponse, Parts

        if not isinstance(block, Block):
            return f"// unknown block type: {type(block).__name__}\n"

        pts = f" ({block.points} pts)" if block.points else ""
        stem = _content_to_typst(block.stem, mode)
        lines: list[str] = [f"*{number}.{pts}* {stem}", ""]

        if isinstance(block.body, Parts):
            lines.append(self._render_parts_node(block.body, mode, block.figure, block.figure_layout))
        elif isinstance(block.body, FreeResponse):
            if mode == "solution" and block.answer is not None:
                answer = _content_to_typst(block.answer, mode)
                lines.append(f"#block(fill: luma(230), inset: 6pt, radius: 3pt)[*Answer:* {answer}]")
            else:
                lines.append(f"#v({block.body.height})")

        lines.append("")
        inner = "\n".join(lines)

        if block.keep_together:
            return f"#block(breakable: false)[\n{inner.rstrip()}\n]\n"
        return inner

    # ------------------------------------------------------------------
    # Parts (recursive)
    # ------------------------------------------------------------------

    def _render_parts_node(
        self,
        parts_node: Any,
        mode: str,
        figure: Any = None,
        figure_layout: Any = None,
    ) -> str:
        from mathpaper.document.layout import PartsGrid, SideFigure
        from mathpaper.document.parts import Parts

        layout = parts_node.layout
        columns = layout.columns if isinstance(layout, PartsGrid) else 1
        default_space = layout.answer_space if isinstance(layout, PartsGrid) else "1in"
        labels = _generate_labels(parts_node.labels, len(parts_node.parts))

        part_blocks = [
            self._render_part(label, part, mode, default_space)
            for label, part in zip(labels, parts_node.parts)
        ]

        if columns == 1:
            body = "\n\n".join(part_blocks)
        else:
            col_spec = ", ".join(["1fr"] * columns)
            cells = ",\n".join(f"[\n{b}\n]" for b in part_blocks)
            body = f"#grid(columns: ({col_spec}), column-gutter: 1em, row-gutter: 1em,\n{cells}\n)"

        if figure is not None:
            fig_typst = _content_to_typst(figure, mode)
            if isinstance(figure_layout, SideFigure):
                fl = figure_layout
                return (
                    f"#grid(columns: (1fr, {fl.width}), column-gutter: 1em)[\n"
                    f"{body}\n"
                    f"][{fig_typst}]"
                )
            return f"{fig_typst}\n\n{body}"

        return body

    def _render_part(self, label: str, part: Any, mode: str, default_space: str) -> str:
        from mathpaper.document.parts import FreeResponse, Parts

        prompt = _content_to_typst(part.prompt, mode)

        if isinstance(part.body, Parts):
            # Nested parts — recurse; the sub-Parts carries its own labels and layout
            sub = self._render_parts_node(part.body, mode)
            if part.body.indent:
                sub = f"#pad(left: 1.5em)[\n{sub}\n]"
            return f"*{label}.* {prompt}\n\n{sub}"

        # FreeResponse leaf
        # part.answer_space takes priority; fall back to the grid's default
        height = part.answer_space or (
            part.body.height if isinstance(part.body, FreeResponse) else default_space
        )
        if mode == "solution" and part.answer is not None:
            answer = _content_to_typst(part.answer, mode)
            return (
                f"*{label}.* {prompt}\n\n"
                f"#block(fill: luma(230), inset: 4pt, radius: 3pt)[{answer}]"
            )
        return f"*{label}.* {prompt}\n\n#v({height})"
