"""
Snake Game using Pygame
Author: Nilesh Babare
Purpose: Demonstrates OOP concepts, event handling, collision detection,
         and multimedia integration using Python.
"""

import pygame
import random
import time
from enum import Enum

# ---------------- CONSTANTS ---------------- #
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
BLOCK_SIZE = 40
FPS_DELAY = 0.12

# ---------------- ENUM FOR DIRECTION ---------------- #
class Direction(Enum):
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

# ---------------- APPLE CLASS ---------------- #
class Apple:
    def __init__(self, surface):
        self.surface = surface
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.move()

    def move(self):
        self.x = random.randint(1, 24) * BLOCK_SIZE
        self.y = random.randint(1, 19) * BLOCK_SIZE

    def draw(self):
        self.surface.blit(self.image, (self.x, self.y))

# ---------------- SNAKE CLASS ---------------- #
class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = Direction.DOWN
        self.length = 1
        self.x = [BLOCK_SIZE]
        self.y = [BLOCK_SIZE]

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == Direction.LEFT:
            self.x[0] -= BLOCK_SIZE
        elif self.direction == Direction.RIGHT:
            self.x[0] += BLOCK_SIZE
        elif self.direction == Direction.UP:
            self.y[0] -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            self.y[0] += BLOCK_SIZE

    def grow(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.surface.blit(self.image, (self.x[i], self.y[i]))

# ---------------- GAME CLASS ---------------- #
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snake Game - Interview Ready")

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.image.load("resources/background.jpg")

        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

        self.load_sounds()
        self.play_background_music()

    def load_sounds(self):
        self.sound_ding = pygame.mixer.Sound("resources/ding.mp3")
        self.sound_crash = pygame.mixer.Sound("resources/crash.mp3")

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1)

    def is_collision(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2

    def check_wall_collision(self):
        return not (0 <= self.snake.x[0] < WINDOW_WIDTH and
                    0 <= self.snake.y[0] < WINDOW_HEIGHT)

    def check_self_collision(self):
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0],
                                 self.snake.x[i], self.snake.y[i]):
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (850, 10))

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def render(self):
        self.surface.blit(self.background, (0, 0))
        self.snake.draw()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

    def game_over_screen(self):
        font = pygame.font.SysFont("arial", 30)
        self.surface.blit(self.background, (0, 0))
        msg1 = font.render(f"Game Over! Score: {self.snake.length}", True, (255, 255, 255))
        msg2 = font.render("Press Enter to Restart | Esc to Exit", True, (255, 255, 255))
        self.surface.blit(msg1, (300, 350))
        self.surface.blit(msg2, (250, 400))
        pygame.display.flip()

    def run(self):
        running = True
        paused = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_RETURN:
                        paused = False
                        pygame.mixer.music.unpause()

                    if not paused:
                        if event.key == pygame.K_LEFT:
                            self.snake.change_direction(Direction.LEFT)
                        elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction(Direction.RIGHT)
                        elif event.key == pygame.K_UP:
                            self.snake.change_direction(Direction.UP)
                        elif event.key == pygame.K_DOWN:
                            self.snake.change_direction(Direction.DOWN)

            if not paused:
                self.snake.move()

                if self.is_collision(self.snake.x[0], self.snake.y[0],
                                     self.apple.x, self.apple.y):
                    self.sound_ding.play()
                    self.snake.grow()
                    self.apple.move()

                if self.check_wall_collision() or self.check_self_collision():
                    self.sound_crash.play()
                    self.game_over_screen()
                    paused = True
                    pygame.mixer.music.pause()
                    self.reset()

                self.render()

            time.sleep(FPS_DELAY)

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    Game().run()
