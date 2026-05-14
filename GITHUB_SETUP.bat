@echo off
chcp 65001 >nul
color 0A
title Kingdom Defense - GitHub Actions Setup

echo.
echo ========================================
echo   GitHub Actions APK Build Setup
echo ========================================
echo.

:: Step 1: Check if Git is installed
echo [Step 1] Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   Git not found! Installing Git...
    winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements --silent
    echo   Git installed! Please restart your computer and run this script again.
    pause
    exit /b 0
)
echo   Git is installed.
echo.

:: Step 2: Check if GitHub CLI is installed
echo [Step 2] Checking GitHub CLI...
gh --version >nul 2>&1
if %errorlevel% neq 0 (
    echo   GitHub CLI not found! Installing...
    winget install GitHub.cli -e --accept-source-agreements --accept-package-agreements --silent
    echo   GitHub CLI installed!
)
echo.

:: Step 3: GitHub Authentication
echo [Step 3] GitHub Authentication
echo   Please login to GitHub in your browser...
gh auth login
if %errorlevel% neq 0 (
    echo   Authentication failed! Please run 'gh auth login' manually.
    pause
    exit /b 1
)
echo   GitHub authenticated successfully!
echo.

:: Step 4: Initialize Git repository
echo [Step 4] Initializing Git repository...
cd /d "%~dp0"

:: Check if already a git repo
if exist ".git" (
    echo   Already a Git repository!
) else (
    echo   Initializing new repository...
    git init
    git add .
    git commit -m "Kingdom Defense - Initial commit"
)
echo.

:: Step 5: Create GitHub repository
echo [Step 5] Creating GitHub repository...
set /p REPO_NAME="Enter repository name (default: kingdom-defense): "
if "%REPO_NAME%"=="" set REPO_NAME=kingdom-defense

gh repo create %REPO_NAME% --public --source=. --remote=origin
if %errorlevel% neq 0 (
    echo   Repository may already exist or creation failed.
    echo   Trying to push to existing repository...
)
echo.

:: Step 6: Push to GitHub
echo [Step 6] Pushing to GitHub...
git branch -M main
git push -u origin main
if %errorlevel% neq 0 (
    echo   Push failed!
    pause
    exit /b 1
)
echo.

:: Step 7: Trigger Actions
echo [Step 7] Checking GitHub Actions...
echo.
echo ========================================
echo   CODE PUSHED SUCCESSFULLY!
echo ========================================
echo.
echo Next steps:
echo 1. Open: https://github.com/YOUR_USERNAME/%REPO_NAME%
echo 2. Click "Actions" tab
echo 3. Wait for "Build Android APK" workflow to complete
echo 4. Download APK from Artifacts
echo.
echo Build takes approximately 15-20 minutes.
echo.
echo Opening GitHub repository in browser...
start https://github.com/%REPO_NAME%
echo.
pause
