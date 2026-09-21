import pygame as pyg
import math
from conster import *
from blockitem import *
from object import obj


class NPC:
    npcs = []

    def __init__(self, w, h, x, y, display, world,
                 color=COLORS["RED"], center=False, move=False):

        self.id = len(self.npcs) + 1
        self.color = color
        self.width = w
        self.height = h
        self.display = display

        self.realx = x
        self.realy = y

        self.world = world
        self.health = 100
        self.hungry = 100

        self.world_x = x
        self.world_y = y

        self.last_dx = 0
        self.last_dy = 0

        self.move = move

        self.direction = (0, 1)
        self.dir_angle = 0

        self.invertory = None

        self.npcs.append(self)

    def addinvertory(self, invertory):
        self.invertory = invertory

        self.invertory.add(
            Item.getitem_status(name="plank"),
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
            self.direction = self._angle_to_discrete(API["dir"])
        else:
            dx = 0
            dy = 0

        x = dx * NPC_SPEED
        y = dy * NPC_SPEED

        self.world_x += x
        self.world_y += y

        self.last_dx = x
        self.last_dy = y

        if API["drap"]:
            self.drap()

    def _angle_to_discrete(self, angle):
        angle = angle % 360

        if angle >= 315 or angle < 45:
            return (0, -1)
        elif angle < 135:
            return (1, 0)
        elif angle < 225:
            return (0, 1)
        else:
            return (-1, 0)

    def drap(self):
        if self.invertory is None:
            return

        slot = self.invertory.slots.get(1)

        if slot is None:
            return

        item = slot[0]
        count = slot[1]

        if count <= 0:
            return

        x, y = self.directionManager()

        obj(
            x,
            y,
            name=item.name
        )

        self.invertory.slots[1] = (
            item,
            count - 1
        )

        if self.invertory.slots[1][1] <= 0:
            del self.invertory.slots[1]

    def directionManager(self):
        x = int(
            (self.world_x + self.width / 2) // BLOCK_SIZE
        ) * BLOCK_SIZE + 11

        y = int(
            (self.world_y + self.height / 2) // BLOCK_SIZE
        ) * BLOCK_SIZE

        if self.direction == (1, 0):
            x += BLOCK_SIZE
        elif self.direction == (-1, 0):
            x -= BLOCK_SIZE
        elif self.direction == (0, 1):
            y += BLOCK_SIZE
        elif self.direction == (0, -1):
            y -= BLOCK_SIZE

        return x, y

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
            "y": self.world_y
        }

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