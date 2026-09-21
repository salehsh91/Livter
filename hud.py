import pygame as pyg
from texture import Texture
class HealthBar:
    def __init__(self,display,API):
        self.health = API["health"] // 10
        self.objsize = 10
        self.display = display
        self.Healthtexture = Texture.Healthtexture

    def update(self,API):
        self.health = API["health"] // 10

    def draw(self):
        x = 10 + self.objsize
        for i in range(self.health):
            y = i * 12 + self.objsize
            self.display.blit(self.Healthtexture,
                (
                    int(x),
                    int(y)
                ))

