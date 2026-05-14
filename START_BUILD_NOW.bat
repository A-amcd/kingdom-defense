@echo off
chcp 65001 >nul
color 0A
title Kingdom Defense APK Build

echo.
echo ========================================
echo   Kingdom Defense APK 构建启动
echo ========================================
echo.

echo [步骤 1] 设置环境变量...
set JAVA_HOME=d:\12\jdk-17.0.2
set ANDROID_HOME=d:\12\android-sdk
set ANDROID_NDK_HOME=d:\12\android-ndk-r25b
set ANDROID_SDK_ROOT=d:\12\android-sdk
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\cmdline-tools\latest\bin;%PATH%
echo   ✓ 环境变量已设置
echo.

echo [步骤 2] 验证工具...
"%JAVA_HOME%\bin\java.exe" -version 2>&1
if %errorlevel% neq 0 (
    echo   ✗ Java验证失败！
    pause
    exit /b 1
)
echo   ✓ Java就绪
py -3.13 --version
if %errorlevel% neq 0 (
    echo   ✗ Python验证失败！
    pause
    exit /b 1
)
echo   ✓ Python就绪
echo.

echo [步骤 3] 安装依赖包...
py -3.13 -m pip install --upgrade pip wheel setuptools
py -3.13 -m pip install buildozer==1.5.0 python-for-android==2024.03.16 cython virtualenv colorama appdirs packaging sh jinja2 requests
echo   ✓ 依赖安装完成
echo.

echo ========================================
echo   现在开始构建 APK！
echo   这将需要 30-60 分钟
echo   请耐心等待...
echo ========================================
echo.

pause

echo.
echo [步骤 4] 执行 Buildozer 构建...
py -3.13 -m buildozer android debug
set EXIT_CODE=%errorlevel%

echo.
echo ========================================
if %EXIT_CODE% equ 0 (
    echo   ✓ 构建完成！检查 bin 目录
    if exist bin\*.apk (
        explorer bin
    )
) else (
    echo   ✗ 构建失败！错误代码: %EXIT_CODE%
)
echo ========================================
echo.

pause
