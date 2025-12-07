import pygame
import random

# 初始化游戏
pygame.init()
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 定义蛇和食物
snake = [(100, 100), (80, 100), (60, 100)]  # 蛇的初始位置
food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
        random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)  # 随机生成食物
score = 0  # 初始化得分

# 绘制蛇
def draw_snake(screen, snake):
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*segment, CELL_SIZE, CELL_SIZE))

# 绘制食物
def draw_food(screen, food):
    pygame.draw.rect(screen, (255, 0, 0), (*food, CELL_SIZE, CELL_SIZE))

# 绘制得分
def draw_score(screen, score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

# 检查某个方向是否会导致蛇与自身碰撞
def is_valid_move(snake, direction):
    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])
    if new_head in snake:  # 新头部位置如果已经在蛇身上，就不能走
        return False
    return True

# 简单AI策略：朝向食物移动，同时避免撞到自己
def get_direction(snake, food):
    head = snake[0]
    directions = [(CELL_SIZE, 0), (-CELL_SIZE, 0), (0, CELL_SIZE), (0, -CELL_SIZE)]  # 右、左、下、上
    random.shuffle(directions)  # 随机化方向，避免总是朝同一方向走

    # 优先考虑吃到食物的方向，同时避免与自己碰撞
    for direction in directions:
        if is_valid_move(snake, direction):
            if food[0] > head[0] and direction == (CELL_SIZE, 0):  # 食物在右
                return direction
            elif food[0] < head[0] and direction == (-CELL_SIZE, 0):  # 食物在左
                return direction
            elif food[1] > head[1] and direction == (0, CELL_SIZE):  # 食物在下
                return direction
            elif food[1] < head[1] and direction == (0, -CELL_SIZE):  # 食物在上
                return direction

    # 如果没有找到朝食物的有效方向，返回一个不与自己撞的方向
    for direction in directions:
        if is_valid_move(snake, direction):
            return direction
    return (0, 0)  # 如果所有方向都无效，则停下

# 主循环
running = True
while running:
    screen.fill((0, 0, 0))  # 清屏
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # AI计算下一步方向
    direction = get_direction(snake, food)

    # 更新蛇的位置
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, new_head)  # 插入新头部

    # 检测是否吃到食物
    if snake[0] == food:
        food = (random.randint(0, WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                random.randint(0, HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
        score += 1  # 每吃一个食物加一分
    else:
        snake.pop()  # 如果没有吃到食物，去掉尾巴

    # 检测碰撞（边界或自身）
    if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
        snake[0][1] < 0 or snake[0][1] >= HEIGHT or
        snake[0] in snake[1:]):
        running = False

    # 绘制蛇、食物和得分
    draw_snake(screen, snake)
    draw_food(screen, food)
    draw_score(screen, score)

    # 更新显示
    pygame.display.flip()
    clock.tick(15)

print('得分为', score)
pygame.quit()


