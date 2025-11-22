# Snake AI PyTorch

基于深度 Q 学习和 PyTorch 的贪食蛇 AI 项目。

## 快速开始

请参考 [docs/README.md](docs/README.md) 了解项目详情和使用指南。

### 训练模型
```bash
python train.py
```

### 运行模型
```bash
python play.py --games 5 --speed 20
```

## 项目结构

详见 [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

```
snake-ai-pytorch/
├── src/           # 源代码
├── model/         # 模型和数据
├── data/          # 资源文件
├── docs/          # 文档
├── config/        # 配置
├── human_play/    # 人类游戏
├── train.py       # 训练启动脚本
└── play.py        # 游戏启动脚本
```

## 文档

- [README.md](docs/README.md) - 项目介绍
- [TRAINING_GUIDE.md](docs/TRAINING_GUIDE.md) - 训练指南
- [MODEL_USAGE.md](docs/MODEL_USAGE.md) - 模型使用
- [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) - 项目结构说明

