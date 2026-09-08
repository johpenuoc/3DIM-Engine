import pygame
from pygame.locals import *
from math import degrees, asin

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
        pdir = self.main.p.dir
        cam_size = self.camera.cam_size
        #print(ppos)

        for transform in self.rays['0'][:int(len(self.rays['0']) / 4)]:
            # these are the end points of each ray; relative to the player
            thetas = transform[3]
            #x_theta = degrees(asin(x / y))
            #z_theta = degrees(asin((cam_size / 2) / z))

            x = cam_size + ppos[0] - transform[0]
            y = cam_size + ppos[1] - transform[1]
            z = cam_size + ppos[2] - transform[2]
            #print('y pos: ', y)

            ray = [ppos, (x, y, z)]
            

            pygame.draw.line(self.main.display, (255, 0, 0), ppos[:2], (x, y))
