import pygame as pyg
from conster import *
from blockitem import Block

class obj:
    objs = {}
    def __init__(self,x,y,width=BLOCK_SIZE,height=BLOCK_SIZE,name="plank"):

        self.world_x = x
        self.world_y = y

        self.width = width
        self.height = height

        block = Block.getblock_status(name = name)
        self.texture = block.texture
        self.type = block.type
        self.name = block.name

        self.id = len(self.objs)+1
        self.objs[self.id] = self

        


    def draw(self,display,bx,by):
        display.blit(self.texture,(self.world_x + bx,self.world_y +by))

    @classmethod
    def drawObjects(cls,display,bx,by):
        for id ,obj in cls.objs.items():
            obj.draw(display,bx,by)






