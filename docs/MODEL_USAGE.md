# 🎮 使用训练好的模型进行游戏

## 📋 模型保存验证

你的模型已成功保存：
- ✓ **模型文件**: `model/model.pth` - 存在
- ✓ **最高分记录**: `model/history_score.json` - 存在

## 🚀 快速开始

### 方式1：使用默认配置进行5局游戏（显示画面）
```powershell
python play_game.py
```

### 方式2：进行10局游戏
```powershell
python play_game.py --games 10
```

### 方式3：快速运行20局游戏（不显示画面，更快）
```powershell
python play_game.py --games 20 --no-display
```

### 方式4：使用自定义模型文件
```powershell
python play_game.py --model ./model/model.pth --games 5
```

## 📊 模型文件说明

### `model.pth` - 神经网络权重
- 包含所有训练后的权重和偏置
- 输入层: 11维（游戏状态）
- 隐藏层: 256个神经元
- 输出层: 3个动作（直走、右转、左转）

### `history_score.json` - 历史最高分
```json
{
  "history_score": 42
}
```

## 🔍 模型工作流程

1. **加载模型**
   ```python
   player = GamePlayer(model_path='./model/model.pth')
   ```

2. **获取游戏状态**（11维状态向量）
   - 3维：前方/右方/左方的危险信息
   - 4维：当前蛇的移动方向
   - 4维：食物的相对位置

3. **模型预测**
   ```python
   prediction = model(state)  # 得到3个动作的Q值
   action = argmax(prediction)  # 选择Q值最高的动作
   ```

4. **执行动作并循环**

## 💡 实用技巧

### 查看不同模型的对比
```powershell
# 保存当前模型备份
Copy-Item model/model.pth model/model_v1.pth

# 继续训练或重新训练
python agent.py

# 对比不同版本
python play_game.py --model model/model_v1.pth --games 10 --no-display
python play_game.py --model model/model.pth --games 10 --no-display
```

### 快速评估模型性能
```powershell
python play_game.py --games 100 --no-display
```
这会快速运行100局游戏并统计平均分数

## ⚙️ 模型参数

训练时使用的超参数：
- **学习率 (LR)**: 0.005
- **折扣系数 (gamma)**: 0.75
- **批大小**: 1000
- **最大记忆**: 100,000

## 🐛 常见问题

**Q: 模型文件不存在怎么办？**
```
A: 运行 python agent.py 进行训练，模型会自动保存
```

**Q: 如何知道模型是否训练充分？**
```
A: 运行 python play_game.py --games 50 --no-display
   对比输出的平均得分和最高分，通常应该有一定的稳定性
```

**Q: 能否改进模型性能？**
```
A: 可以调整 agent.py 中的参数：
   - 增加 BATCH_SIZE（更多样本学习）
   - 调整 LR（学习率）
   - 修改 gamma（折扣系数）
   然后重新运行 python agent.py
```

## 📈 训练进度建议

| 游戏局数 | 预期表现 |
|---------|---------|
| 100-200 | 初步学习，得分波动大 |
| 500-1000 | 逐渐改善，找到基本策略 |
| 2000+ | 相对稳定，得分提高 |
| 5000+ | 接近最优策略 |

建议至少训练2000局以上获得较好的模型。
