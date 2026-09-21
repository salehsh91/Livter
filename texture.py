import pygame as pyg
from conster import *

class Texture:
    try:
            
        grass = pyg.transform.scale(
            pyg.image.load(
                "assets/grass2.png"
            ).convert(),
            (BLOCK_SIZE ,BLOCK_SIZE)
        )

        stone = pyg.transform.scale(
            pyg.image.load(
                "assets/stone.png"
            ).convert(),
            (BLOCK_SIZE ,BLOCK_SIZE)
        )

        water = pyg.transform.scale(
            pyg.image.load(
                "assets/water2.png"
            ).convert(),
            (BLOCK_SIZE ,BLOCK_SIZE)
        )

        sand = pyg.transform.scale(
            pyg.image.load(
                "assets/sand2.png"
            ).convert(),
            (BLOCK_SIZE ,BLOCK_SIZE)
        )


        plank = pyg.transform.scale(
                    pyg.image.load(
                        "assets/plank.png"
                    ).convert(),
                    (BLOCK_SIZE ,BLOCK_SIZE)
                )

        Healthtexture = pyg.transform.scale(
                    pyg.image.load(
                        "assets/health.png"
                    ).convert_alpha(),
                    (10,10)
                )

    except:

        grass = pyg.Surface(
            (BLOCK_SIZE ,BLOCK_SIZE)
        )
        grass.fill(
            (34, 139, 34)
        )

        stone = pyg.Surface(
            (BLOCK_SIZE ,BLOCK_SIZE)
        )
        stone.fill(
            (128, 128, 128)
        )

        water = pyg.Surface(
            (BLOCK_SIZE ,BLOCK_SIZE)
        )
        water.fill(
            (30, 144, 255)
        )

        sand = pyg.Surface(
            (BLOCK_SIZE ,BLOCK_SIZE)
        )
        sand.fill(
            (244, 164, 96)
        )
        plank = pyg.Surface(
            (BLOCK_SIZE ,BLOCK_SIZE)
        )
        plank.fill(
            (244, 164, 96)
        )
        Healthtexture = pyg.Surface(
            (10,10)
        )
        Healthtexture.fill(
            (244, 0, 0)
        )