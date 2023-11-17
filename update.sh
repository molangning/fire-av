#!/usr/bin/env bash
# https://stackoverflow.com/questions/3822621/how-to-exit-if-a-command-failed

set -e 
set -o pipefail

./scripts/get-aws-ranges.py
./scripts/curi0usjack-htaccess-downloader.py