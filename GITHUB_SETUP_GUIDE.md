# GitHub Actions APK构建指南

## 准备工作

### 1. 安装 Git for Windows

1. 访问 https://git-scm.com/download/win 下载 Git
2. 运行安装程序，默认选项即可
3. 安装完成后，在命令提示符或PowerShell中验证：
   ```bash
   git --version
   ```

### 2. 创建 GitHub 账户

如果还没有GitHub账户，请访问 https://github.com 注册

### 3. 创建远程仓库

#### 方法一：使用网页界面（推荐）

1. 登录 GitHub
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `kingdom-defense`
   - Description: `王国防线 - 一款塔防游戏`
   - 选择 "Public"（公开仓库，Actions免费使用）
   - 不要勾选 "Initialize this repository with a README"
4. 点击 "Create repository"

#### 方法二：使用命令行

```bash
# 初始化本地仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 添加远程仓库（将 YOUR_USERNAME 替换为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/kingdom-defense.git

# 推送代码
git branch -M main
git push -u origin main
```

## 触发 APK 构建

1. 推送代码后，进入你的GitHub仓库
2. 点击 "Actions" 标签页
3. 你应该能看到 "Build Android APK" 工作流正在运行或已完成
4. 点击工作流运行记录
5. 在 "Artifacts" 部分下载 APK 文件

## 下载生成的 APK

1. 在 Actions 页面点击具体的工作流运行
2. 页面底部有 "Artifacts" 部分
3. 点击 "kingdom-defense-apk" 下载APK文件
4. 将APK文件传输到Android设备安装

## 构建状态说明

- ✅ 绿色勾：构建成功，APK已生成
- ❌ 红色叉：构建失败，需要检查错误日志
- ⏳ 转圈：构建中，需要等待

## 常见问题

### Q: 构建失败怎么办？
A: 点击失败的workflow，查看详细的错误日志，根据错误信息修复代码后重新推送

### Q: APK文件太大？
A: 这是正常现象，因为包含了完整的Python解释器和pygame库

### Q: 如何构建Release版本？
A: 修改 buildozer.spec 中的 `android.build_type = release`，但需要签名配置

## 后续更新

每次推送代码到 main 分支，GitHub Actions 都会自动重新构建 APK。

---

如有问题，请在GitHub仓库中创建Issue。
