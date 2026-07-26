#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 hooks/test-mutation_matrix.py "$@"
