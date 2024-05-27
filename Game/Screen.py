import pygame
import sys


class Screen:
    GRID_SIZE = 33
    CELL_SIZE = 33
    WINDOW_SIZE = GRID_SIZE * CELL_SIZE
    MARK_COLOR = (255, 0, 0)  # Red color
    BG_COLOR = (255, 255, 255)  # White color
    LINE_COLOR = (0, 0, 0)  # Black color

    def __init__(self, map):
        self.grid = map
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))

    def show_map(self):
        self.draw_grid(self.screen)
        pygame.display.flip()

    def show_player(self):
        self.draw_player(self.screen)
        pygame.display.flip()

    def draw_grid(self, screen):
        screen.fill(self.BG_COLOR)
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                rect = self.getRect(row, col)
                pygame.draw.rect(screen, self.LINE_COLOR, rect, 1)
                self.color_grid(screen, row, col)

    def color_grid(self, screen, row, col):
        rect = self.getRect(row, col)
        if self.grid[row][col] is not None:
            if self.grid[row][col] == "X":
                pygame.draw.circle(screen, self.MARK_COLOR, rect.center, self.CELL_SIZE // 4)
            elif self.grid[row][col] == "Z":
                pygame.draw.circle(screen, (0, 0, 255), rect.center, self.CELL_SIZE // 4)
            elif self.grid[row][col] == "S":
                pygame.draw.circle(screen, (0, 255, 0), rect.center, self.CELL_SIZE // 4)
            elif self.grid[row][col] == "R":
                pygame.draw.circle(screen, (0, 0, 0), rect.center, self.CELL_SIZE // 4)

    def draw_player(self, screen, position: dict):
        row = position.x
        col = position.y
        if self.grid[row][col] is not None:
            rect = self.getRect(row, col)
            pygame.draw.circle(screen, (0, 255, 255), rect.center, self.CELL_SIZE // 4)

    def get_rect(self, row, col):
        return pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
