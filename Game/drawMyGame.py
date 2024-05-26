import pygame
import sys


GRID_SIZE = 32
CELL_SIZE = 32
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
MARK_COLOR = (255, 0, 0)  # Red color
BG_COLOR = (255, 255, 255)  # White color
LINE_COLOR = (0, 0, 0)  # Black color

#Boarder R
#grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
grid = [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'Z'], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'Z'], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'Z'], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'Z'], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'Z'], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'Z'], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'X', 'X', 'X', 'X', 'X', 'X', None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'S', 'S', 'S', 'S', 'S', 'S', None, None, None, None, None, None, None, None]]

def draw_grid(screen):
    screen.fill(BG_COLOR)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LINE_COLOR, rect, 1)
            if grid[row][col] is not None:
                pygame.draw.circle(screen, MARK_COLOR, rect.center, CELL_SIZE // 4)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
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
                if grid[row][col] is None:
                    grid[row][col] = 'R'
                else:
                    grid[row][col] = None

        draw_grid(screen)
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    except:
        print(grid)
