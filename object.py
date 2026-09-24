import pygame as pyg
from conster import *
from blockitem import Block

class obj:
    objs = {}
    def __init__(self,x,y,objwidth=BLOCK_SIZE,objheight=BLOCK_SIZE,name="plank",offset_x=0,offset_y=0):

        
                

        self.world_x = offset_x + ((x-offset_x)//BLOCK_SIZE)*BLOCK_SIZE
        self.world_y = offset_y + ((y-offset_y)//BLOCK_SIZE)*BLOCK_SIZE

        self.width = objwidth
        self.height = objheight

        self.base_x = offset_x
        self.base_y = offset_y

        block = Block.getblock_status(name = name)
        self.texture = block.texture
        self.type = block.type
        self.name = block.name

        

        
        


    def create(self):
        for id, obj in self.objs.items():
            if self.world_x == obj.world_x and self.world_y == obj.world_y:
                return False

        self.id = len(self.objs) + 1
        self.objs[self.id] = self
        return True

    @classmethod
    def remove(cls,x,y,objwidth=BLOCK_SIZE,objheight=BLOCK_SIZE,name="plank",offset_x=0,offset_y=0):

        A_world_x = offset_x + ((x-offset_x)//BLOCK_SIZE)*BLOCK_SIZE
        A_world_y = offset_y + ((y-offset_y)//BLOCK_SIZE)*BLOCK_SIZE

        A_width = objwidth
        A_height = objheight

        A_base_x = offset_x
        A_base_y = offset_y

        block = Block.getblock_status(name = name)
        A_texture = block.texture
        A_type = block.type
        A_name = block.name

        for id, obj in cls.objs.items():
            if A_world_x == obj.world_x and A_world_y == obj.world_y:
                o = obj.name
                del cls.objs[id]
                return (True,o)

        
        return (False,None)

    
    def draw(self,display,bx,by):
        display.blit(self.texture,(self.world_x + bx,self.world_y +by))

    @classmethod
    def drawObjects(cls,display,bx,by):
        for id ,obj in cls.objs.items():
            obj.draw(display,bx,by)






