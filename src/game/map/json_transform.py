import json

from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SRC_DIR))

import conf.config as conf


with open('src/game/map/map.txt', 'r', encoding='utf-8') as file:
    f_data = file.read().split('\n')
    f_data = [i.replace(' ', '') for i in f_data]
    file.close()  

map_data = {}
TS = conf.TILE_SIZE
for y, row in enumerate(f_data):
    itt = list(row)
    for x, z in enumerate(itt):
         if int(z) != 0:
            pos = [x * TS, y * TS, int(z) * TS]
            map_data[f'{y} {x}'] = pos

with open('src/game/map/map.json', 'w', encoding='utf-8') as j_file:
    json.dump(map_data, j_file, indent=4)
    j_file.close()