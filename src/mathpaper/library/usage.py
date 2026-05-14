"""Opt-in usage logging: track which problems were used, when, and in what course."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from platformdirs import user_data_dir

_LOG_DIR = Path(user_data_dir("mathpaper", "mathpaper"))
_LOG_FILE = _LOG_DIR / "usage.jsonl"


def log_usage(
    problem_id: str,
    course: str,
    title: str,
) -> None:
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "date": date.today().isoformat(),
        "course": course,
        "title": title,
        "problem_id": problem_id,
    }
    with _LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def read_usage(
    course: str | None = None,
    problem_id: str | None = None,
) -> list[dict]:
    if not _LOG_FILE.exists():
        return []
    entries = []
    with _LOG_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if course and entry.get("course", "").lower() != course.lower():
                continue
            if problem_id and entry.get("problem_id") != problem_id:
                continue
            entries.append(entry)
    return entries
