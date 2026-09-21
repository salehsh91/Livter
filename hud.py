import pygame as pyg
from texture import Texture


class HUD:
    def __init__(self, display, API):
        self.display = display

        self.health = API["health"] // 10
        self.hungry = API["hungry"] // 10

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

    def draw_health(self):
        x = 10 + self.objsize

        for i in range(self.health):
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