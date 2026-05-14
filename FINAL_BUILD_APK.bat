@echo off
chcp 65001 >nul
title Kingdom Defense APK Final Build
color 0A

cd /d "%~dp0"

echo.
echo ########################################################################
echo #                       Kingdom Defense APK Build                      #
echo ########################################################################
echo.

echo [1/6] Cleaning up previous build...
if exist ".buildozer" rmdir /s /q ".buildozer"
if exist "bin" rmdir /s /q "bin"
echo   Done.
echo.

echo [2/6] Setting environment variables...
set JAVA_HOME=d:\12\jdk-17.0.2
set ANDROID_HOME=d:\12\android-sdk
set ANDROID_NDK_HOME=d:\12\android-ndk-r25b
set ANDROID_SDK_ROOT=d:\12\android-sdk
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\cmdline-tools\latest\bin;%PATH%

echo   JAVA_HOME: %JAVA_HOME%
echo   ANDROID_HOME: %ANDROID_HOME%
echo   ANDROID_NDK_HOME: %ANDROID_NDK_HOME%
echo   Done.
echo.

echo [3/6] Verifying tools...
"%JAVA_HOME%\bin\java.exe" -version 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Java verification failed!
    pause
    exit /b 1
)
echo   Java verified.
echo.

echo [4/6] Installing build dependencies...
py -3.13 -m pip install --upgrade pip wheel setuptools
py -3.13 -m pip install buildozer==1.5.0 python-for-android==2024.03.16 cython virtualenv colorama appdirs packaging sh jinja2 requests
py -3.13 -m pip install kivy 2>&1 || echo Warning: Kivy installation may have issues
echo   Done.
echo.

echo [5/6] Starting APK Build Process...
echo ########################################################################
echo.
echo   ATTENTION!
echo   THIS PROCESS CAN TAKE 30-60 MINUTES!
echo   Please be patient. First build will download many components.
echo.
echo ########################################################################
echo.
timeout /t 10

echo Starting buildozer android debug...
echo.

py -3.13 -m buildozer android debug 2>&1

set BUILD_EXIT=%errorlevel%

echo.
echo [6/6] Checking results...
echo.

if %BUILD_EXIT% equ 0 (
    if exist "bin\*.apk" (
        echo ########################################################################
        echo #                          BUILD SUCCESSFUL!                           #
        echo ########################################################################
        echo.
        echo APK files generated:
        dir bin\*.apk /b
        echo.
        echo APK are located in: %cd%\bin\
        echo.
        explorer bin\
    ) else (
        echo Buildozer reported success, but APK not found.
    )
) else (
    echo ########################################################################
    echo #                          BUILD FAILED!                               #
    echo ########################################################################
    echo.
    echo Please check the error messages above.
    echo.
    echo If this keeps failing, try the GitHub Actions method!
    echo See FINAL_PACKAGING_GUIDE.md for details.
    echo.
)

echo.
echo Press any key to exit...
pause >nul
