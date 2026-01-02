@echo off

REM Merge all open Dependabot PRs
for /f "tokens=1" %%i in ('gh pr list --author "app/dependabot" --state open --json number --jq ".[].number"') do (
    gh pr merge %%i --merge --delete-branch
)