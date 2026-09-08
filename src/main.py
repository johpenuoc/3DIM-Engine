import pygame
from pygame.locals import *
import sys

import conf.config as conf

import game.player as player

from engine.engine import Engine

class Main:
    def __init__(self):
        self.window = pygame.display.set_mode(conf.WIN_SIZE)
        self.display = pygame.Surface(conf.DIS_SIZE)

        self.dt = 0
        self.clock = pygame.time.Clock()

        self.p = player.Player()

        self.engine = Engine(self)

    def run(self):
        while 1:
            self.dt = self.clock.tick(conf.REL_FPS) / 1000

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.p.update(self.dt)



            self.display.fill((0, 0, 0))

            pygame.draw.rect(self.display, (255, 255, 255), (
                self.p.pos[0] - 4, self.p.pos[1] - 4, 8, 8
            ))

            self.engine.draw()

            self.window.blit(pygame.transform.scale(self.display, conf.WIN_SIZE), (0, 0))
            pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    main = Main()
    main.run()