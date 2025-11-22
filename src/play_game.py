"""
使用训练好的模型自动进行贪食蛇游戏
无需训练，直接加载模型并进行游戏演示
"""

import torch
import json
from game import SnakeGameAI, Direction, Point
import numpy as np
import os
import sys

# 添加上级目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class GamePlayer:
    def __init__(self, model_path=None):
        """初始化游戏玩家，加载预训练模型"""
        if model_path is None:
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'model.pth')
        self.load_model(model_path)
        self.load_history_score()
    
    def load_model(self, model_path):
        """加载训练好的模型"""
        try:
            self.model = torch.load(model_path, map_location='cpu')
            self.model.eval()  # 设置为评估模式
            print(f"✓ 模型加载成功: {model_path}")
        except FileNotFoundError:
            print(f"✗ 模型文件不存在: {model_path}")
            print("  请先运行 python agent.py 进行训练")
            raise
    
    def load_history_score(self):
        """加载历史最高分"""
        history_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'history_score.json')
        try:
            with open(history_path, 'r') as file:
                data = json.load(file)
                self.history_score = data['history_score']
                print(f"✓ 历史最高分: {self.history_score}")
        except FileNotFoundError:
            self.history_score = 0
            print("⚠ 未找到历史分数文件")
    
    def get_state(self, game):
        """获取游戏状态（与agent.py中的逻辑相同）"""
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y,  # food down
            
            # 蛇长度信息（归一化到 0-1）
            len(game.snake) / 100,  # 蛇长度比例
        ]
        return np.array(state, dtype=float)
    
    def get_action(self, state):
        """使用模型预测行动（不进行随机探索）"""
        with torch.no_grad():  # 不计算梯度，加快推理速度
            state_tensor = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_tensor)
            move = torch.argmax(prediction).item()
            final_move = [0, 0, 0]
            final_move[move] = 1
        return final_move
    
    def play_game(self, num_games=5, show_display=True, speed=20):
        """
        运行游戏
        
        Args:
            num_games: 要进行多少局游戏
            show_display: 是否显示游戏画面（True为显示，False为快速运行）
            speed: 游戏速度（每秒帧数，默认20）
        """
        game = SnakeGameAI(if_show=show_display, speed=speed)
        scores = []
        
        print(f"\n{'='*50}")
        print(f"开始自动游戏 - 进行 {num_games} 局游戏")
        print(f"游戏画面显示: {show_display}")
        print(f"{'='*50}\n")
        
        for game_num in range(1, num_games + 1):
            score = 0
            while True:
                # 获取当前状态
                state = self.get_state(game)
                
                # 使用模型预测行动
                action = self.get_action(state)
                
                # 执行行动
                reward, done, score = game.play_step(action)
                
                if done:
                    game.reset()
                    break
            
            scores.append(score)
            print(f"第 {game_num:2d} 局 - 得分: {score:3d}")
        
        # 计算统计信息
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        print(f"\n{'='*50}")
        print(f"游戏总结:")
        print(f"  平均得分: {avg_score:.1f}")
        print(f"  最高得分: {max_score}")
        print(f"  最低得分: {min_score}")
        print(f"  历史最高: {self.history_score}")
        print(f"{'='*50}\n")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='使用训练好的模型进行贪食蛇游戏')
    parser.add_argument('--games', type=int, default=5, help='要进行的游戏局数（默认5）')
    parser.add_argument('--no-display', action='store_true', help='不显示游戏画面，加快运行速度')
    parser.add_argument('--model', type=str, default='./model/model.pth', help='模型文件路径')
    parser.add_argument('--speed', type=int, default=20, help='游戏速度（帧数/秒，默认20，范围1-100）')
    
    args = parser.parse_args()
    
    # 限制速度在合理范围内
    speed = max(1, min(args.speed, 100))
    
    try:
        player = GamePlayer(model_path=args.model)
        player.play_game(num_games=args.games, show_display=not args.no_display, speed=speed)
    except FileNotFoundError:
        print("\n请先运行以下命令进行模型训练:")
        print("  python agent.py")


if __name__ == '__main__':
    main()
