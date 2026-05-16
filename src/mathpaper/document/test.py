from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mathpaper.document.templated import TemplatedProblem


@dataclass
class Test:
    title: str
    course: str = ""
    version: str = ""
    _blocks: list[TemplatedProblem] = field(default_factory=list, repr=False)

    # Tell pytest this is not a test class.
    __test__ = False

    def add(self, block: TemplatedProblem) -> None:
        if not isinstance(block, TemplatedProblem):
            raise TypeError(
                f"Test.add expects a TemplatedProblem, got {type(block).__name__}"
            )
        self._blocks.append(block)

    def build(self, out_dir: str | Path) -> None:
        from mathpaper.render.compiler import compile_typst, typst_available
        from mathpaper.render.templated import (
            render_templated_main,
            stage_root_lib,
            stage_templated_problem,
        )

        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        stage_root_lib(out)

        subdirs: list[str] = []
        for i, block in enumerate(self._blocks, start=1):
            subdirs.append(stage_templated_problem(block, out, i))

        student_src = render_templated_main(
            title=self.title,
            course=self.course,
            version=self.version,
            subdirs=subdirs,
            solution_mode=False,
        )
        solution_src = render_templated_main(
            title=self.title,
            course=self.course,
            version=self.version,
            subdirs=subdirs,
            solution_mode=True,
        )
        student_path = out / "main.typ"
        solution_path = out / "answer_key.typ"
        student_path.write_text(student_src, encoding="utf-8")
        solution_path.write_text(solution_src, encoding="utf-8")

        if typst_available():
            compile_typst(student_path, out / "main.pdf")
            compile_typst(solution_path, out / "answer_key.pdf")
        else:
            print("Warning: typst not found on PATH — skipping PDF compilation.")

        self._write_manifest(out)

    def _write_manifest(self, out: Path) -> None:
        import mathpaper

        problems = [
            {
                "index": i + 1,
                "template": str(b.resolved_template()),
                "points": b.points,
            }
            for i, b in enumerate(self._blocks)
        ]

        manifest = {
            "title": self.title,
            "course": self.course,
            "version": self.version,
            "created_by": f"mathpaper {mathpaper.__version__}",
            "problems": problems,
        }
        (out / "manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
