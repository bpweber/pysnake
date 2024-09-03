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

move_speed = 15

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

snake_pos = [100, 50]

snake_bod = [[100, 50],
             [90, 50],
             [80, 50],
             [70, 50]
]

food_pos = [random.randrange(1, (win_x//10)) * 10,
            random.randrange(1, (win_y//10)) * 10]
food_spawn = True

dir = RIGHT
new_dir = dir

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

if __name__ == '__main__':
    while True:
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key in key_maps:
                new_dir = key_maps[e.key]

        dir = dir if dir + new_dir == 0 else new_dir

        if dir == UP:
            snake_pos[1] -= 10
        if dir == DOWN:
            snake_pos[1] += 10
        if dir == LEFT:
            snake_pos[0] -= 10
        if dir == RIGHT:
            snake_pos[0] += 10

        snake_bod.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 10
            move_speed += 2
            food_spawn = False
        else:
            snake_bod.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (win_x//10)) * 10,
                        random.randrange(1, (win_y//10)) * 10]

        food_spawn = True
        game_window.fill(black)

        for pos in snake_bod:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0] < 0 or snake_pos[0] > win_x-10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > win_y-10:
            game_over()

        for block in snake_bod[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        display_score(1, white, 'JetBrainsMono Nerd Font', 40)

        pygame.display.update()
        fps.tick(move_speed)

