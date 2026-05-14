# APK打包完整指南

## 快速开始

### 方法一：一键脚本（推荐）

**步骤1：安装必要工具**

1. **安装Git** 
   - 访问 https://git-scm.com/download/win
   - 下载并安装，默认选项即可
   - 安装完成后**重启电脑**让PATH生效

2. **安装GitHub CLI**
   - 访问 https://cli.github.com/
   - 下载并安装
   - 或在PowerShell中运行：`winget install GitHub.cli`

**步骤2：运行打包脚本**

1. 打开文件资源管理器，进入 `D:\12`
2. 双击运行 `build_apk.bat`
3. 或者打开PowerShell，运行：
   ```powershell
   cd d:\12
   python build_apk.py
   ```

**步骤3：按提示操作**

脚本会引导你完成：
- 输入GitHub用户名和邮箱
- 完成GitHub授权
- 自动创建仓库并推送代码

---

### 方法二：手动操作（更稳定）

#### 第一步：安装GitHub Desktop（最简单）

1. 访问 https://desktop.github.com/ 下载GitHub Desktop
2. 安装并登录你的GitHub账户
3. 点击 "File" → "Add Local Repository"
4. 选择 `D:\12` 文件夹
5. 点击 "Publish repository"
6. 填写仓库名称：`kingdom-defense`
7. 选择 "Public"
8. 点击 "Publish"

#### 第二步：触发构建

推送代码后，GitHub会自动开始构建APK：
1. 打开 https://github.com/你的用户名/kingdom-defense
2. 点击 "Actions" 标签
3. 等待构建完成（绿色勾表示成功）
4. 点击构建记录，下载APK

---

## 使用GitHub Actions构建（无需手动操作）

### 构建流程

```
代码推送 → GitHub接收 → 自动构建 → APK生成 → 下载使用
    ↓           ↓           ↓          ↓         ↓
  1分钟      30秒       15-20分钟    5分钟     即刻
```

### 查看构建状态

1. **打开仓库**：访问 `https://github.com/你的用户名/kingdom-defense`

2. **进入Actions页面**：点击绿色的 "Actions" 标签

3. **查看工作流**：
   - 应该看到 "Build Android APK" 工作流
   - 点击左侧的工作流名称查看详情

4. **构建状态**：
   - ⏳ 黄色圆圈 = 构建中（请等待）
   - ✅ 绿色勾 = 成功（可以下载APK）
   - ❌ 红色叉 = 失败（需要查看日志修复）

### 下载APK

构建成功后：

1. 点击构建任务的名称（如 "#1 Build Android APK"）

2. 向下滚动到 "Artifacts" 部分

3. 点击 "kingdom-defense-apk" 下载APK

4. APK文件会自动下载为ZIP，解压后得到APK文件

### 安装APK

1. 将APK文件传到Android手机
2. 在手机上打开文件管理器
3. 找到APK文件，点击安装
4. 如果提示"禁止安装未知来源应用"：
   - 进入 设置 → 安全 → 允许未知来源
   - 或在安装时勾选"允许"
5. 安装完成，打开游戏！

---

## 常见问题

### Q1: 构建失败怎么办？
**A**: 
- 点击失败的构建记录
- 查看 "Run buildozer android debug" 步骤的错误日志
- 根据错误信息修复代码
- 重新推送代码触发构建

### Q2: APK文件在哪里？
**A**: 
- GitHub Actions页面 → 具体构建记录 → Artifacts
- 下载的ZIP文件，解压后就是APK

### Q3: APK有多大？
**A**: 
- 通常30-100MB
- 因为包含了完整的Python解释器和pygame库
- 这是正常的，所有Python转Android应用都这样

### Q4: 如何更新游戏？
**A**: 
- 修改代码后推送到GitHub
- GitHub会自动重新构建
- 下载新的APK安装即可

### Q5: 可以在手机上直接调试吗？
**A**: 
- 可以，但需要配置Android设备的开发者选项
- 在手机设置中启用USB调试
- 用USB连接电脑后运行：`adb install app.apk`

### Q6: 构建需要多长时间？
**A**: 
- 首次构建：15-20分钟（需要下载所有SDK）
- 后续构建：5-10分钟（使用缓存）

---

## 脚本说明

### build_apk.bat
Windows批处理脚本，简单自动化

### build_apk.py
Python脚本，功能更完整，推荐使用

### 如果你更喜欢手动操作

可以按照这个流程：

1. 创建GitHub仓库
2. 安装Git
3. 初始化本地仓库
4. 添加所有文件
5. 提交
6. 推送到GitHub
7. 等待构建完成

---

## 技术细节

### 项目使用的工具

- **Buildozer**: Python打包工具
- **python-for-android**: Android构建工具
- **pygame**: 游戏引擎
- **GitHub Actions**: 自动化构建

### 构建配置

- Android SDK: API 33
- Android NDK: 25b
- 最小支持: Android 5.0 (API 21)
- 构建类型: Debug

---

## 获取帮助

如果遇到问题：

1. 查看 [GitHub Actions日志](https://docs.github.com/cn/actions) 
2. 查看 [Buildozer文档](https://buildozer.readthedocs.io/)
3. 在GitHub仓库创建Issue

---

**祝你游戏愉快！** 🎮
