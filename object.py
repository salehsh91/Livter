import pygame as pyg
from conster import *
from blockitem import Block

class obj:
    objs = {}
    def __init__(self,x,y,z,objwidth=BLOCK_SIZE,objheight=BLOCK_SIZE,name="plank",offset_x=0,offset_y=0):

        
                

        self.world_x = offset_x + ((x-offset_x)//BLOCK_SIZE)*BLOCK_SIZE
        self.world_y = offset_y + ((y-offset_y)//BLOCK_SIZE)*BLOCK_SIZE
        self.world_z = z

        self.width = objwidth
        self.height = objheight
        self.length = 1

        self.base_x = offset_x
        self.base_y = offset_y

        block = Block.getblock_status(name = name)
        self.texture = block.texture
        self.type = block.type
        self.name = block.name

        

        
        


    def create(self):
        for id, obj in self.objs.items():
            if self.world_x == obj.world_x and self.world_y == obj.world_y and self.world_z == obj.world_z:
                return False

        self.id = (self.world_x,self.world_y,self.world_z)
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

    @classmethod
    def zblock(cls,x,y,playerz,playerl,offset_x,offset_y,autoGround):
        world_x = (
            offset_x
            + ((x - offset_x) // BLOCK_SIZE) * BLOCK_SIZE
        )

        world_y = (
            offset_y
            + ((y - offset_y) // BLOCK_SIZE) * BLOCK_SIZE
        )

        if autoGround:

            z = 1

            while True:

                occupied = False

                for object_ in cls.objs.values():

                    if (
                        object_.world_x == world_x
                        and object_.world_y == world_y
                        and object_.world_z == z
                    ):
                        occupied = True
                        break

                if not occupied:
                    return z

                z += 1

        return max(1, playerz - playerl)

    
    def draw(self, display, bx, by):
        # Shadow on the ground
        shadow_width = self.width
        shadow_height = max(6, self.height // 4)

        shadow = pyg.Surface(
            (shadow_width, shadow_height),
            pyg.SRCALPHA
        )

        pyg.draw.ellipse(
            shadow,
            (0, 0, 0, 80),
            shadow.get_rect()
        )

        display.blit(
            shadow,
            (
                self.world_x + bx,
                self.world_y + by + self.height - shadow_height // 2
            )
        )

        # Object
        display.blit(
            self.texture,
            (
                self.world_x + bx,
                self.world_y + by
            )
        )

    def draw(self, display, bx, by):
        # Shadow
        z_height = max(0, self.world_z - 1)

        shadow_width = max(
            4,
            int(self.width * (1 - z_height * 0.08))
        )

        shadow_height = max(
            3,
            int(self.height * 0.25 * (1 - z_height * 0.05))
        )

        shadow_alpha = max(
            25,
            int(80 - z_height * 8)
        )

        shadow = pyg.Surface(
            (shadow_width, shadow_height),
            pyg.SRCALPHA
        )

        pyg.draw.ellipse(
            shadow,
            (0, 0, 0, shadow_alpha),
            shadow.get_rect()
        )

        shadow_x = (
            self.world_x
            + bx
            + (self.width - shadow_width) / 2
        )

        shadow_y = (
            self.world_y
            + by
            + self.height
            - shadow_height / 2
            + z_height * 4
        )

        display.blit(
            shadow,
            (shadow_x, shadow_y)
        )

        # Object
        draw_y = (
            self.world_y
            + by
            
        )

        display.blit(
            self.texture,
            (
                self.world_x + bx,
                draw_y
            )
        )
    @classmethod
    def drawObjects(cls,display,bx,by):
        for id ,obj in cls.objs.items():
            obj.draw(display,bx,by)


    @classmethod
    def getObj(cls,world_x,world_y,world_z,offset_x=0,offset_y=0):
        x = offset_x + ((world_x-offset_x)//BLOCK_SIZE)*BLOCK_SIZE
        y = offset_y + ((world_y-offset_y)//BLOCK_SIZE)*BLOCK_SIZE
        return cls.objs.get((x,y,world_z))


            


    @classmethod
    def getObj3x3x3(cls, world_x, world_y, world_z, offset_x=0, offset_y=0):
        objs = []

        for xX in range(-1, 2):
            x = world_x + (xX * BLOCK_SIZE)

            for xY in range(-1, 2):
                y = world_y + (xY * BLOCK_SIZE)

                for xZ in range(-1, 2):
                    z = world_z + xZ

                    object_ = cls.getObj(
                        x,
                        y,
                        z,
                        offset_x,
                        offset_y
                    )

                    if object_ is not None:
                        startx = object_.world_x
                        starty = object_.world_y

                        lastx = object_.world_x + object_.width
                        lasty = object_.world_y + object_.height

                        objs.append([
                            startx,
                            starty,
                            lastx,
                            lasty,
                            object_.world_z,
                            object_.length
                        ])

        return objs
                

    @classmethod
    def getObjs(cls):
        return cls.objs






