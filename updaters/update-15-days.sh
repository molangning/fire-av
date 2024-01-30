#!/usr/bin/env bash

set -e 
set -o pipefail

./scripts/get-ip-range-by-tags.py

./validate-lists.sh