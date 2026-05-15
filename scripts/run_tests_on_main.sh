#!/usr/bin/env bash
# Run the full pytest suite — but only when committing to main.
# Installed as a pre-commit hook via .pre-commit-config.yaml.
set -e

branch="$(git symbolic-ref --short HEAD 2>/dev/null || echo '')"
if [ "$branch" != "main" ]; then
  echo "[pytest-on-main] on branch '$branch' — skipping tests."
  exit 0
fi

echo "[pytest-on-main] on main — running pytest..."

# Prefer the project conda env if it exists; otherwise rely on whatever
# python is on PATH (the developer's active env).
if command -v conda >/dev/null 2>&1 && conda env list 2>/dev/null | grep -q '^mathpaper-dev '; then
  conda run --no-capture-output -n mathpaper-dev pytest -q tests/
else
  pytest -q tests/
fi
