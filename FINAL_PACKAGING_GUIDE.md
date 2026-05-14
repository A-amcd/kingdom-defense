# Kingdom Defense APK 本地打包完整指南

## 已准备好的工具

✅ **JDK 17**: `d:\12\jdk-17.0.2`
✅ **Android SDK**: `d:\12\android-sdk`
✅ **Android NDK 25b**: `d:\12\android-ndk-r25b`
✅ **Buildozer 配置**: `buildozer.spec`
✅ **游戏代码**: `tp.py` / `tp(9).py`

## 方法一：使用本地脚本（推荐）

### 步骤1: 确保在正确目录
打开PowerShell，运行：
```powershell
cd d:\12
```

### 步骤2: 运行本地打包脚本
在PowerShell中运行：
```powershell
powershell -ExecutionPolicy Bypass -File "d:\12\build_apk.ps1"
```
或者双击运行：`d:\12\build_apk_local.bat`

### 步骤3: 等待打包完成
首次构建需要 **30-60分钟**，请耐心等待。

---

## 方法二：使用GitHub Actions（最简单）

如果本地打包有问题，**强烈推荐使用GitHub Actions**，这个更稳定：

### 步骤1: 准备Git仓库
```powershell
cd d:\12
```

### 步骤2: 安装Git并创建仓库
访问: https://git-scm.com/download/win 下载Git并安装

### 步骤3: 上传到GitHub并等待自动构建
详细步骤见: `QUICK_START_GUIDE.md`

---

## 方法三：纯手动执行（调试用）

如果想手动执行每一步：

```powershell
cd d:\12

# 设置环境变量
$env:JAVA_HOME = "d:\12\jdk-17.0.2"
$env:ANDROID_HOME = "d:\12\android-sdk"
$env:ANDROID_NDK_HOME = "d:\12\android-ndk-r25b"
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:Path = "$env:JAVA_HOME\bin;$env:ANDROID_HOME\platform-tools;$env:ANDROID_HOME\cmdline-tools\latest\bin;$env:Path"

# 验证Java
& "$env:JAVA_HOME\bin\java.exe" -version

# 安装构建工具
py -m pip install buildozer==1.5.0 python-for-android==2024.03.16

# 开始打包
py -m buildozer android debug
```

---

## 预期结果

成功后，APK文件会在 `d:\12\bin\` 目录下。

APK文件大小约：30-100 MB

---

## 常见问题

### Q: 提示找不到文件？
A: 确保当前在 `d:\12` 目录

### Q: 提示权限错误？
A: 以管理员身份运行PowerShell

### Q: 网络下载失败？
A: 重试，或使用GitHub Actions方式

---

## 下一步

**推荐先用方法一**（`build_apk.ps1`），如果失败立刻切换到**方法二**（GitHub Actions）。
