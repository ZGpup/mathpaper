"""ProblemLibrary: scan, index, and search @problem-decorated Python files."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from mathpaper.library.decorator import ProblemDef


class ProblemLibrary:
    def __init__(self, *library_paths: str | Path):
        self._problems: list[ProblemDef] = []
        self._by_id: dict[str, ProblemDef] = {}
        for path in library_paths:
            self._load_path(Path(path))

    def _load_path(self, path: Path) -> None:
        if path.is_file() and path.suffix == ".py":
            self._load_file(path)
        elif path.is_dir():
            for py_file in sorted(path.rglob("*.py")):
                if py_file.name.startswith("_"):
                    continue
                self._load_file(py_file)

    def _load_file(self, path: Path) -> None:
        module_name = f"_mathpaper_problems_{path.stem}_{abs(hash(str(path)))}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            return
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"Warning: failed to load problem file {path}: {e}")
            return

        for defn in getattr(module, "_PROBLEMS", []):
            if defn.id in self._by_id:
                print(f"Warning: duplicate problem id '{defn.id}' in {path}, skipping")
                continue
            self._problems.append(defn)
            self._by_id[defn.id] = defn

    def all(self) -> list[ProblemDef]:
        return list(self._problems)

    def get(self, id: str) -> ProblemDef:
        if id not in self._by_id:
            raise KeyError(f"No problem with id '{id}'")
        return self._by_id[id]

    def search(
        self,
        tags: list[str] | None = None,
        topic: str | None = None,
        keywords: str | None = None,
        course: str | None = None,
        difficulty: str | None = None,
    ) -> list[ProblemDef]:
        results = self._problems
        if tags:
            tags_lower = [t.lower() for t in tags]
            results = [p for p in results if all(t in [x.lower() for x in p.tags] for t in tags_lower)]
        if topic:
            results = [p for p in results if p.topic.lower() == topic.lower()]
        if course:
            results = [p for p in results if p.course.lower() == course.lower()]
        if difficulty:
            results = [p for p in results if p.difficulty.lower() == difficulty.lower()]
        if keywords:
            kw = keywords.lower()
            results = [p for p in results if kw in p.id.lower() or kw in p.description.lower()]
        return results

    def topics(self) -> list[str]:
        return sorted({p.topic for p in self._problems})

    def courses(self) -> list[str]:
        return sorted({p.course for p in self._problems if p.course})

    def all_tags(self) -> list[str]:
        tags: set[str] = set()
        for p in self._problems:
            tags.update(p.tags)
        return sorted(tags)

    def build_catalog(self, out_path: str | Path) -> None:
        import json
        from datetime import datetime, timezone

        out = Path(out_path)
        catalog = {
            "generated": datetime.now(timezone.utc).isoformat(),
            "problems": [p.to_dict() for p in self._problems],
        }
        out.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
        print(f"Catalog written: {out} ({len(self._problems)} problems)")
