@echo off
chcp 65001 >nul
color 0E
title Python Environment Diagnostic

echo.
echo ========================================
echo   Python 环境诊断工具
echo ========================================
echo.

echo [测试 1] 查找Python可执行文件...
echo.

:: 方法1: py launcher
echo 1. 测试 py launcher...
py -0 2>&1
echo   退出码: %errorlevel%
echo.

:: 方法2: 检查常见Python安装位置
echo 2. 检查Python安装目录...
if exist "C:\Python312\python.exe" (
    echo   ✓ 找到 C:\Python312\python.exe
    C:\Python312\python.exe -V
)
if exist "C:\Python311\python.exe" (
    echo   ✓ 找到 C:\Python311\python.exe
    C:\Python311\python.exe -V
)
if exist "C:\Python310\python.exe" (
    echo   ✓ 找到 C:\Python310\python.exe
    C:\Python310\python.exe -V
)
if exist "C:\Program Files\Python*\python.exe" (
    echo   ✓ 在Program Files找到Python
    dir "C:\Program Files\Python*\python.exe" /b /s 2>nul
)
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\*\*\python.exe" (
    echo   ✓ 在用户目录找到Python
    dir "C:\Users\%USERNAME%\AppData\Local\Programs\Python\*\*\python.exe" /b /s 2>nul
)
echo.

:: 方法3: 使用where命令
echo 3. 使用where命令查找Python...
where python 2>&1
where py 2>&1
echo.

echo ========================================
echo   诊断完成
echo ========================================
echo.
echo 如果以上都没有找到Python，请：
echo.
echo 1. 下载并安装Python: https://www.python.org/downloads/
echo 2. 安装时勾选 "Add Python to PATH"
echo 3. 安装完成后，重新打开命令提示符
echo 4. 运行此脚本再次测试
echo.

pause
