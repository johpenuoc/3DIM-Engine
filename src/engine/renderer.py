import pygame
import json

import conf.config as conf


class Renderer:
    def __init__(self):
        # load the map
        self.map_data = []
        with open('src/game/map/map.json', 'r', encoding='utf-8') as j_file:
            self.map_data = json.load(j_file)
            j_file.close()

    def render(self, display, ppos, ray):
        pass
