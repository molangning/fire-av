#!/usr/bin/env bash

set -euxo pipefail
export PYTHONUNBUFFERED=1

./scripts/update-asn-list.py
./scripts/get-tor-exit-list.py
./scripts/get-ip-range-from-isc.py
./scripts/get-ip-range-from-asn.py
./scripts/get-lists-from-blocklist-de.py
./scripts/get-ip-range-by-tags.py

./validate-lists.sh
