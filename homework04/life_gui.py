import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size

        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.speed = speed

    def draw_lines(self) -> None:
        # Copy from previous assignment
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        """Нарисовать grid"""
        for i, row in enumerate(self.life.curr_generation):
            for j, cell in enumerate(row):
                color = pygame.Color("green") if cell else pygame.Color("white")
                pygame.draw.rect(
                    self.screen, color, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                )

    def run(self) -> None:
        # Copy from previous assignment
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.life.curr_generation = self.life.create_grid(randomize=True)

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                        print("Paused")
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and paused:
                        x, y = event.pos
                        # ячейка, внутри которой был клик
                        x //= self.cell_size
                        y //= self.cell_size
                        self.life.curr_generation[y][x] = not self.life.curr_generation[y][x]
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()
                if paused:
                    continue
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()

            if not paused:
                self.life.step()

            if self.life.is_max_generations_exceeded or not self.life.is_changing:
                running = False

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life = GameOfLife((20, 20))
    game = GUI(life)
    game.run()
