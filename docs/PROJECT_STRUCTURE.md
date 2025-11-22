# 项目结构说明

整理后的项目文件夹结构如下：

```
snake-ai-pytorch/
├── src/                           # 源代码目录
│   ├── agent.py                   # AI 代理，负责训练循环
│   ├── game.py                    # 游戏环境
│   ├── model.py                   # 神经网络模型定义
│   ├── helper.py                  # 辅助函数（绘图）
│   └── play_game.py               # 游戏推理脚本
│
├── model/                         # 模型和数据目录
│   ├── model.pth                  # 训练好的模型权重
│   ├── history_score.json         # 历史最高分和游戏次数
│   └── training_progress.png      # 训练曲线图
│
├── data/                          # 数据和资源目录
│   └── arial.ttf                  # 字体文件
│
├── docs/                          # 文档目录
│   ├── README.md                  # 项目说明
│   ├── MODEL_USAGE.md             # 模型使用指南
│   └── TRAINING_GUIDE.md          # 训练指南
│
├── config/                        # 配置文件目录
│   └── environment.yml            # Conda 环境配置
│
├── human_play/                    # 人类游戏脚本
│   └── snake_game_human.py        # 人类玩家版本
│
├── train.py                       # 训练启动脚本（根目录）
├── play.py                        # 游戏启动脚本（根目录）
├── README.md                      # 根目录说明（链接到 docs/README.md）
├── .gitignore                     # Git 忽略文件
└── LICENSE                        # 许可证

```

## 使用方式

### 训练模型
从项目根目录运行：
```bash
python train.py
```

### 运行已训练的模型
```bash
# 基本用法（默认5局，速度20 FPS）
python play.py

# 指定游戏局数
python play.py --games 10

# 调节游戏速度（单位：帧/秒，范围 1-100）
python play.py --speed 50

# 不显示画面，加快运行
python play.py --no-display --speed 100

# 组合使用
python play.py --games 20 --speed 30
```

### 运行人类版本
```bash
python human_play/snake_game_human.py
```

## 目录说明

| 文件夹 | 说明 |
|--------|------|
| `src/` | 核心源代码，包含 AI 训练和推理逻辑 |
| `model/` | 保存训练好的模型权重和历史数据 |
| `data/` | 资源文件（字体等） |
| `docs/` | 项目文档 |
| `config/` | 配置文件 |
| `human_play/` | 人类游戏脚本 |

## 文件说明

| 文件 | 说明 |
|-----|------|
| `src/agent.py` | AI 代理类，管理训练过程 |
| `src/game.py` | 游戏环境，包含游戏逻辑和渲染 |
| `src/model.py` | 神经网络模型定义和训练器 |
| `src/helper.py` | 绘制训练曲线图 |
| `src/play_game.py` | 使用训练好的模型进行游戏 |
| `train.py` | 训练启动脚本 |
| `play.py` | 游戏启动脚本 |
