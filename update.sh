#!/usr/bin/env bash
# https://stackoverflow.com/questions/3822621/how-to-exit-if-a-command-failed

set -e 
set -o pipefail

./scripts/get-aws-ranges.py
./scripts/get-azure-ranges.py
./scripts/get-tor-exit-list.py
./scripts/get-ip-range-from-asn.py
# Optional, enable if you need it
# ./scripts/curi0usjack-htaccess-downloader.py