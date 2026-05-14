@echo off
chcp 65001 >nul
echo ========================================
echo   Kingdom Defense APK打包助手
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 建议使用管理员权限运行以避免权限问题
    echo.
)

:: 步骤1: 安装Git
echo [1/5] 检查/安装 Git...
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo   正在安装Git，请稍候...
    winget install --id Git.Git -e --accept-source-agreements --accept-package-agreements --silent
    if %errorlevel% neq 0 (
        echo   [错误] Git安装失败，请手动下载: https://git-scm.com/download/win
        echo   安装完成后，请重新运行此脚本
        pause
        exit /b 1
    )
)
echo   ✓ Git已安装
echo.

:: 步骤2: 安装GitHub CLI
echo [2/5] 检查/安装 GitHub CLI...
where gh >nul 2>&1
if %errorlevel% neq 0 (
    echo   正在安装GitHub CLI，请稍候...
    winget install GitHub.cli -e --accept-source-agreements --accept-package-agreements --silent
    if %errorlevel% neq 0 (
        echo   [错误] GitHub CLI安装失败
        echo   请手动下载: https://cli.github.com/
        pause
        exit /b 1
    )
)
echo   ✓ GitHub CLI已安装
echo.

:: 步骤3: 配置Git
echo [3/5] 配置Git...
echo   请输入你的GitHub用户名:
set /p GH_USER=
echo   请输入你的GitHub邮箱:
set /p GH_EMAIL=

git config --global user.name "%GH_USER%"
git config --global user.email "%GH_EMAIL%"
echo   ✓ Git配置完成
echo.

:: 步骤4: GitHub认证
echo [4/5] GitHub认证...
echo   请在浏览器中完成GitHub授权
gh auth login
if %errorlevel% neq 0 (
    echo   [错误] GitHub认证失败
    pause
    exit /b 1
)
echo   ✓ GitHub认证成功
echo.

:: 步骤5: 创建仓库并推送
echo [5/5] 创建GitHub仓库并推送代码...
echo   仓库名称 (kingdom-defense):
set /p REPO_NAME=
if "%REPO_NAME%"=="" set REPO_NAME=kingdom-defense

:: 创建仓库
gh repo create %REPO_NAME% --public --clone=false
if %errorlevel% neq 0 (
    echo   [错误] 创建仓库失败
    pause
    exit /b 1
)

:: 初始化Git仓库
git init
git add .
git commit -m "Kingdom Defense - Initial commit"

:: 添加远程仓库
git remote add origin https://github.com/%GH_USER%/%REPO_NAME%.git
git branch -M main

:: 推送代码
git push -u origin main
if %errorlevel% neq 0 (
    echo   [错误] 推送代码失败
    echo   请检查网络连接并重试
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 所有步骤完成！
echo ========================================
echo.
echo   接下来请:
echo   1. 打开 https://github.com/%GH_USER%/%REPO_NAME%
echo   2. 点击 Actions 标签查看构建进度
echo   3. 构建完成后下载APK文件
echo.
echo   构建可能需要15-20分钟，请耐心等待...
echo.
pause
