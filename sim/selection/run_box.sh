#!/bin/sh
# SIM-SPEC-03: all W1 runs, in this order. Checks first.
set -e
cd "$(dirname "$0")"
python3 box2d.py equiv
python3 box2d.py step
python3 box2d.py main 64
python3 box2d.py main 4 9 16 25 36 49
python3 analyse_box.py
