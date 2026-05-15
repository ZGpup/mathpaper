#!/usr/bin/env bash
# Pre-push gate: run pytest only when one of the refs being pushed is main.
# Installed via .pre-commit-config.yaml (stage: pre-push).
#
# Git's pre-push hook protocol: stdin contains one line per ref being pushed,
# in the form  "<local_ref> <local_sha> <remote_ref> <remote_sha>".
# The pre-commit framework forwards that stdin to this script unchanged.
set -e

pushing_main=0
while read -r local_ref local_sha remote_ref remote_sha; do
  if [ "$remote_ref" = "refs/heads/main" ]; then
    pushing_main=1
    break
  fi
done

if [ "$pushing_main" -eq 0 ]; then
  echo "[pytest-on-push-to-main] not pushing to main — skipping tests."
  exit 0
fi

echo "[pytest-on-push-to-main] pushing to main — running pytest..."

if command -v conda >/dev/null 2>&1 && conda env list 2>/dev/null | grep -q '^mathpaper-dev '; then
  conda run --no-capture-output -n mathpaper-dev pytest -q tests/
else
  pytest -q tests/
fi
