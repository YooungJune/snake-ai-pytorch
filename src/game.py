import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import os

pygame.init()
# 获取 arial.ttf 的路径
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
font_path = os.path.join(data_dir, 'arial.ttf')
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 25)
else:
    # 如果找不到，使用系统字体
    font = pygame.font.SysFont('arial', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 20

class SnakeGameAI:

    def __init__(self, w=640, h=480, if_show=False, speed=20):
        self.w = w
        self.h = h
        self.speed = speed  # 游戏速度（每秒帧数）
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.show_run = if_show
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.show_run = not self.show_run
        
        # 计算旧距离（移动前的蛇头与食物距离）
        old_dist = abs(self.head.x - self.food.x) + abs(self.head.y - self.food.y)
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 计算新距离（移动后的蛇头与食物距离）
        new_dist = abs(self.head.x - self.food.x) + abs(self.head.y - self.food.y)
        
        # 3. check if game over
        reward = 0
        game_over = False
        
        # 计算"死亡倒计时惩罚"：超时时间越长，惩罚越大
        # 这会强制 AI 必须不断吃食物（找到食物）或者探索，而不是原地转圈
        max_frames = 100 * len(self.snake)
        frames_left = max_frames - self.frame_iteration
        
        # === 动态奖励系数（随蛇长度变化） ===
        # 蛇越长，各种奖励都增加，但死亡惩罚减少
        snake_length_factor = len(self.snake) / 3  # 从3开始计算，初始值为1
        
        if self.is_collision():
            game_over = True
            # 蛇越长，死亡惩罚越少（因为已经玩得很好了）
            death_penalty = -10 / snake_length_factor  # 蛇长3时-10，蛇长6时-5，蛇长30时-1
            reward = death_penalty
            return reward, game_over, self.score
        
        if self.frame_iteration > max_frames:
            game_over = True
            death_penalty = -10 / snake_length_factor
            reward = death_penalty
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            # === 简化的吃食物奖励 ===
            # 蛇越长，吃到食物的奖励越多
            eating_reward = 10 * snake_length_factor
            reward = eating_reward
            self._place_food()
            self.frame_iteration = 0  # 重置计时器，鼓励持续吃食物
        else:
            self.snake.pop()
            
            # === 简化的奖励系统 ===
            # 只有三种奖励：距离、生存、超时
            # 移除冗余信号，让模型专注学习
            
            # 1. 距离奖励（强信号，前期有效）
            distance_bonus = 2.0 / len(self.snake)  # 增加系数
            
            if new_dist < old_dist:
                distance_reward = distance_bonus  # 接近食物：强奖励
            else:
                distance_reward = -distance_bonus  # 远离食物：强惩罚
            
            # 2. 超时惩罚（强压力，强制探索）
            timeout_penalty = -0.1 * (1 - frames_left / max_frames) if frames_left < max_frames * 0.3 else 0
            # 只在最后30%时间才施加惩罚，避免早期压力过大
            
            # 总奖励 = 距离 + 超时
            # 移除生存奖励，防止原地转圈
            reward = distance_reward + timeout_penalty
        
        # 5. update ui and clock
        if(self.show_run):
            self._update_ui()
            self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill(BLACK)

        # 绘制蛇，实现红（头）→深绿→淡绿（尾）的渐变色
        snake_length = len(self.snake)
        for idx, pt in enumerate(self.snake):
            # 计算颜色渐变：蛇头红色 → 蛇身深绿 → 尾部浅绿
            if idx == 0:
                # 蛇头：纯红色
                r, g, b = 200, 0, 0
            else:
                # 蛇身：深绿逐渐变淡到浅绿
                progress = (idx - 1) / max(1, snake_length - 2)  # 0到1的进度（从第二格开始）
                # 从深绿(0,150,0)逐渐变淡到浅绿(100,180,100)
                r = int(100 * progress)           # 0→100
                g = int(150 + 30 * progress)      # 150→180
                b = int(100 * progress)           # 0→100
            
            color = (r, g, b)
            pygame.draw.rect(self.display, color, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            
            # 内部高亮（使用深色版本）
            inner_color = (int(r * 0.5), int(g * 0.5), int(b * 0.5))
            pygame.draw.rect(self.display, inner_color, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)