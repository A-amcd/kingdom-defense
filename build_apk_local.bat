@echo off
chcp 65001 >nul
title Kingdom Defense APK 打包工具

echo ========================================
echo   Kingdom Defense APK 打包助手
echo ========================================
echo.

cd /d "%~dp0"

:: 设置环境变量
echo [1/5] 设置环境变量...
set JAVA_HOME=d:\12\jdk-17.0.2
set ANDROID_HOME=d:\12\android-sdk
set ANDROID_NDK_HOME=d:\12\android-ndk-r25b
set PATH=%JAVA_HOME%\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\cmdline-tools\latest\bin;%PATH%

echo   ✓ JAVA_HOME: %JAVA_HOME%
echo   ✓ ANDROID_HOME: %ANDROID_HOME%
echo   ✓ ANDROID_NDK_HOME: %ANDROID_NDK_HOME%
echo.

:: 验证Java
echo [2/5] 验证Java...
"%JAVA_HOME%\bin\java.exe" -version 2>&1
if %errorlevel% neq 0 (
    echo   [错误] Java未正确配置！
    pause
    exit /b 1
)
echo   ✓ Java就绪
echo.

:: 安装依赖
echo [3/5] 安装构建依赖...
py -3.13 -m pip install --upgrade pip
py -3.13 -m pip install buildozer==1.5.0 python-for-android==2024.03.16 cython virtualenv
if %errorlevel% neq 0 (
    echo   [警告] 依赖安装可能有问题，继续尝试...
)
echo   ✓ 依赖安装完成
echo.

:: 开始打包
echo [4/5] 开始Android APK打包...
echo   这个过程可能需要30-60分钟
echo   请耐心等待，首次构建需要下载很多组件
echo.
timeout /t 5

:: 运行buildozer
py -3.13 -m buildozer android debug
if %errorlevel% neq 0 (
    echo.
    echo [错误] 打包失败！
    echo   请检查上面的错误信息
    pause
    exit /b 1
)

echo.
echo [5/5] 打包完成！
echo.

:: 检查生成的APK
if exist "bin\*.apk" (
    echo ========================================
    echo   ✅ APK构建成功！
    echo ========================================
    echo.
    echo APK文件:
    dir bin\*.apk
    echo.
    echo APK位置: %cd%\bin\
    echo.
    explorer bin\
) else (
    echo [警告] 未找到APK文件，可能构建失败
)

echo.
echo 按任意键退出...
pause
