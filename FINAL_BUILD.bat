@echo off
chcp 65001 >nul
title Kingdom Defense APK Build

cd /d "%~dp0"

echo.
echo ========================================
echo   Kingdom Defense APK Build
echo ========================================
echo.

:: Find Python
echo [Step 1] Finding Python...
for /f "tokens=*" %%i in ('py -0') do (
    for /f "tokens=2" %%p in ("%%i") do set PYTHON_CMD=%%p
)
if not defined PYTHON_CMD set PYTHON_CMD=py

echo Using Python: %PYTHON_CMD%
echo.

:: Setup environment
echo [Step 2] Setting up environment...
set JAVA_HOME=d:\12\jdk-17.0.2
set ANDROID_HOME=d:\12\android-sdk
set ANDROID_NDK_HOME=d:\12\android-ndk-r25b
set ANDROID_SDK_ROOT=d:\12\android-sdk
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%PATH%
echo.

:: Verify Java
echo [Step 3] Verifying Java...
"%JAVA_HOME%\bin\java.exe" -version
echo.

:: Install dependencies step by step
echo [Step 4] Installing dependencies...
echo.

echo Installing pip upgrade...
%PYTHON_CMD% -m pip install --upgrade pip
echo.

echo Installing build tools...
%PYTHON_CMD% -m pip install wheel setuptools
echo.

echo Installing Cython...
%PYTHON_CMD% -m pip install "cython>=3.0,<4.0"
echo.

echo Installing other dependencies...
%PYTHON_CMD% -m pip install colorama appdirs jinja2 toml pexpect requests
echo.

echo Installing buildozer...
%PYTHON_CMD% -m pip install buildozer==1.4.0
echo.

echo Installing python-for-android...
%PYTHON_CMD% -m pip install python-for-android==2023.5.21
echo.

:: Build!
echo ========================================
echo [Step 5] Starting APK build!
echo This takes 30-60 minutes. Please wait.
echo ========================================
echo.

%PYTHON_CMD% -m buildozer android debug
set BUILD_EXIT=%errorlevel%

:: Results
echo.
if %BUILD_EXIT% equ 0 (
    echo ========================================
    echo   BUILD SUCCESSFUL!
    echo ========================================
    if exist bin\*.apk (
        dir bin\*.apk
        explorer bin
    )
) else (
    echo ========================================
    echo   BUILD FAILED! Error: %BUILD_EXIT%
    echo ========================================
)

echo.
pause
