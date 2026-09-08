import pygame
from math import sin, cos, degrees, asin, radians, sqrt
import conf.config as conf

class Camera:
    def __init__(self):
        #self.rays = {}

        # the camera works as such:
        #   the camera is a box projected onto a 3d plain
        #   the height of the camera box is taken by calcualting the opposite side;
        #   if a ray is shooting out at 0 degrees, parallel to the floor,
        #       then the fov is the angle from that ray downards and upwards (hence '* 2')
        #       so the ray length is the hypotenues and the fov is theta
        #   similarly, the width of the box is the same but on the other plain
        #   but because its a box, we know all sides are equal, so we only calculate one side length
        s = sin(radians(conf.FOV)) * conf.RAY_LEN * 2
        self.cam_size = s

    def angle_rays(self):
        total_box_outline_rays = (self.cam_size * 4) - 4
        line_den = (self.cam_size * 2) / conf.RAY_DEN
        angle_jump = int(self.cam_size / line_den)

        init_angle = 360 - (conf.FOV / 2)
        z_theta = init_angle

        #print(self.cam_size, line_den, angle_jump)

        rays = []
        for _ in range(int(self.cam_size)):
            x_theta = init_angle
            for i in range(int(line_den)):
                x_theta += angle_jump
                x_theta %= 360

                rays.append([x_theta, z_theta])

            z_theta += 1
            z_theta %= 360
            
        return rays