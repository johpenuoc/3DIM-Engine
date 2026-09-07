import pygame
from pygame.locals import *

from engine.camera import Camera
class Engine:
    def __init__(self, Main):
        self.main = Main
        self.camera = Camera()

    # not really tracing, i just didnt know what to call it
    def trace_rays(self):
        #rays = list(self.camera.collect_rays().values())
        rays = self.camera.collect_rays()
        ppos = self.main.p.pos
        print(ppos)

        for transform in rays['0']:
            # these are the end points of each ray; relative to the player
            x = ppos[0] - transform[0]
            y = ppos[1] - transform[1]
            z = ppos[2] - transform[2]

            pygame.draw.line(self.main.display, (255, 0, 0), ppos[:2], (ppos[0] - x, ppos[1] - y))
