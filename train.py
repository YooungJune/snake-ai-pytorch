#!/usr/bin/env python
"""
训练 AI Snake 模型的启动脚本
从项目根目录运行: python train.py
"""

import sys
import os

# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# 导入并运行训练
from agent import Agent, train

if __name__ == '__main__':
    train()
