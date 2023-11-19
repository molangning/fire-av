#!/usr/bin/bash

# Script to update lists for github

git add -N .

if [ -z "$(git ls-files --modified sources/)" ]; then
    echo "[+] No files were changed"
else
    echo "[+] Files were changed! Pushing changed..."
    git stage sources/
    git config --local user.email "example@github.com"
    git config --local user.name "GitHub Action"
    git commit -m "Automated data update"
    git push
fi

