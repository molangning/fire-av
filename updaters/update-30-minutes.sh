#!/usr/bin/env bash

set -e 
set -o pipefail

./scripts/get-tor-exit-list.py
./scripts/get-ip-range-from-isc.py
./scripts/get-ip-range-from-asn.py

./validate-lists.sh