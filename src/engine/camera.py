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

    def pythag(self, a, b):
        return sqrt((a**2 + b**2))
    
    def collect_rays(self):
        # these are all the boxes inside the outlines box ('s')
        total_box_outline_rays = (self.cam_size * 4) - 4
        total_box_fill_rays = [total_box_outline_rays - (8 * i) for i in range(int(self.cam_size // 2) - 1)]
        if total_box_fill_rays[-1] == 8:
            total_box_fill_rays.append(1) 

        rays = {}

        for shift, total_points in enumerate(total_box_fill_rays):
            total_rays = total_points / conf.RAY_DEN
            jump = conf.RAY_DEN
            box_side_len = int(total_points / (4 * conf.RAY_DEN))

            rays[str(shift)] = []

            # top left to top right
            _x = None
            #print(shift, box_side_len)
            for p in range(1, box_side_len + 1):
                p = p * conf.RAY_DEN

                x = (self.cam_size / 2) + shift + p
                _x = x
                y = conf.RAY_LEN
                z = self.pythag(self.pythag(x, y), (self.cam_size / 2) + shift)

                z_adj = self.pythag(x, y)
                x_theta = degrees(asin(x / z_adj))
                z_theta = degrees(asin(z_adj / z))

                rays[str(shift)].append([
                    x, y, z, [x_theta, z_theta]
                ])

            # top right to bottom right
            _z = None
            for p in range(1, box_side_len + 1):
                p = p * conf.RAY_DEN

                y = conf.RAY_LEN
                z = self.pythag(self.pythag(_x, y), (self.cam_size / 2) + shift + p)
                _z = z

                z_adj = self.pythag(_x, y)
                x_theta = degrees(asin(_x / z_adj))
                z_theta = degrees(asin(z_adj / z))
                rays[str(shift)].append([
                    _x, y, z, [x_theta, z_theta]
                ])

            # bottom right to bottom left
            __x = None
            for p in range(1, box_side_len + 1):
                p = p * conf.RAY_DEN

                x = _x - p
                __x = x
                y = conf.RAY_LEN

                z_adj = self.pythag(x, y)
                x_theta = degrees(asin(x / z_adj))
                z_theta = degrees(asin(z_adj / _z))

                rays[str(shift)].append([
                    x, y, _z, [x_theta, z_theta]
                ])

            # bottom left to top left
            for p in range(1, box_side_len + 1):
                p = p * conf.RAY_DEN

                y = conf.RAY_LEN
                z = _z - p

                z_adj = self.pythag(__x, y)
                x_theta = degrees(asin(__x / z_adj))
                z_theta = degrees(asin(z_adj / z))
                
                rays[str(shift)].append([
                    __x, y, z, [x_theta, z_theta]
                ])

        return rays