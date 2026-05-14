@echo off
chcp 65001 >nul
title Kingdom Defense APK Build
cd /d "%~dp0"

echo.
echo ========================================
echo   Kingdom Defense APK Build
echo   Step 1: Clean old installations
echo ========================================
echo.

py -3.13 -m pip uninstall -y buildozer python-for-android sh 2>nul

echo.
echo ========================================
echo   Step 2: Install dependencies one by one
echo ========================================
echo.

echo Installing basic tools...
py -3.13 -m pip install --upgrade pip wheel setuptools
if errorlevel 1 (
    echo   WARNING: pip upgrade had issues, continuing...
)

echo.
echo Installing Cython (important for compilation)...
py -3.13 -m pip install "cython>=3.0,<4.0" --no-cache-dir
if errorlevel 1 (
    echo   WARNING: Cython installation failed, trying alternate...
    py -3.13 -m pip install cython --only-binary :all: --no-cache-dir
)

echo.
echo Installing other dependencies...
py -3.13 -m pip install colorama appdirs jinja2 toml pexpect requests
if errorlevel 1 (
    echo   WARNING: Some dependencies failed, continuing...
)

echo.
echo ========================================
echo   Step 3: Install buildozer and p4a
echo ========================================
echo.

echo Installing buildozer...
py -3.13 -m pip install buildozer==1.4.0 --no-cache-dir
if errorlevel 1 (
    echo   ERROR: buildozer installation failed!
    pause
    exit /b 1
)

echo.
echo Installing python-for-android...
py -3.13 -m pip install python-for-android==2023.5.21 --no-cache-dir
if errorlevel 1 (
    echo   WARNING: python-for-android installation failed, continuing...
)

echo.
echo ========================================
echo   Step 4: Verify installation
echo ========================================
echo.

echo Checking buildozer...
py -3.13 -m buildozer --version
if errorlevel 1 (
    echo   ERROR: buildozer not working!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Step 5: Starting APK build
echo ========================================
echo.
echo   THIS MAY TAKE 30-60 MINUTES!
echo   Be patient...
echo ========================================
echo.

py -3.13 -m buildozer android debug
set BUILD_EXIT=%errorlevel%

echo.
echo ========================================
if %BUILD_EXIT% equ 0 (
    echo   BUILD SUCCESSFUL!
    if exist bin\*.apk (
        echo APK files in bin folder:
        dir bin\*.apk /b
        explorer bin
    )
) else (
    echo   BUILD FAILED! Error code: %BUILD_EXIT%
)
echo ========================================
echo.
pause
