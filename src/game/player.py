import pygame

class Player:
    def __init__(self):
        # x, y, z
        self.pos = [0, 0]
        # x, y bearings
        self.dir = [0, 0]

    def movement(self, dt):
        keys = pygame.key.get_pressed()
        self.pos[0] += (keys[pygame.K_d] - keys[pygame.K_a]) * dt
        self.pos[1] += (keys[pygame.K_s] - keys[pygame.K_w]) * dt

    def direction(self, dt):
        keys = pygame.key.get_pressed()
        d0 = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        d1 = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.dir[0] += d0 * 70 * dt
        self.dir[1] += d1 * 70 * dt
        self.dir[0] %= 360 * (d0 if d0 != 0 and abs(self.dir[0]) >= 360 else 1)
        self.dir[1] %= 360 * (d1 if d1 != 0 and abs(self.dir[1]) >= 360 else 1)

    def update(self, dt):
        self.movement(dt)
        self.direction(dt)

        print(f'pos: {self.pos[:2]} | dir: {self.dir}')