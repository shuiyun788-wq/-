import pygame , sys , random
from pygame.math import Vector2




class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(1,0)
        self.add_new_block = False
    def draw_snake(self):
        for block in  self.body:
            x_pos=block.x*cell_size
            y_pos=block.y*cell_size
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,(0,204,204),block_rect)
    def move_snake(self):
        if not self.add_new_block:
            body_copy = self.body[:-1]  # 保留除最后一节蛇身
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

        else:
            body_copy = self.body[:]  # 保留除最后一节蛇身
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.add_new_block = False


    def add_block(self):
        self.add_new_block = True



class FRUIT:
    def __init__(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)
    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size,self.pos.y*cell_size,cell_size,cell_size)
        pygame.draw.rect(screen,(215,0,0),fruit_rect)
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
#主循环,including 蛇位置，刷新。渲染，判断是否吃到果实
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
    def draw_score(self):
        score_text = 'Score:'+str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text,True,(56,74,12))

        score_rect = score_surface.get_rect(center = (40,10))
        screen.blit(score_surface,score_rect )

    def check_fail(self):
        if (not 0 <= self.snake.body[0].x <= cell_number-1) or (not 0 <= self.snake.body[0].y <= cell_number-1):
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    def game_over(self):
        pygame.quit()
        sys.exit()

    def is_available(self, direction):
        new_head = self.snake.body[0] + direction
        if new_head in self.snake.body:
            return False
        return True


pygame.init()#初始化pygame
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number))
clock=pygame.time.Clock()
game_font = pygame.font.Font(None,25)
main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

    # 定义可能的方向
    possible_directions = [
        Vector2(1, 0),  # 向右
        Vector2(-1, 0), # 向左
        Vector2(0, 1),  # 向下
        Vector2(0, -1)  # 向上
    ]

    # 优先朝食物移动的逻辑
    if main_game.fruit.pos.x < main_game.snake.body[0].x and main_game.snake.direction != Vector2(1, 0):
        target_direction = Vector2(-1, 0)
    elif main_game.fruit.pos.x > main_game.snake.body[0].x and main_game.snake.direction != Vector2(-1, 0):
        target_direction = Vector2(1, 0)
    elif main_game.fruit.pos.y < main_game.snake.body[0].y and main_game.snake.direction != Vector2(0, 1):
        target_direction = Vector2(0, -1)
    elif main_game.fruit.pos.y > main_game.snake.body[0].y and main_game.snake.direction != Vector2(0, -1):
        target_direction = Vector2(0, 1)
    else:
        target_direction = main_game.snake.direction


    if  main_game.is_available(target_direction) ==False:

        for direction in possible_directions:
            if main_game.is_available(direction) == True:
                target_direction = direction
                break

    # 更新蛇的方向
    main_game.snake.direction = target_direction

    # 渲染游戏
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
