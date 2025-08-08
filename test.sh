#!/usr/bin/env bash
set -euo pipefail

# Allow overriding via existing env; fallback to defaults below
export ALPACA_API_KEY="${ALPACA_API_KEY:-PKHUYUQCXLEPVHEDKBD2}"
export ALPACA_SECRET_KEY="${ALPACA_SECRET_KEY:-IpVh6OLR005NGf4Mbazlr6UYNY5uoK5nUuFF0Wyc}"

# Activate local venv if present
if [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Run all tests by default; pass through targets/args when provided
if [ "$#" -eq 0 ]; then
  uv run pytest -q tests
else
  uv run pytest -q "$@"
fi