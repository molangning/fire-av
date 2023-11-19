#!/usr/bin/bash

# Script to update lists for github

git add -N .

if [ -z "$(git ls-files --modified sources/)" ]; then
    echo "[+] No files were changed"
else
    echo "[+] Files were changed! Pushing changed..."
    git remote set-url origin "https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/$GITHUB_REPOSITORY"
    git stage sources/
    git config --local user.email "example@github.com"
    git config --local user.name "GitHub Action"
    git commit -m "[Github Action] Automated lists update."
    git push
fi

