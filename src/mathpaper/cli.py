"""Command-line interface for mathpaper."""
import argparse
import subprocess
import sys
from pathlib import Path


def _cmd_check_typst(args) -> None:
    try:
        result = subprocess.run(["typst", "--version"], capture_output=True, text=True, check=True)
        print(f"typst found: {result.stdout.strip()}")
    except FileNotFoundError:
        print("typst not found on PATH. Install from https://typst.app/", file=sys.stderr)
        sys.exit(1)


def _cmd_index(args) -> None:
    from mathpaper.library import ProblemLibrary

    path = Path(args.path)
    if not path.exists():
        print(f"Error: path '{path}' does not exist", file=sys.stderr)
        sys.exit(1)

    lib = ProblemLibrary(path)
    out = path / "catalog.json"
    lib.build_catalog(out)


def _cmd_search(args) -> None:
    from mathpaper.library import ProblemLibrary

    path = Path(args.path)
    if not path.exists():
        print(f"Error: path '{path}' does not exist", file=sys.stderr)
        sys.exit(1)

    lib = ProblemLibrary(path)
    results = lib.search(
        tags=args.tag or None,
        topic=args.topic,
        course=args.course,
        difficulty=args.difficulty,
        keywords=args.keywords,
    )

    if not results:
        print("No matching problems found.")
        return

    col_w = max(len(r.id) for r in results) + 2
    for r in results:
        tags = ", ".join(r.tags)
        print(f"  {r.id:<{col_w}}  [{r.difficulty:6}]  {r.description}")
        print(f"  {'':>{col_w}}  topic={r.topic!r}  tags=[{tags}]")
        print()


def _cmd_explore(args) -> None:
    app_path = Path(__file__).parent / "app.py"
    problems_path = getattr(args, "path", None) or "./problems"

    try:
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path), "--", problems_path],
            check=True,
        )
    except FileNotFoundError:
        print(
            "streamlit not found. Install it with:\n  pip install streamlit",
            file=sys.stderr,
        )
        sys.exit(1)


def _cmd_build(args) -> None:
    script = Path(args.script)
    if not script.exists():
        print(f"Error: script '{script}' does not exist", file=sys.stderr)
        sys.exit(1)

    env = {**__import__("os").environ}
    if args.no_render_figures:
        env["MATHPAPER_NO_RENDER_FIGURES"] = "1"
    if args.force_render_figures:
        env["MATHPAPER_FORCE_RENDER_FIGURES"] = "1"

    result = subprocess.run([sys.executable, str(script)], env=env)
    sys.exit(result.returncode)


def _cmd_history(args) -> None:
    from mathpaper.library.usage import read_usage

    entries = read_usage(course=args.course or None)
    if not entries:
        print("No usage history found.")
        return

    entries.sort(key=lambda e: e.get("date", ""), reverse=True)
    for e in entries:
        print(f"  {e.get('date', '?')}  {e.get('course', '?')!r}  {e.get('problem_id', '?')}  ({e.get('title', '')})")


def main() -> None:
    parser = argparse.ArgumentParser(prog="mathpaper", description="mathpaper CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check-typst", help="Check that typst is installed and on PATH")

    p_build = sub.add_parser("build", help="Run a mathpaper build script")
    p_build.add_argument("script", help="Path to the Python build script")
    p_build.add_argument(
        "--no-render-figures",
        action="store_true",
        dest="no_render_figures",
        help="Skip figure rendering; reuse cached PNGs from .mathpaper_cache/figures/",
    )
    p_build.add_argument(
        "--force-render-figures",
        action="store_true",
        dest="force_render_figures",
        help="Ignore the figure cache and re-render every figure from scratch.",
    )

    p_index = sub.add_parser("index", help="Build catalog.json from a problems directory")
    p_index.add_argument("path", nargs="?", default="./problems", help="Path to problems directory")

    p_search = sub.add_parser("search", help="Search problems in a problems directory")
    p_search.add_argument("path", nargs="?", default="./problems", help="Path to problems directory")
    p_search.add_argument("--tag", action="append", dest="tag", help="Filter by tag (repeatable)")
    p_search.add_argument("--topic", help="Filter by topic")
    p_search.add_argument("--course", help="Filter by course")
    p_search.add_argument("--difficulty", choices=["easy", "medium", "hard"], help="Filter by difficulty")
    p_search.add_argument("--keywords", help="Filter by keywords in id or description")

    p_explore = sub.add_parser("explore", help="Open the interactive browser test builder")
    p_explore.add_argument("path", nargs="?", default="./problems", help="Path to problems directory")

    p_history = sub.add_parser("history", help="Show problem usage history")
    p_history.add_argument("--course", help="Filter by course name")

    args = parser.parse_args()

    dispatch = {
        "check-typst": _cmd_check_typst,
        "build": _cmd_build,
        "index": _cmd_index,
        "search": _cmd_search,
        "explore": _cmd_explore,
        "history": _cmd_history,
    }

    if args.command in dispatch:
        dispatch[args.command](args)
    else:
        parser.print_help()
