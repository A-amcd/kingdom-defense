# Kingdom Defense - 王国防线

一款融合经典塔防玩法的移动端游戏，支持中文字体显示。

## 游戏特性

- 🎮 经典塔防玩法
- 🏰 多种地图主题（精灵森林、冰封山脉、王国城堡、灼热沙漠等）
- 🎯 多样化的敌人类型
- 🛡️ 多种防御塔选择
- 📱 专为移动设备优化

## 运行游戏

```bash
# 安装依赖
pip install -r requirements.txt

# 运行游戏
python main.py
```

## APK构建

本项目使用 GitHub Actions 自动构建 Android APK：

1. Fork 本仓库
2. 推送代码到 main 分支
3. GitHub Actions 将自动构建 APK
4. 在 Actions 页面下载生成的 APK 文件

## 项目结构

- `main.py` - 游戏入口
- `tp.py` - 游戏主逻辑
- `tp(9).py` - 游戏核心文件
- `setup.py` - 项目配置文件
- `buildozer.spec` - Buildozer 构建配置
- `icon.png` - 应用图标

## 开发环境

- Python 3.x
- Pygame
- Buildozer (用于Android打包)

## 许可证

本项目仅供学习交流使用。
