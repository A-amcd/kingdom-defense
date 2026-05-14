#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kingdom Defense APK打包脚本
自动完成GitHub仓库创建和代码推送
"""

import os
import sys
import subprocess
import webbrowser
import time

def run_command(cmd, description="", check=True):
    """运行命令并显示进度"""
    print(f"\n[执行] {description}")
    print(f"命令: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check,
            encoding='utf-8',
            errors='replace'
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"[错误] {result.stderr}", file=sys.stderr)
        
        if result.returncode == 0:
            print(f"✓ {description} 成功")
            return True
        else:
            print(f"✗ {description} 失败", file=sys.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} 失败: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ {description} 出错: {e}", file=sys.stderr)
        return False

def check_command(cmd):
    """检查命令是否存在"""
    try:
        result = subprocess.run(
            f"where {cmd}" if os.name == 'nt' else f"which {cmd}",
            shell=True,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False

def main():
    print("=" * 60)
    print("   Kingdom Defense APK 打包助手")
    print("=" * 60)
    
    # 检查必要工具
    print("\n[检查] 必要工具...")
    
    tools = {
        'git': 'Git',
        'gh': 'GitHub CLI'
    }
    
    missing = []
    for cmd, name in tools.items():
        if check_command(cmd):
            print(f"  ✓ {name} 已安装")
        else:
            print(f"  ✗ {name} 未安装")
            missing.append((cmd, name))
    
    if missing:
        print("\n[错误] 以下工具未安装:")
        for cmd, name in missing:
            print(f"  - {name}")
        print("\n请先安装这些工具:")
        print("  Git: https://git-scm.com/download/win")
        print("  GitHub CLI: https://cli.github.com/")
        return 1
    
    # 获取用户信息
    print("\n[输入] 请提供GitHub信息:")
    github_user = input("  GitHub 用户名: ").strip()
    github_email = input("  GitHub 邮箱: ").strip()
    
    if not github_user or not github_email:
        print("\n[错误] 用户名和邮箱不能为空")
        return 1
    
    repo_name = input("  仓库名称 [kingdom-defense]: ").strip()
    if not repo_name:
        repo_name = "kingdom-defense"
    
    # 配置Git
    print("\n[步骤 1/5] 配置Git...")
    run_command(f'git config --global user.name "{github_user}"', "设置用户名")
    run_command(f'git config --global user.email "{github_email}"', "设置邮箱")
    
    # GitHub认证
    print("\n[步骤 2/5] GitHub认证...")
    print("请在浏览器中完成GitHub授权...")
    webbrowser.open("https://github.com/login/device")
    
    print("\n打开浏览器后，输入代码完成授权")
    print("或者在终端中运行: gh auth login")
    input("\n按回车键继续...")
    
    # 检查认证状态
    if not run_command("gh auth status", "检查GitHub认证状态", check=False):
        print("\n请先运行 'gh auth login' 完成认证")
        return 1
    
    # 初始化Git仓库
    print("\n[步骤 3/5] 初始化Git仓库...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if os.path.exists(".git"):
        print("  Git仓库已存在，跳过初始化")
    else:
        run_command("git init", "初始化Git仓库")
        run_command("git add .", "添加文件到暂存区")
        run_command('git commit -m "Kingdom Defense - Initial commit"', "提交代码")
    
    # 创建GitHub仓库
    print("\n[步骤 4/5] 创建GitHub仓库...")
    remote_url = f"https://github.com/{github_user}/{repo_name}.git"
    
    # 检查远程仓库是否已存在
    check_remote = subprocess.run(
        f"git remote get-url origin",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if check_remote.returncode == 0:
        print("  远程仓库已配置，跳过创建")
    else:
        run_command(
            f'gh repo create {repo_name} --public --source=. --remote=origin',
            "创建GitHub仓库"
        )
    
    # 推送代码
    print("\n[步骤 5/5] 推送代码...")
    run_command("git branch -M main", "切换到main分支")
    
    # 设置远程仓库（如果还没有）
    if check_remote.returncode != 0:
        run_command(f'git remote add origin {remote_url}', "添加远程仓库")
    
    if not run_command("git push -u origin main", "推送代码到GitHub", check=False):
        print("\n推送失败，尝试强制推送...")
        if not run_command("git push -u origin main --force", "强制推送代码", check=False):
            print("\n请手动推送代码:")
            print(f"  git remote add origin {remote_url}")
            print(f"  git push -u origin main")
            return 1
    
    # 完成
    print("\n" + "=" * 60)
    print("   ✅ 所有步骤完成！")
    print("=" * 60)
    
    print("\n📋 接下来的操作:")
    print(f"  1. 打开 https://github.com/{github_user}/{repo_name}")
    print(f"  2. 点击 'Actions' 标签查看构建进度")
    print(f"  3. 等待15-20分钟让GitHub Actions完成构建")
    print(f"  4. 点击构建任务，在Artifacts下载APK文件")
    
    print("\n📱 下载APK后:")
    print("  - 将APK文件传到手机")
    print("  - 在手机上安装（可能需要允许未知来源）")
    print("  - 开始游戏！")
    
    print("\n💡 提示:")
    print("  - 首次构建需要下载Android SDK组件，可能较慢")
    print("  - 后续更新代码会自动重新构建APK")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
