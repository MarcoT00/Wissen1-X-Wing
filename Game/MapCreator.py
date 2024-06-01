import pygame
import sys
import csv
import os

# Ziel: Z; Spiel: X; Start: S; Border: R

GRID_WIDTH = 32  # top1: 18; top2: 33
GRID_HEIGHT = 30  # top1: 34; top2: 32
CELL_SIZE = 20

SPIEL_COLOR = (255, 255, 255)  # White
RAND_COLOR = (70, 79, 81)
START_COLOR = (143, 227, 136)
ZIEL_COLOR = (219, 80, 74)
LINE_COLOR = (0, 0, 0)  # Black

# Board
grid = [["R" for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def draw_grid(screen):
    screen.fill(RAND_COLOR)
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)
            if grid[row][col] == "X":
                pygame.draw.circle(screen, SPIEL_COLOR, rect.center, CELL_SIZE // 4)
            elif grid[row][col] == "S":
                pygame.draw.circle(screen, START_COLOR, rect.center, CELL_SIZE // 4)
            elif grid[row][col] == "Z":
                pygame.draw.circle(screen, ZIEL_COLOR, rect.center, CELL_SIZE // 4)


def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
    pygame.display.set_caption("2D Grid with Mouse Interaction")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if grid[row][col] == "R":
                    grid[row][col] = "X"
                elif grid[row][col] == "X":
                    grid[row][col] = "S"
                elif grid[row][col] == "S":
                    grid[row][col] = "Z"
                else:
                    grid[row][col] = "R"

        draw_grid(screen)
        pygame.display.flip()


def save_grid(filename, grid):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in grid:
            writer.writerow(row)
    print(f"Saved to {filename}")


if __name__ == "__main__":
    main()
    # savegrid("topology1.csv", grid)
    # print(grid)
