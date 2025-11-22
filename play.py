#!/usr/bin/env python
"""
运行已训练好的 AI Snake 模型的启动脚本
从项目根目录运行: python play.py [选项]

示例:
  python play.py --games 5
  python play.py --speed 50 --games 10
  python play.py --no-display --speed 100
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入并运行游戏
from play_game import main

if __name__ == '__main__':
    main()
