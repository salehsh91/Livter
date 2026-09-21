import pygame as pyg
from texture import Texture
from conster import WIDTH,HEIGHT


class HUD:
    def __init__(self, display, API):
        self.display = display

        self.health = API["health"] // 10
        self.hungry = API["hungry"] // 10
        self.invertory = API["invertory"]
        self.maxslots = API["numslots"]

        self.invertoryOpened = True
        

        self.objsize = 10

        self.Healthtexture = Texture.health

        # فعلاً از همان تکسچر قلب برای گرسنگی استفاده می‌کنیم
        # بعداً می‌توانی Texture.hunger را جایگزین کنی
        self.Hungertexture = Texture.health

    def update(self, API):
        self.health = max(0, API["health"] // 10)
        self.hungry = max(0, API["hungry"] // 10)

    def draw(self):
        self.draw_health()
        self.draw_hunger()
        self.draw_invertory()

    def draw_health(self):
        x = 10 + self.objsize

        for i in range(int(self.health)):
            y = i * 12 + self.objsize

            self.display.blit(
                self.Healthtexture,
                (
                    int(x),
                    int(y)
                )
            )

    def draw_hunger(self):
        x = 30 + self.objsize

        for i in range(self.hungry):
            y = i * 12 + self.objsize

            self.display.blit(
                self.Hungertexture,
                (
                    int(x),
                    int(y)
                )
            )

    def draw_invertory(self):
        if not self.invertoryOpened:
            return

        slot_size = 50
        gap = 10
        columns = 6
        rows = (self.maxslots + columns - 1) // columns

        w = columns * (slot_size + gap)
        h = rows * (slot_size + gap)

        x = WIDTH - w - 20
        y = HEIGHT - int(h/columns) * gap-gap

        pyg.draw.rect(
            self.display,
            (50, 50, 50),
            (x, y, w, h)
        )
        for id, data in list(self.invertory.items()):
            item = data[0]
            count = data[1]

            col = (id - 1) % 6
            row = (id - 1) // 6

            slot_x = x + col * 60
            slot_y = y + row * 60

            pyg.draw.rect(
                self.display,
                (80, 80, 80),
                (slot_x, slot_y, 50, 50)
            )

            texture = pyg.transform.scale(
                item.texture,
                (40, 40)
            )

            self.display.blit(
                texture,
                (slot_x + 5, slot_y + 5)
            )

            if count > 1:
                font = pyg.font.Font(None, 20)
                text = font.render(
                    str(count),
                    True,
                    (255, 255, 255)
                )

                self.display.blit(
                    text,
                    (slot_x + 35, slot_y + 32)
                )

            

            

            