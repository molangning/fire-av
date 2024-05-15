#!/usr/bin/env bash

set -euxo pipefail
export PYTHONUNBUFFERED=1

./scripts/get-ip-range-by-tags.py

./validate-lists.sh
