#!/usr/bin/env bash
# https://stackoverflow.com/questions/3822621/how-to-exit-if-a-command-failed

set -e 
set -o pipefail

./scripts/ipv4-checker.py
./scripts/new-line-checker.py