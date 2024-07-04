import pygame


class Screen:
    CELL_SIZE = 26
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
        pygame.font.init()
        self.font = pygame.font.SysFont("Comic Sans MS", self.CELL_SIZE - 4)

    def show_map(self):
        self.draw_grid(self.screen)
        pygame.display.update()

    def show_player(self, position, cost):
        self.draw_player(self.screen, position, cost)
        pygame.display.update()

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

    def draw_player(self, screen, position: dict, cost):
        pygame.event.clear()
        row = position["y"]
        col = position["x"]
        if self.grid[row][col] is not None:
            rect = self.get_rect(row, col)
            pygame.draw.circle(
                screen, self.RAND_COLOR, rect.center, self.CELL_SIZE // 4
            )

            text = self.font.render(str(cost), True, (0, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (
                col * self.CELL_SIZE + self.CELL_SIZE // 2,
                row * self.CELL_SIZE + self.CELL_SIZE // 2,
            )
            self.screen.blit(text, text_rect)

            # self.font.render_to(screen, (position['x'], position['y']), cost, (64, 86, 244))
            # pygame.draw.circle(screen, (64, 86, 244), rect.center, self.CELL_SIZE // 4)

    def get_rect(self, row, col):
        return pygame.Rect(
            col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE
        )

    def save_as_image(self, name):
        '''image = pygame.Surface((self.X_SIZE, self.Y_SIZE))
        image.blit(self.screen, (self.X_SIZE, self.Y_SIZE), (self.X_SIZE, self.Y_SIZE))  # Blit portion of the display to the image
        pygame.image.save(image, name)  # Save the image to the disk'''
        pygame.image.save(self.screen, name)

    def close(self):
        pygame.display.quit()
        pygame.quit()