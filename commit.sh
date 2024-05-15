#!/usr/bin/bash

# DO NOT USE THIS SCRIPT WITH USER INPUT!!!
# COMMAND INJECTION IS POSSIBLE

set -euxo pipefail

if [ -z "$(git ls-files --modified $2)" ]; then
    echo "[+] No files were changed"
else
    echo "[+] Files were changed! Pushing changed..."
    git pull
    git stage $2
    git remote set-url origin https://x-access-token:$1@github.com/$GITHUB_REPOSITORY
    git config --local user.email "41898282+github-actions[bot]@users.noreply.github.com"
    git config --local user.name "GitHub Actions"
    git commit -m "[Github Action] Automated lists update."
    git push
fi
