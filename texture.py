import os
import pygame as pyg
from conster import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")



def load_texture(name, fallback, alpha=False):
    try:
        image = pyg.image.load(
            os.path.join(ASSETS_DIR, name)
        )
        return image.convert_alpha() if alpha else image.convert()
    except:
        surface = pyg.Surface(
            (BLOCK_SIZE, BLOCK_SIZE),
            pyg.SRCALPHA if alpha else 0
        )
        surface.fill(fallback)
        return surface



class Texture:
    grass = pyg.transform.scale(
        load_texture("grass2.png", (34, 139, 34)),
        (BLOCK_SIZE, BLOCK_SIZE)
    )

    stone = pyg.transform.scale(
        load_texture("stone.png", (128, 128, 128)),
        (BLOCK_SIZE, BLOCK_SIZE)
    )

    water = pyg.transform.scale(
        load_texture("water2.png", (30, 144, 255)),
        (BLOCK_SIZE, BLOCK_SIZE)
    )

    sand = pyg.transform.scale(
        load_texture("sand2.png", (244, 164, 96)),
        (BLOCK_SIZE, BLOCK_SIZE)
    )

    plank = pyg.transform.scale(
        load_texture("plank.png", (244, 164, 96)),
        (BLOCK_SIZE, BLOCK_SIZE)
    )

    health = pyg.transform.scale(
            load_texture("health.png", (244, 0, 0),True),
            (10,10)
        )