import pygame
from pygame.locals import *
from math import degrees, asin, sin, cos, radians

import conf.config as conf

from engine.camera import Camera
class Engine:
    def __init__(self, Main):
        self.main = Main
        self.camera = Camera()

        self.rays = self.camera.angle_rays()

    def angular_transformation(self, x_theta, z_theta):
        x_theta = (x_theta +- self.main.p.dir[0]) % 360
        z_theta = (z_theta + self.main.p.dir[1]) % 360

        # === everything below here is just some dumb maths to relate the 
        #     length of the z transformation to the length of the x and y
        #     transformations ===

        # z_theta can only be between 0 and 180
        # because a head can only look up and down; we're not owls
        z_transformation = sin(radians((z_theta + 90) % 360))
        #print(z_transformation, z_theta)
        l1 = conf.RAY_LEN * z_transformation
        x = sin(radians(x_theta)) * l1
        y = cos(radians(x_theta)) * l1

        # l1 is the adjacent side on the z-axis
        l2 = l1 / cos(radians(z_theta))
        z = sin(radians(z_theta)) * l2

        #print(f'{x_theta:.2f} | {z_theta:.2f}', [x, y, z])

        # the line rotates and shinks upon an increased z_theta
        #pygame.draw.line(win, (255, 255, 255), (250, 250), (250 + x, 250 - y))

        # (x, y, z) are the positional information of the ray's end-point
        return (x, y, z)

    # not really tracing, i just didnt know what to call it
    def trace_rays(self):
        #rays = list(self.camera.collect_rays().values())
        ppos = self.main.p.pos
        pdir = self.main.p.dir
        cam_size = self.camera.cam_size
        #print(ppos)

        for angle in self.rays:
            # these are the end points of each ray; relative to the player
            #thetas = transform[3]
            #x_theta = degrees(asin(x / y))
            #z_theta = degrees(asin((cam_size / 2) / z))

            #x = cam_size + ppos[0] - transform[0]
            #y = cam_size + ppos[1] - transform[1]
            #z = cam_size + ppos[2] - transform[2]
            #print('y pos: ', y)

            x, y, z = self.angular_transformation(angle[0], angle[1])

            #ray = [ppos, (x, y, z)]
            
            pos = ppos[:2]
            pygame.draw.line(self.main.display, (255, 0, 0), (pos[0], pos[1]), (pos[0] - x, pos[1] - y))
