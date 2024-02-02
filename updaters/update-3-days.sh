#!/usr/bin/env bash

set -euxo pipefail

./scripts/get-ip-range-by-tags.py

./validate-lists.sh