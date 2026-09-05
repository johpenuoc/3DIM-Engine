import pygame
from math import sin, cos
import conf.config as conf

class Camera:
    def __init_(self, pos, dir):
        self.player_pos = pos
        self.player_dir = dir

        self.dim = [0, 0]
        self.rays = []

        # the camera works as such:
        #   the camera is a box projected onto a 3d plain
        #   the height of the camera box is taken by calcualting the opposite side;
        #   if a ray is shooting out at 0 degrees, parallel to the floor,
        #       then the fov is the angle from that ray downards and upwards (hence '* 2')
        #       so the ray length is the hypotenues and the fov is theta
        #   similarly, the width of the box is the same but on the other plain
        #   but because its a box, we know all sides are equal, so we only calculate one side length
        s = sin(conf.FOV) * conf.RAY_LEN * 2
        self.cam_size = s

    def initialise_rays(self):
        # TOTAL rays to outline a box:
        #   camera size + camera size - 1 + camera size - 1 + camera size - 2

        # these are all the boxes inside the outlines box ('s')
        total_box_outline_rays = (self.cam_size * 4) - 4
        total_box_fill_rays = [(total_box_outline_rays - (8 * i)) * (i + 1) for i in range(int(self.cam_size // 2) - 1)]
        if total_box_fill_rays[-1] == 8:
            total_box_fill_rays.append(1)
        sum_total_box_fill_rays = sum(total_box_fill_rays)

        scattering = sum_total_box_fill_rays // conf.RAY_DEN

        rays = []
        # the four corners (of the box outline) and center ray are always drawn to provide basic function
        top_left_x_axis = self.player_pos[0] - (sin(self.player_dir[0] - conf.FOV) * conf.RAY_LEN)
        top_left_y_axis = self.player_pos[1] - (cos(self.player_dir[1] - conf.FOV) * conf.RAY_LEN)
        top_left = [top_left_x_axis, top_left_y_axis]

        for box_size in total_box_fill_rays:
            for i in range(box_size // scattering):
                pass
