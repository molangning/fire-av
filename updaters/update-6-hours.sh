#!/usr/bin/env bash

set -euxo pipefail
export PYTHONUNBUFFERED=1

./scripts/get-aws-ranges.py
./scripts/get-azure-ranges.py
./scripts/get-google-cloud-ranges.py
./scripts/get-cloudflare-ip-ranges.py

./validate-lists.sh
