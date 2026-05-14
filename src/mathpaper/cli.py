"""Command-line interface for mathpaper."""
import argparse
import subprocess
import sys


def _cmd_check_typst(args) -> None:
    try:
        result = subprocess.run(["typst", "--version"], capture_output=True, text=True, check=True)
        print(f"typst found: {result.stdout.strip()}")
    except FileNotFoundError:
        print("typst not found on PATH. Install from https://typst.app/", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(prog="mathpaper", description="mathpaper CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("check-typst", help="Check that typst is installed and on PATH")

    args = parser.parse_args()

    if args.command == "check-typst":
        _cmd_check_typst(args)
    else:
        parser.print_help()
