import random
import time

import pygame
from pygame.locals import *


SIZE = 40                                                       # size of block (Dimensions 40x40)
BACKGROUND_COLOR = (92, 25, 84)


class Apple:
    def __init__(self, parent_screen ):
        self.apple_image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.apple_image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 19) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length                                                # [100] * 3 = [100, 100, 100]
        self.y = [SIZE] * length
        self.direction= 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def walk(self):                                                                                 # NOTE: Block gets pos of his previous block

        for i in range(self.length - 1, 0, -1):         # -1 --> step size
            self.x[i] = self.x[i-1]                     # current pos is the previous block-pos
            self.y[i] = self.y[i-1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0]  += SIZE
        if self.direction == 'up':
            self.y[0]  -= SIZE
        if self.direction == 'down':
            self.y[0]  += SIZE

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SNAKE GAME")

        pygame.mixer.init()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:

                return True

        return False


    def play_sound(self, sound_typ):
        sound = pygame.mixer.Sound(f"resources/{sound_typ}.mp3")
        pygame.mixer.Sound.play(sound)


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # self.snake.x[0], self.snake.y[0] --> Snake-Head
        # snake collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake collision with itself
        # collision only possible if length > 3
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game Over"

        # snake collsion with border
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"


    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('comicsansms', 30)
        line1 = font.render(f"GAME OVER!", True, (255, 255, 255))
        line2 = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        line3 = font.render(f"To play again press Enter. To Exit press Escape! ", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        self.surface.blit(line2, (200, 350))
        self.surface.blit(line3, (200, 400))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)


if __name__ == "__main__":
    game = Game()
    game.run()








