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


        self.display_alpha = 255.0
        

        
        


    def create(self):
        for id, obj in self.objs.items():
            if self.world_x == obj.world_x and self.world_y == obj.world_y and self.world_z == obj.world_z:
                return False

        self.id = (self.world_x,self.world_y,self.world_z)
        self.objs[self.id] = self

        
        return True

    @classmethod
    def remove(cls, x, y, z, objwidth=BLOCK_SIZE, objheight=BLOCK_SIZE, name="plank", offset_x=0, offset_y=0, autogrand=False):

        A_world_x = offset_x + ((x - offset_x) // BLOCK_SIZE) * BLOCK_SIZE
        A_world_y = offset_y + ((y - offset_y) // BLOCK_SIZE) * BLOCK_SIZE

        if autogrand:
            # پیدا کردن بالاترین بلاک (بیشترین world_z) در همین ستون x,y
            target_id = None
            target_z = None

            for id_, o in cls.objs.items():
                if o.world_x == A_world_x and o.world_y == A_world_y:
                    if target_z is None or o.world_z > target_z:
                        target_z = o.world_z
                        target_id = id_

            if target_id is None:
                return (False, None)

            name_removed = cls.objs[target_id].name
            del cls.objs[target_id]
            return (True, name_removed)

        # حالت عادی: حذف بلاک دقیقاً در z مشخص‌شده
        for id_, o in cls.objs.items():
            if A_world_x == o.world_x and A_world_y == o.world_y and o.world_z == z:
                name_removed = o.name
                del cls.objs[id_]
                return (True, name_removed)

        return (False, None)

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

        return max(1, playerz - 1)

    
    

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






    FADE_MARGIN = BLOCK_SIZE * 1.5      # هرچقدر بزرگ‌تر، محدوده‌ی تشخیص وسیع‌تر
    FADE_SPEED = 0.09                 # هرچقدر کوچیک‌تر، محو شدن نرم‌تر (کندتر)
    FADE_MIN_ALPHA = 150                # کمترین شفافیت (۰ تا ۲۵۵)

    def draw(self, display, bx, by, player=None):
        # ---------- محاسبه‌ی هدف شفافیت ----------
        target_alpha = 255

        if player is not None:
            m = self.FADE_MARGIN

            overlap_x = (
                self.world_x - m < player.world_x + player.width
                and self.world_x + self.width + m > player.world_x
            )
            overlap_y = (
                self.world_y - m < player.world_y + player.height
                and self.world_y + self.height + m > player.world_y
            )

            if overlap_x and overlap_y and self.world_z > player.world_z:
                target_alpha = self.FADE_MIN_ALPHA

        # ---------- نرم کردن انتقال (لرپ) ----------
        self.display_alpha += (
            (target_alpha - self.display_alpha) * self.FADE_SPEED
        )

        alpha = int(self.display_alpha)

        # ---------- Shadow ----------
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
        shadow_alpha = int(shadow_alpha * (alpha / 255))

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

        # ---------- Object ----------
        draw_y = (
            self.world_y
            + by
        )

        self.texture.set_alpha(alpha)
        display.blit(
            self.texture,
            (
                self.world_x + bx,
                draw_y
            )
        )
        self.texture.set_alpha(255)