from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Test:
    title: str
    course: str = ""
    version: str = ""
    _blocks: list[Any] = field(default_factory=list, repr=False)

    # Tell pytest this is not a test class.
    __test__ = False

    def add(self, block: Any) -> None:
        self._blocks.append(block)

    def to_typst(self, mode: str = "student") -> str:
        """Render the test as a single Typst string (legacy Block path).

        TemplatedProblem instances cannot be serialized to a single string —
        they are rendered via the per-subdir staging path in ``build()``.
        """
        from mathpaper.document.templated import TemplatedProblem
        from mathpaper.render.typst import TypstRenderer

        if any(isinstance(b, TemplatedProblem) for b in self._blocks):
            raise RuntimeError(
                "Test contains TemplatedProblem(s); use build() to render the "
                "per-subdir layout, or to_typst() on a test containing only "
                "legacy Block problems."
            )
        return TypstRenderer().render(self, mode)

    def write_typst(self, out_dir: str | Path, mode: str = "student") -> Path:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        name = "main" if mode == "student" else "answer_key"
        path = out / f"{name}.typ"
        path.write_text(self.to_typst(mode), encoding="utf-8")
        return path

    def build(self, out_dir: str | Path) -> None:
        from mathpaper.document.templated import TemplatedProblem

        if any(isinstance(b, TemplatedProblem) for b in self._blocks):
            self._build_templated(Path(out_dir))
        else:
            self._build_legacy(Path(out_dir))

    # ------------------------------------------------------------------
    # New (TemplatedProblem) build path
    # ------------------------------------------------------------------

    def _build_templated(self, out: Path) -> None:
        from mathpaper.document.templated import TemplatedProblem
        from mathpaper.render.compiler import compile_typst, typst_available
        from mathpaper.render.templated import (
            render_templated_main,
            stage_root_lib,
            stage_templated_problem,
        )

        out.mkdir(parents=True, exist_ok=True)
        stage_root_lib(out)

        subdirs: list[str] = []
        for i, block in enumerate(self._blocks, start=1):
            if not isinstance(block, TemplatedProblem):
                raise TypeError(
                    "Mixed Block/TemplatedProblem tests are not supported. "
                    "Convert all blocks to TemplatedProblem, or use the legacy "
                    "build path with only Block instances."
                )
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

        self._write_manifest(out, templated=True)

    # ------------------------------------------------------------------
    # Legacy (Block) build path
    # ------------------------------------------------------------------

    def _build_legacy(self, out: Path) -> None:
        from mathpaper.render.assets import collect_assets
        from mathpaper.render.compiler import compile_typst, typst_available

        out.mkdir(parents=True, exist_ok=True)
        assets_dir = out / "assets"
        collect_assets(self._blocks, assets_dir)

        student_typ = self.write_typst(out, mode="student")
        key_typ = self.write_typst(out, mode="solution")

        if typst_available():
            compile_typst(student_typ, out / "main.pdf")
            compile_typst(key_typ, out / "answer_key.pdf")
        else:
            print("Warning: typst not found on PATH — skipping PDF compilation.")

        self._write_manifest(out, templated=False)

    def _write_manifest(self, out: Path, *, templated: bool) -> None:
        import mathpaper
        from mathpaper.document.templated import TemplatedProblem

        problems = []
        for i, b in enumerate(self._blocks):
            entry = {"index": i + 1}
            if isinstance(b, TemplatedProblem):
                entry["kind"] = "templated"
                entry["template"] = str(b.resolved_template())
                entry["points"] = b.points
            else:
                entry["kind"] = "block"
                entry["body"] = type(getattr(b, "body", b)).__name__
                entry["points"] = getattr(b, "points", None)
            problems.append(entry)

        manifest = {
            "title": self.title,
            "course": self.course,
            "version": self.version,
            "created_by": f"mathpaper {mathpaper.__version__}",
            "templated": templated,
            "problems": problems,
        }
        (out / "manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
