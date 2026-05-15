from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class Block:
    stem: Any
    body: Any                       # FreeResponse | Parts
    answer: Any | None = None       # top-level answer for solution mode
    figure: Any | None = None
    figure_layout: Any | None = None
    points: int | None = None
    keep_together: bool = True


def Problem(prompt, answer_space="1in", answer=None, points=None, keep_together=True):
    """Convenience constructor: a single free-response block."""
    from mathpaper.document.parts import FreeResponse
    return Block(
        stem=prompt,
        body=FreeResponse(answer_space),
        answer=answer,
        points=points,
        keep_together=keep_together,
    )


def MultipartProblem(
    prompt,
    parts=None,
    layout=None,
    figure=None,
    figure_layout=None,
    points=None,
    keep_together=True,
):
    """Convenience constructor: a block whose body is a parts list.

    ``parts`` may be a plain list[Part] (old style) or a Parts instance
    (new style, which carries its own layout and label scheme).
    """
    from mathpaper.document.parts import Parts
    if isinstance(parts, Parts):
        body = parts
    else:
        body = Parts(parts=parts or [], layout=layout)
    return Block(
        stem=prompt,
        body=body,
        figure=figure,
        figure_layout=figure_layout,
        points=points,
        keep_together=keep_together,
    )
