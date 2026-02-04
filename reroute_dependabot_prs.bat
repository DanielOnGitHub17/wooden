@echo off

REM Reroute all open Dependabot PRs from main to updates
echo Rerouting Dependabot PRs from main to updates...
echo.

for /f "tokens=1" %%i in ('gh pr list --author "app/dependabot" --base main --state open --json number --jq ".[].number"') do (
    echo Rerouting PR #%%i...
    gh pr edit %%i --base updates
    if errorlevel 1 (
        echo Failed to reroute PR #%%i
    ) else (
        echo Successfully rerouted PR #%%i to updates
    )
    echo.
)

echo Done!
