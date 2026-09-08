import pygame, sys
from math import sin, cos, degrees, asin, radians, sqrt, radians
import conf.config as conf

class Camera:
    def __init__(self, pos, dir):
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
        s = sin(radians(conf.FOV)) * conf.RAY_LEN * 2
        self.cam_size = s
        print('s', s * 4 - 4)


        # angular ray variables
        self.dir = [0, 0]
        self.ray = [0, 0]

    def angular_ray(self, win, dt):
        keys = pygame.key.get_pressed()
        d0 = (keys[pygame.K_d] - keys[pygame.K_a]) * 15 * dt
        d1 = (keys[pygame.K_s] - keys[pygame.K_w]) * 15 * dt

        self.dir[0] += d0 * 70 * dt
        self.dir[1] += d1 * 70 * dt
        self.dir[0] %= 360# * (d0 if d0 != 0 and abs(int(self.dir[0])) >= 360 else 1)
        self.dir[1] %= 360# * (d1 if d1 != 0 and abs(int(self.dir[1])) >= 360 else 1)


        x_theta = (self.ray[0] + self.dir[0]) % 360
        z_theta = (self.ray[1] + self.dir[1]) % 360

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
                z = self.pythag(x, y) + shift
                rays[str(shift)].append([
                    x, y, z
                ])

            # top right to bottom right
            _z = None
            for p in range(1, box_side_len + 1):
                p = p * conf.RAY_DEN

                y = conf.RAY_LEN
                z = self.pythag(x, y) + shift + p
                _z = z
                rays[str(shift)].append([
                    _x, y, z
                ])

            # bottom right to bottom left
            __x = None
            for p in range(1, box_side_len + 1):
                p = p * conf.RAY_DEN

                x = _x - p
                __x = x
                y = conf.RAY_LEN
                rays[str(shift)].append([
                    x, y, _z
                ])

            # bottom left to top left
            for p in range(1, box_side_len + 1):
                p = p * conf.RAY_DEN

                y = conf.RAY_LEN
                z = _z - p
                rays[str(shift)].append([
                    __x, y, z
                ])

        print(rays)


    def initialise_rays(self):
        # TOTAL rays to outline a box:
        #   camera size + camera size - 1 + camera size - 1 + camera size - 2

        # these are all the boxes inside the outlines box ('s')
        total_box_outline_rays = (self.cam_size * 4) - 4
        total_box_fill_rays = [(total_box_outline_rays - (8 * i)) * (i + 1) for i in range(int(self.cam_size // 2) - 1)]
        if total_box_fill_rays[-1] == 8:
            total_box_fill_rays.append(1)
        sum_total_box_fill_rays = sum(total_box_fill_rays)

        #scattering = sum_total_box_fill_rays // conf.RAY_DEN

        rays = []
        # the four corners (of the box outline) and center ray are always drawn to provide basic function
        ##top_left_x_axis = self.player_pos[0] - (sin(self.player_dir[0] - conf.FOV) * conf.RAY_LEN)
        ##top_left_y_axis = self.player_pos[1] - (cos(self.player_dir[1] - conf.FOV) * conf.RAY_LEN)
        ##top_left = [top_left_x_axis, top_left_y_axis]

        opp = self.cam_size / 2
        #reversing = False
        for box_size in total_box_fill_rays:
            ray_total = (sum_total_box_fill_rays / box_size) * conf.RAY_DEN

            # when we shoot the rays into the box inside the previous
            # we need to adjust the angle inwards slightly to point it
            # towards those inner points
            universal_starting_angle = degrees(asin(opp / conf.RAY_LEN))
            x_ang = self.player_dir[0] - universal_starting_angle
            y_ang = self.player_dir[1] - universal_starting_angle

            # this is moving across a square.
            # the first for loop points the ray along the top line of a square
            # starting from the top left and makes its way across
            # then it stops and works its way downwards instead
            # then at the bottom it goes left
            # the eventually up, to where it started
            # (p.s. not a single line of code here has even been ran, and i havent checked the maths
            # so tomorrow is probably going to be an absolute headache...)
            line_len = ray_total // 4
            box_side_len = box_size // 4
            for p in range(0, int(ray_total), int(ray_total // 4)):
                print(box_side_len - p)
                print(degrees(asin(box_side_len - p)))
                x_ang = self.player_dir[0] - degrees(asin((box_side_len - p)) / conf.RAY_LEN)
                rays.append([
                    self.player_pos[0] - (x_ang * conf.RAY_LEN),
                    self.player_pos[1] - (y_ang * conf.RAY_LEN)
                ])

            right_x_side = self.player_dir[0] - degrees(asin((box_side_len - line_len)) / conf.RAY_LEN)
            for p in range(0, ray_total, ray_total // 4):
                y_ang = self.player_dir[0] - degrees(asin((box_side_len - p)) / conf.RAY_LEN)
                rays.append([
                    self.player_pos[0] - (right_x_side * conf.RAY_LEN),
                    self.player_pos[1] - (y_ang * conf.RAY_LEN)
                ])

            bottom_y_side = self.player_dir[0] - degrees(asin((box_side_len - line_len)) / conf.RAY_LEN)
            x_ang = right_x_side
            for p in range(0, ray_total, ray_total // 4):
                x_ang = self.player_dir[0] - degrees(asin((p)) / conf.RAY_LEN)
                rays.append([
                    self.player_pos[0] - (x_ang * conf.RAY_LEN),
                    self.player_pos[1] - (bottom_y_side * conf.RAY_LEN)
                ])

            y_ang = bottom_y_side
            for p in range(0, ray_total, ray_total // 4):
                y_ang = self.player_dir[0] - degrees(asin((p)) / conf.RAY_LEN)
                rays.append([
                    self.player_pos[0] - (x_ang * conf.RAY_LEN),
                    self.player_pos[1] - (bottom_y_side * conf.RAY_LEN)
                ])

            # this keeps the opp 'opposite' within its camera size / 2 limit
            d = '''if opp > 0 and not reversing:
                opp -= 1
            else:
                opp += 1
                reversing = True
            if opp > self.cam_size / 2:
                reversing = False
                opp -= 2'''
            opp -= 1

cam = Camera([0, 0, 0], [0, 0])


win = pygame.display.set_mode((500, 500))
c = pygame.time.Clock()
dt = 0

while 1:
    dt = c.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((0, 0, 0))

    cam.angular_ray(win, dt)

    pygame.display.update()