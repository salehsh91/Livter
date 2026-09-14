import pygame as pyg
from conster import *
from texture import *

class Block:
    blocks = [{"texture": Texture.water,"type": "water","name":"water"},{"texture": Texture.sand,"type": "sand","name":"sand"},{"texture": Texture.stone,"type": "stone","name":"stone"},{"texture": Texture.grass,"type": "grass","name":"grass"},{"texture": Texture.plank,"type": "plank","name":"plank"}]

    @classmethod
    def getblock_status(cls,texture=None,type=None,name=None):
        for block in cls.blocks:
            if texture != None:
                metod = "texture"
                metod2 = texture
            elif type != None:
                metod = "type"
                metod2 = type
            elif name != None:
                metod = "name"
                metod2 = name
            if block[metod] == metod2:
                findblock = block
                    
            

            
        return findblock
            



    