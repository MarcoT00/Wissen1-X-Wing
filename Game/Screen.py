import pygame
import sys


class Screen:
    CELL_SIZE = 24
    X_SIZE = None
    Y_SIZE = None
    MARK_COLOR = (255, 0, 0)  # Red color
    BG_COLOR = (255, 255, 255)  # White color
    LINE_COLOR = (0, 0, 0)  # Black color

    SPIEL_COLOR = (255, 255, 255)  # White
    RAND_COLOR = (70, 79, 81)
    START_COLOR = (143, 227, 136)
    ZIEL_COLOR = (219, 80, 74)
    LINE_COLOR = (0, 0, 0)  # Black

    def __init__(self, map):
        self.grid = map
        pygame.init()
        self.X_SIZE = len(map[0])
        self.Y_SIZE = len(map)
        self.screen = pygame.display.set_mode(
            (self.X_SIZE * self.CELL_SIZE, self.Y_SIZE * self.CELL_SIZE)
        )

    def show_map(self):
        self.draw_grid(self.screen)
        pygame.display.flip()

    def show_player(self, position):
        self.draw_player(self.screen, position)
        pygame.display.flip()

    def draw_grid(self, screen):
        screen.fill(self.RAND_COLOR)
        for row in range(self.Y_SIZE):
            for col in range(self.X_SIZE):
                rect = self.get_rect(row, col)
                pygame.draw.rect(screen, self.LINE_COLOR, rect, 1)
                self.color_grid(screen, row, col)

    def color_grid(self, screen, row, col):
        rect = self.get_rect(row, col)
        if self.grid[row][col] is not None:
            if self.grid[row][col] == "X":
                pygame.draw.circle(
                    screen, self.SPIEL_COLOR, rect.center, self.CELL_SIZE // 4
                )
            elif self.grid[row][col] == "Z":
                pygame.draw.circle(
                    screen, self.ZIEL_COLOR, rect.center, self.CELL_SIZE // 4
                )
            elif self.grid[row][col] == "S":
                pygame.draw.circle(
                    screen, self.START_COLOR, rect.center, self.CELL_SIZE // 4
                )
            elif self.grid[row][col] == "R":
                pygame.draw.circle(
                    screen, self.RAND_COLOR, rect.center, self.CELL_SIZE // 4
                )

    def draw_player(self, screen, position: dict):
        row = position["y"]
        col = position["x"]
        if self.grid[row][col] is not None:
            rect = self.get_rect(row, col)
            pygame.draw.circle(screen, (0, 255, 255), rect.center, self.CELL_SIZE // 4)

    def get_rect(self, row, col):
        return pygame.Rect(
            col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE
        )
