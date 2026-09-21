import pygame as pyg
import math
from conster import *
from object import obj


class NPC:
    npcs = []

    def __init__(self, w, h, x, y, display, world, color=COLORS["RED"], center=False, move=False):
        self.id = len(self.npcs) + 1
        self.color = color
        self.width = w
        self.height = h
        self.display = display
        self.realx = x
        self.realy = y
        self.world = world

        self.health = 100
        self.hungry = 0

        self.world_x = x
        self.world_y = y

        self.last_dx = 0
        self.last_dy = 0

        self.move = move
        self.direction = (0, 1)   # جهت گسسته (بالا/پایین/چپ/راست) — برای directionManager
        self.dir_angle = 0        # زاویه‌ی خام (۰..۳۶۰)، اگه جای دیگه لازم شد

        self.npcs.append(self)


    def update(self,bManager):
        blocks = bManager.getblock(self.world_x,self.world_y,self.width,self.height)
        for key, type in blocks.items():
            if type == "water":
                self.health -= 1
            

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
        """
        زاویه‌ی پیوسته (۰..۳۶۰، ۰=بالا) رو به یکی از ۴ جهت گسسته
        تبدیل می‌کنه — چون directionManager فقط این ۴ حالت رو می‌شناسه.
        هر ۹۰ درجه یه ربع؛ مرزها رو ۴۵ درجه جابه‌جا کردیم که "بالا"
        دقیقاً وسط بازه‌ی خودش (۳۱۵..۴۵) بیفته.
        """
        angle = angle % 360
        if angle >= 315 or angle < 45:
            return (0, -1)   # بالا
        elif angle < 135:
            return (1, 0)    # راست
        elif angle < 225:
            return (0, 1)    # پایین
        else:
            return (-1, 0)   # چپ

    def drap(self):
        x, y = self.directionManager()
        obj1 = obj(x, y, name="plank")

    

    def directionManager(self):
        # ⚠️ یادآوری: این تابع هنوز همون دو باگ قبلی رو داره که جدا
        # باید حل بشن (گرید از base_x شروع نمی‌شه + آفست +11 نامتقارنه).
        # این‌جا فقط سازگاری با ورودی زاویه‌ای اضافه شده، نه رفع اون باگ‌ها.
        x = int((self.world_x + self.width / 2) // BLOCK_SIZE) * BLOCK_SIZE + 11
        y = int((self.world_y + self.height / 2) // BLOCK_SIZE) * BLOCK_SIZE

        if self.direction == (1, 0):
            x += BLOCK_SIZE
        elif self.direction == (-1, 0):
            x -= BLOCK_SIZE
        elif self.direction == (0, 1):
            y += BLOCK_SIZE
        elif self.direction == (0, -1):
            y -= BLOCK_SIZE

        return x, y

    def getStatus(self):
        return {"health": self.health, "hungry": self.hungry, "x": self.world_x, "y": self.world_y}

    @classmethod
    def drawNPC(cls):
        for npc in cls.npcs:
            pyg.draw.rect(
                npc.display, npc.color,
                (npc.world_x + npc.world.bx, npc.world_y + npc.world.by, npc.width, npc.height)
            )