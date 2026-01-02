#!/bin/bash
chmod +x ./merge_dependabot_prs.sh

# Merge all open Dependabot PRs
gh pr list --author "app/dependabot" --state open --json number --jq ".[].number" | \
  xargs -I {} gh pr merge {} --merge --delete-branch
