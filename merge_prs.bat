@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Merge All Open Pull Requests
echo ========================================
echo.

REM Check if GitHub CLI is installed
gh --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: GitHub CLI is not installed!
    echo Please install it from: https://cli.github.com/
    pause
    exit /b 1
)

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not in a git repository!
    pause
    exit /b 1
)

echo Fetching all open pull requests...
echo.

REM Get all open PR numbers
for /f "tokens=1" %%i in ('gh pr list --state open --json number --jq ".[].number"') do (
    set PR_NUMBER=%%i
    echo.
    echo ----------------------------------------
    echo Processing PR #!PR_NUMBER!
    echo ----------------------------------------
    
    REM Show PR details
    gh pr view !PR_NUMBER! --json title,author --jq ".title + \" by \" + .author.login"
    
    REM Ask for confirmation
    set /p CONFIRM="Merge this PR? (y/N): "
    
    if /i "!CONFIRM!"=="y" (
        echo Merging PR #!PR_NUMBER!...
        gh pr merge !PR_NUMBER! --merge --delete-branch
        
        if errorlevel 1 (
            echo ERROR: Failed to merge PR #!PR_NUMBER!
        ) else (
            echo SUCCESS: Merged PR #!PR_NUMBER!
        )
    ) else (
        echo Skipping PR #!PR_NUMBER!
    )
)

echo.
echo ========================================
echo  All PRs processed!
echo ========================================
pause