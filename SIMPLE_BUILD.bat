@echo off
chcp 65001 >nul
title Kingdom Defense APK Build
cd /d "%~dp0"

echo.
echo ========================================
echo   Kingdom Defense APK Build
echo ========================================
echo.

echo [1/5] Setting up environment...
set JAVA_HOME=d:\12\jdk-17.0.2
set ANDROID_HOME=d:\12\android-sdk
set ANDROID_NDK_HOME=d:\12\android-ndk-r25b
set ANDROID_SDK_ROOT=d:\12\android-sdk
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\cmdline-tools\latest\bin;%PATH%
echo   Done.
echo.

echo [2/5] Verifying tools...
"%JAVA_HOME%\bin\java.exe" -version
if errorlevel 1 (
    echo   ERROR: Java not found!
    pause
    exit /b 1
)
echo   Java OK.
py -3.13 --version
if errorlevel 1 (
    echo   ERROR: Python not found!
    pause
    exit /b 1
)
echo   Python OK.
echo.

echo [3/5] Installing dependencies...
py -3.13 -m pip install --upgrade pip wheel setuptools
py -3.13 -m pip install cython>=3.0 virtualenv colorama appdirs packaging sh jinja2 requests
py -3.13 -m pip install buildozer==1.4.0 python-for-android==2023.5.21
echo   Done.
echo.

echo [4/5] Starting APK build...
echo ========================================
echo   THIS MAY TAKE 30-60 MINUTES!
echo   Be patient, first build downloads a lot.
echo ========================================
echo.

py -3.13 -m buildozer android debug
set BUILD_EXIT=%errorlevel%

echo.
echo [5/5] Checking results...
echo.

if %BUILD_EXIT% equ 0 (
    if exist bin\*.apk (
        echo ========================================
        echo   BUILD SUCCESSFUL!
        echo ========================================
        echo.
        echo APK files in bin folder:
        dir bin\*.apk /b
        echo.
        explorer bin
    ) else (
        echo Build done, but no APK found. Check buildozer logs.
    )
) else (
    echo ========================================
    echo   BUILD FAILED! Error code: %BUILD_EXIT%
    echo ========================================
    echo.
    echo See error messages above.
    echo If it keeps failing, try GitHub Actions method.
    echo See FINAL_PACKAGING_GUIDE.md
    echo.
)

echo.
echo Press any key to exit...
pause >nul
