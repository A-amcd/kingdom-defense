import os

print("=== APK 打包配置验证 ===\n")

# 检查必要文件
files = {
    'tp(9).py': '游戏主文件',
    'main.py': '入口脚本',
    'buildozer.spec': 'Buildozer 配置',
    'setup.py': 'Python 包配置',
    'icon.png': '应用图标',
    '.github/workflows/build-apk.yml': 'GitHub Actions 工作流'
}

print("📁 文件检查:")
all_exists = True
for filepath, desc in files.items():
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"  {status} {filepath} ({desc})")
    if not exists:
        all_exists = False

# 检查工作流配置
print("\n🔧 工作流配置检查:")
try:
    with open('.github/workflows/build-apk.yml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('name:', '名称字段'),
        ('on:', '触发条件'),
        ('jobs:', '任务定义'),
        ('workflow_dispatch', '手动触发'),
        ('buildozer android debug', '构建命令')
    ]
    
    for check, desc in checks:
        if check in content:
            print(f"  ✅ 包含 {desc}")
        else:
            print(f"  ❌ 缺少 {desc}")
        
except Exception as e:
    print(f"  ❌ 工作流文件读取失败: {e}")

# 检查 main.py
print("\n🚀 入口脚本检查:")
try:
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('tp(9).py', '加载 tp(9).py'),
        ('Game()', '创建 Game 实例'),
        ('run()', '调用 run 方法')
    ]
    
    for check, desc in checks:
        if check in content:
            print(f"  ✅ {desc}")
        else:
            print(f"  ❌ {desc}")
            
except Exception as e:
    print(f"  ❌ main.py 读取失败: {e}")

print("\n" + "="*40)
if all_exists:
    print("🎉 所有文件已准备就绪！")
    print("\n📋 下一步操作:")
    print("1. 将所有文件上传到 GitHub 仓库")
    print("2. 等待 1-5 分钟让 GitHub 扫描工作流")
    print("3. 进入 Actions 页面找到 'Build Android APK'")
    print("4. 点击 'Run workflow' 手动触发构建")
else:
    print("❌ 缺少必要文件，请检查！")