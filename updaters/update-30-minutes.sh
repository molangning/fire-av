#!/usr/bin/env bash

./scripts/get-tor-exit-list.py
./scripts/get-ip-range-from-isc.py
./scripts/get-ip-range-from-asn.py

set -euxo pipefail

./validate-lists.sh
