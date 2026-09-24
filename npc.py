import pygame as pyg
import math
from conster import *
from blockitem import *
from object import obj
from blockitem import Item


class NPC:
    npcs = []

    def __init__(self, w, h, x, y, display, world,
                 color=COLORS["RED"], center=False, move=False):

        self.id = len(self.npcs) + 1
        self.color = color
        self.width = w
        self.height = h
        self.length = 2
        self.display = display

        self.realx = x
        self.realy = y

        self.world = world
        self.health = 100
        self.hungry = 100

        self.world_x = x
        self.world_y = y
        self.world_z = 1

        self.last_dx = 0
        self.last_dy = 0

        self.move = move

        self.dir_angle = 0
        self.camdir_angle = 0

        self.invertory = None

        self.rightHand = None
        self.Auto_Ground = True

        self.last_drap_time = 0
        self.drap_delay = 500  # میلی‌ثانیه

        self.npcs.append(self)

    def addinvertory(self, invertory):
        self.invertory = invertory

        self.invertory.add(
            Item.getitem_status(name="plank"),
            999
        )
        self.invertory.add(
            Item.getitem_status(name="stone"),
            999
        )

    def update(self, bManager):
        blocks = bManager.getblock(
            self.world_x,
            self.world_y,
            self.width,
            self.height
        )

        for key, block_type in blocks.items():
            if block_type == "water":
                self.health -= Block.getblock_status(
                    type=block_type
                ).damage
                break

    def getAPI(self, API):
        if API["move"]:
            rad = math.radians(API["dir"])

            dx = math.sin(rad)
            dy = -math.cos(rad)

            self.dir_angle = API["dir"]
            
        else:
            dx = 0
            dy = 0

        x = dx * NPC_SPEED
        y = dy * NPC_SPEED

        self.world_x += x
        self.world_y += y

        self.last_dx = x
        self.last_dy = y

        self.camdir_angle = API["cameradir"]
        now = pyg.time.get_ticks()

        if now - self.last_drap_time >= self.drap_delay:
            self.last_drap_time = now
            self.drap(API["drap"])
        



    def drap(self, drap):
        if self.invertory is None or drap == 0:
            return

        # پیدا کردن Slot فعال
        key = None

        for k, data in self.invertory.slots.items():
            if len(data) >= 3 and data[2] == True:
                key = k
                break

        if key is None:
            return

        slot = self.invertory.slots[key]

        self.rightHand = slot

        if len(slot) < 3:
            return

        item = slot[0]
        count = slot[1]
        active = slot[2]

        if count <= 0 or active == False:
            return

        # محاسبه محل قرار گرفتن/برداشتن Object
        x = WIDTH / 2
        y = HEIGHT / 2

        rad = math.radians(self.camdir_angle)

        end_x = x + math.sin(rad) * camdirline
        end_y = y - math.cos(rad) * camdirline

        

        w = item.block.w
        h = item.block.h

        base_x = self.world.base_x
        base_y = self.world.base_y

        world_x = end_x - self.world.bx
        world_y = end_y - self.world.by
        world_z = obj.zblock(world_x,world_y,self.world_z,self.length,base_x,base_y,self.Auto_Ground)

        # گذاشتن Object
        if drap >= 1:

            new_obj = obj(
                world_x,
                world_y,
                world_z,
                w,
                h,
                name=item.name,
                offset_x=base_x,
                offset_y=base_y
            )

            if new_obj.create():

                self.invertory.slots[key] = (
                    item,
                    count - 1,
                    active
                )

        # برداشتن Object
        elif drap <= -1:
            result = obj.remove(
                world_x,
                world_y,
                w,
                h,
                name=item.name,
                offset_x=base_x,
                offset_y=base_y)

            if result[0]:
                a = False
                i = Item.getitem_status(name=result[1])
                if slot[0] == i:
                    a = True

                self.invertory.add(i, 1 ,a)

        

        

    

    def getStatus(self, bManager):
        blocks = {}
        id = 0

        for nx in range(-10, 10):
            for ny in range(-10, 10):

                x = nx * BLOCK_SIZE + self.world_x
                y = ny * BLOCK_SIZE + self.world_y

                id += 1

                blocks[id] = bManager.getblock(
                    x,
                    y,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )

        return {
            "blocks": blocks,
            "invertory": self.invertory.slots,
            "numslots": self.invertory.slotnum,
            "health": self.health,
            "hungry": self.hungry,
            "x": self.world_x,
            "y": self.world_y,
            "cameradir": self.camdir_angle
        }

    def draw(self, display, bx, by):
        pyg.draw.rect(
            display,
            self.color,
            (
                self.world_x + bx,
                self.world_y + by,
                self.width,
                self.height
            )
        )

    

    @classmethod
    def drawNPC(cls):
        for npc in cls.npcs:
            pyg.draw.rect(
                npc.display,
                npc.color,
                (
                    npc.world_x + npc.world.bx,
                    npc.world_y + npc.world.by,
                    npc.width,
                    npc.height
                )
            )