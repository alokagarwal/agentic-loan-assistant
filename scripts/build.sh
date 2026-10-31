#!/usr/bin/env bash
# Builds dist/agent.zip for AgentCore direct code deploy (Linux ARM64, Python 3.13).
set -euo pipefail

cd "$(dirname "$0")/.."

# Package name comes from pyproject.toml (loan-assistant -> loan_assistant)
PKG=$(uv run --no-sync python -c 'import tomllib;print(tomllib.load(open("pyproject.toml","rb"))["project"]["name"].replace("-","_"))')
BUILD=build
OUT=dist/agent.zip

rm -rf "$BUILD" dist
mkdir -p "$BUILD" dist

# 1. Install dependencies for AgentCore's platform (ARM64 Linux), not this machine
uv export --no-dev --no-hashes --no-emit-project -o "$BUILD.requirements.txt" >/dev/null
uv pip install \
  --target "$BUILD" \
  --python-platform aarch64-manylinux_2_28 \
  --python-version 3.13 \
  --only-binary=:all: \
  -r "$BUILD.requirements.txt"
rm -f "$BUILD.requirements.txt"

# 2. Add the code
cp agent.py "$BUILD/"
cp -r "src/$PKG" "$BUILD/"
[ -d samples ] && cp -r samples "$BUILD/"

# 3. Zip it
(cd "$BUILD" && zip -qr "../$OUT" . -x '*__pycache__*')
echo "Built $OUT ($(du -h "$OUT" | cut -f1))"
