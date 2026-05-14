#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# 设置Android路径
try:
    import android
    android.init()
    android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
except ImportError:
    pass

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入游戏主模块
import tp

# 运行游戏
if __name__ == '__main__':
    game = tp.Game()
    game.run()