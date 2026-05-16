"""TemplatedProblem: a problem authored as a sibling .typ file + Python context.

A TemplatedProblem pairs:
  - A hand-authored .typ file (durable, edited with Tinymist).
  - A Python-computed context dict (figures, answers, computed values).

At build time each TemplatedProblem is staged into its own subdirectory inside
the test output, alongside its context.json and any figure assets it
references. The master main.typ #includes each subdirectory's .typ.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TemplatedProblem:
    """A problem whose layout lives in a .typ file and whose data lives in Python.

    Most users construct this via an @problem-decorated function — the
    decorator resolves ``template`` to the sibling .typ file with the same
    basename as the decorated function's module, so the function body only
    needs to return values:

        @problem(id="related_rates_001", ...)
        def related_rates_001(seed=None):
            return TemplatedProblem(context={...}, points=10)

    Direct construction (without the decorator) requires an explicit
    ``template`` path.

    Parameters
    ----------
    context:
        JSON-serializable dict consumed by the .typ file via ``json("context.json")``.
    template:
        Path to the .typ file. Resolved by the @problem decorator when omitted.
    points:
        Point value for the problem; surfaced to the .typ via ``ctx.points`` if
        the context doesn't already supply it.
    figures:
        Optional list of ``Figure`` instances to stage alongside the .typ in
        the build subdir. Their ``asset_name`` is appended to the staged dir.
    extra_files:
        Optional list of additional file paths to copy into the build subdir
        (e.g. images authored outside the figure pipeline).
    """

    context: dict[str, Any] = field(default_factory=dict)
    template: str | Path | None = None
    points: int | None = None
    figures: list[Any] = field(default_factory=list)
    extra_files: list[str | Path] = field(default_factory=list)

    def resolved_template(self) -> Path:
        if self.template is None:
            raise ValueError(
                "TemplatedProblem.template is unresolved. Either pass an explicit "
                "template= path, or construct via an @problem-decorated function "
                "(which resolves the sibling .typ automatically)."
            )
        return Path(self.template)
