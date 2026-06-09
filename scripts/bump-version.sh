#!/usr/bin/env bash
set -euo pipefail

PART="${1:-patch}"  # major, minor, or patch

# Find latest semver tag
LATEST=$(git tag --list 'v*.*.*' --sort=-version:refname | head -1)

if [ -z "$LATEST" ]; then
  echo "3.0.0"
  exit 0
fi

# Strip leading 'v'
VER="${LATEST#v}"

# Split on dots
IFS='.' read -r MAJ MIN PAT <<< "$VER"

case "$PART" in
  major) echo "$((MAJ + 1)).0.0" ;;
  minor) echo "$MAJ.$((MIN + 1)).0" ;;
  patch) echo "$MAJ.$MIN.$((PAT + 1))" ;;
  *)     echo "usage: $0 {major|minor|patch}" >&2; exit 1 ;;
esac
