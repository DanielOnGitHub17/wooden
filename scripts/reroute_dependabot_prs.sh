#!/bin/bash

# Reroute all open Dependabot PRs from main to updates
echo "Rerouting Dependabot PRs from main to updates..."
echo

# Get all open Dependabot PRs targeting main branch
pr_numbers=$(gh pr list --author "app/dependabot" --base main --state open --json number --jq ".[].number")

if [ -z "$pr_numbers" ]; then
    echo "No Dependabot PRs found targeting main branch"
    exit 0
fi

# Reroute each PR to updates branch
for pr in $pr_numbers; do
    echo "Rerouting PR #$pr..."
    if gh pr edit "$pr" --base updates; then
        echo "Successfully rerouted PR #$pr to updates"
    else
        echo "Failed to reroute PR #$pr"
    fi
    echo
done

echo "Done!"
