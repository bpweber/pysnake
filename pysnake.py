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

move_speed = 10

win_x = 1280
win_y = 720

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

def display_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f'SCORE {score}', True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

def game_over():
    font = pygame.font.SysFont('JetBrainsMono Nerd Font', 50)
    game_over_surface = font.render(f'GAME OVER | SCORE {score}', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (win_x/2, win_y/2)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()
    quit()

class Snake:
    def __init__(self, x, y, size, length, dir):
        self.x = x
        self.y = y
        self.size = size
        self.body = [[x, y]]
        for i in range(length-1):
            self.body.append([x - (i * size), y])
        self.dir = dir

    def changedir(self, new_dir):
        self.dir = self.dir if self.dir + new_dir == 0 else new_dir
        if self.dir == UP:
            self.y -= self.size
        if self.dir == DOWN:
            self.y += self.size
        if self.dir == LEFT:
            self.x -= self.size
        if self.dir == RIGHT:
            self.x += self.size

class Food:
    def __init__(self, size):
        self.is_spawned = True
        self.size = size
        self.x = random.randrange(1, (win_x//self.size)) * self.size
        self.y = random.randrange(1, (win_y//self.size)) * self.size 

    def spawnfood(self):
        self.__init__(self.size)

if __name__ == '__main__':
    snake = Snake(x=100, y=40, size=20, length=1, dir=RIGHT)
    new_dir = snake.dir
    food = Food(size=20)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key in key_maps:
                new_dir = key_maps[e.key]

        snake.changedir(new_dir)

        snake.body.insert(0, [snake.x, snake.y])
        if snake.x == food.x and snake.y == food.y:
            score += 10
            move_speed += 2
            food.is_spawned = False
        else:
            snake.body.pop()

        if not food.is_spawned:
            food.spawnfood()

        game_window.fill(black)

        for pos in snake.body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], snake.size, snake.size))

        pygame.draw.rect(game_window, red, pygame.Rect(food.x, food.y, food.size, food.size))

        if snake.x < 0 or snake.x > win_x-snake.size:
            game_over()
        if snake.y < 0 or snake.y > win_y-snake.size:
            game_over()

        for block in snake.body[1:]:
            if snake.x == block[0] and snake.y == block[1]:
                game_over()

        display_score(1, white, 'JetBrainsMono Nerd Font', 40)

        pygame.display.update()
        fps.tick(move_speed)

