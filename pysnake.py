import pygame
import time
import random

UP = 1
DOWN = -1
LEFT = -2
RIGHT = 2

key_maps = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT
}

move_speed = 60

win_x = 1920
win_y = 1080

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()

pygame.display.set_caption('pysnake')
game_window = pygame.display.set_mode((win_x, win_y))

fps = pygame.time.Clock()

score = 0

def display_score():
    font = pygame.font.SysFont('JetBrainsMono Nerd Font', 30)
    surface = font.render(f'SCORE {score}', True, white)
    rect = surface.get_rect()
    game_window.blit(surface, rect)

def game_over():
    font = pygame.font.SysFont('JetBrainsMono Nerd Font', 50)
    surface = font.render(f'GAME OVER | SCORE {score}', True, red)
    rect = surface.get_rect()
    rect.midtop = (win_x/2, win_y/2)
    game_window.blit(surface, rect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    quit()

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self, x, y, size, length, dir):
        self.head = Position(x, y)
        self.size = size
        self.body = []
        for i in range(length):
            self.body.append(Position(x - (i * size), y))
        self.dir = dir
    def changedir(self, new_dir):
        self.dir = self.dir if self.dir + new_dir == 0 else new_dir
        if self.dir == UP:
            self.head.y -= self.size/4
        if self.dir == DOWN:
            self.head.y += self.size/4
        if self.dir == LEFT:
            self.head.x -= self.size/4
        if self.dir == RIGHT:
            self.head.x += self.size/4

class Food:
    def __init__(self, size):
        self.is_spawned = True
        self.size = size
        self.pos = Position(
            random.randrange(1, (win_x//self.size)) * self.size,
            random.randrange(1, (win_y//self.size)) * self.size
        )
    def spawnfood(self):
        self.__init__(self.size)

if __name__ == '__main__':
    size = 16
    snake = Snake(x=size*4, y=size*2, size=size, length=2, dir=RIGHT)
    food = Food(size=size)
    new_dir = snake.dir
    frame_ctr = 0
    while True:
        if frame_ctr % 4 == 0:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN and e.key in key_maps:
                    new_dir = key_maps[e.key]
        snake.changedir(new_dir)

        snake.body.insert(0, Position(snake.head.x, snake.head.y))
        if snake.head.x == food.pos.x and snake.head.y == food.pos.y:
            score += 10
            move_speed += 2
            food.is_spawned = False
        else:
            snake.body.pop()

        if not food.is_spawned:
            food.spawnfood()

        game_window.fill(black)

        for pos in snake.body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos.x, pos.y, snake.size, snake.size))
        pygame.draw.rect(game_window, red, pygame.Rect(food.pos.x, food.pos.y, food.size, food.size))

        if snake.head.x < 0 or snake.head.x > (win_x - snake.size):
            game_over()
        if snake.head.y < 0 or snake.head.y > (win_y - snake.size):
            game_over()
        for block in snake.body[1:]:
            if snake.head.x == block.x and snake.head.y == block.y:
                game_over()

        display_score()

        pygame.display.update()
        fps.tick(move_speed)
        frame_ctr += 1

