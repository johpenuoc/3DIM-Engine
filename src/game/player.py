import pygame

class Player:
    def __init__(self):
        # x, y, z
        self.pos = [0, 0, 0]
        # x, y bearings
        self.dir = [0, 0]

    def movement(self, dt):
        keys = pygame.key.get_pressed()
        self.pos[0] += (keys[pygame.K_d] - keys[pygame.K_a]) * dt
        self.pos[1] += (keys[pygame.K_s] - keys[pygame.K_w]) * dt

    def direction(self, dt):
        keys = pygame.key.get_pressed()
        self.dir[0] += ((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) % 360) * dt
        self.dir[1] += ((keys[pygame.K_DOWN] - keys[pygame.K_UP]) % 360) * dt