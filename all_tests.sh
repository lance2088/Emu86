#!/bin/sh
#  This file should include all tests run on our assembly emulator.

# exit on any error with that error status:
set -e

export TDIR="tests"

for test_file in $TDIR/*/test_*.py; do echo "$test_file"; python3 "$test_file"; done