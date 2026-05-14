@echo off
chcp 65001 >nul
color 0E
title Kingdom Defense APK Build - Robust Version

cd /d "%~dp0"

echo.
echo ========================================
echo   Kingdom Defense APK Build
echo   Robust Version - Handles Python 3.13
echo ========================================
echo.

:: Step 1: Environment setup
echo [1/6] Setting up environment variables...
set JAVA_HOME=d:\12\jdk-17.0.2
set ANDROID_HOME=d:\12\android-sdk
set ANDROID_NDK_HOME=d:\12\android-ndk-r25b
set ANDROID_SDK_ROOT=d:\12\android-sdk
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME\cmdline-tools\latest\bin;%PATH%

echo   JAVA_HOME: %JAVA_HOME%
echo   ANDROID_HOME: %ANDROID_HOME%
echo   ANDROID_NDK_HOME: %ANDROID_NDK_HOME%
echo.

:: Step 2: Verify Java
echo [2/6] Verifying Java...
"%JAVA_HOME%\bin\java.exe" -version 2>&1
if errorlevel 1 (
    echo   ERROR: Java not found!
    pause
    exit /b 1
)
echo   Java OK.
echo.

:: Step 3: Clean and upgrade pip
echo [3/6] Cleaning and upgrading pip...
py -3.13 -m pip uninstall -y buildozer python-for-android sh 2>nul
py -3.13 -m pip install --upgrade pip --no-cache-dir --no-warn-script-location
echo   pip upgraded.
echo.

:: Step 4: Install dependencies in stages
echo [4/6] Installing dependencies (this may take a while)...
echo.

:: Stage 4a: Core tools
echo   4a. Installing core tools...
py -3.13 -m pip install wheel setuptools --no-cache-dir --no-warn-script-location

:: Stage 4b: Cython (critical!)
echo   4b. Installing Cython (may take several minutes)...
py -3.13 -m pip install "cython>=3.0,<4.0" --no-cache-dir --no-warn-script-location
if errorlevel 1 (
    echo   Retrying Cython installation...
    timeout /t 5
    py -3.13 -m pip install "cython>=3.0" --force-reinstall --no-cache-dir --no-warn-script-location
)

:: Stage 4c: Other dependencies
echo   4c. Installing other dependencies...
py -3.13 -m pip install colorama appdirs jinja2 toml pexpect requests --no-cache-dir --no-warn-script-location

:: Stage 4d: buildozer
echo   4d. Installing buildozer...
py -3.13 -m pip install buildozer==1.4.0 --no-cache-dir --no-warn-script-location

:: Stage 4e: python-for-android
echo   4e. Installing python-for-android...
py -3.13 -m pip install python-for-android==2023.5.21 --no-cache-dir --no-warn-script-location

echo   Dependencies installed.
echo.

:: Step 5: Verify
echo [5/6] Verifying buildozer...
py -3.13 -m buildozer --version
if errorlevel 1 (
    echo.
    echo   ERROR: buildozer not working!
    echo   Trying to diagnose...
    py -3.13 -m pip list | findstr /i buildozer
    pause
    exit /b 1
)
echo   buildozer verified.
echo.

:: Step 6: Build!
echo [6/6] Starting APK build...
echo ========================================
echo   IMPORTANT: This takes 30-60 minutes!
echo   Please wait and do not close this window.
echo ========================================
echo.

py -3.13 -m buildozer android debug
set BUILD_EXIT=%errorlevel%

:: Results
echo.
echo ========================================
if %BUILD_EXIT% equ 0 (
    echo   BUILD SUCCESSFUL!
    echo ========================================
    if exist bin\*.apk (
        echo.
        echo APK files generated:
        dir bin\*.apk
        echo.
        echo Opening bin folder...
        explorer bin
    ) else (
        echo No APK found in bin folder.
    )
) else (
    echo   BUILD FAILED!
    echo ========================================
    echo.
    echo Error code: %BUILD_EXIT%
    echo.
    echo Common issues:
    echo 1. Network timeout - try again
    echo 2. Missing dependencies - run this script again
    echo 3. Python compatibility - Python 3.11-3.12 recommended
)

echo.
echo ========================================
echo Press any key to exit...
pause >nul
