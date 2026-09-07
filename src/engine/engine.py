import pygame
from pygame.locals import *

from engine.camera import Camera
class Engine:
    def __init__(self, Main):
        self.main = Main
        self.camera = Camera()

        self.rays = self.camera.collect_rays()

    # not really tracing, i just didnt know what to call it
    def trace_rays(self):
        #rays = list(self.camera.collect_rays().values())
        ppos = self.main.p.pos
        #print(ppos)

        for transform in self.rays['0'][:int(len(self.rays['0']) / 4)]:
            # these are the end points of each ray; relative to the player
            x = ppos[0] - transform[0]
            y = ppos[1] - transform[1]
            z = ppos[2] - transform[2]
            #print('y pos: ', y)

            pygame.draw.line(self.main.display, (255, 0, 0), ppos[:2], (x, y))
