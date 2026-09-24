
import pygame as pyg
import math
from texture import Texture
from conster import WIDTH,HEIGHT,camdirline


class HUD:
    def __init__(self, display, API):
        self.display = display
        self.playerx = API["x"]
        self.playery = API["y"]
        self.health = API["health"] // 10
        self.hungry = API["hungry"] // 10
        self.invertory = API["invertory"]
        self.maxslots = API["numslots"]
        self.camdirangle = API["cameradir"]

        self.invertoryOpened = True
        self.linesizedir = camdirline
        self.objsize = 10
        self.Healthtexture = Texture.health
        self.Hungertexture = Texture.health

        self.inventory_button = pyg.Rect(
            WIDTH - 140,
            10,
            130,
            45
        )

        

    def update(self, API):
        self.health = max(0, API["health"] // 10)
        self.hungry = max(0, API["hungry"] // 10)
        self.playerx = API["x"]
        self.playery = API["y"]
        self.camdirangle = API["cameradir"]

    def update_event(self, ev):
        if ev.type == pyg.MOUSEBUTTONDOWN and ev.button == 1:

            if self.inventory_button.collidepoint(ev.pos):
                self.invertoryOpened = not self.invertoryOpened
                return

            if not self.invertoryOpened:
                return

            slot_size = 50
            gap = 10
            columns = 6
            rows = (self.maxslots + columns - 1) // columns

            w = columns * (slot_size + gap)
            h = rows * (slot_size + gap)

            x = WIDTH - w - 20
            y = HEIGHT - int(h / columns) * gap - gap

            for id in range(1, self.maxslots + 1):
                col = (id - 1) % 6
                row = (id - 1) // 6

                slot_x = x + col * 60
                slot_y = y + row * 60

                slot_rect = pyg.Rect(
                    slot_x,
                    slot_y,
                    50,
                    50
                )

                if slot_rect.collidepoint(ev.pos):
                    self.click_slot(id)
                    return

    def click_slot(self, id):
        
        if id not in self.invertory:
            return

        for key, data in self.invertory.items():
            self.invertory[key] = (
                data[0],
                data[1],
                key == id
            )

        

        # کاری که می‌خواهی با Slot انجام شود را اینجا بنویس

    def draw(self):
        self.draw_health()
        self.draw_hunger()
        self.draw_invertory()
        self.draw_inventory_button()
        self.draw_cameraDIR()

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
        y = HEIGHT - int(h / columns) * gap - gap

        pyg.draw.rect(
            self.display,
            (50, 50, 50),
            (x, y, w, h)
        )

        for id, data in list(self.invertory.items()):
            
            item = data[0]
            count = data[1]
            active = data[2] if len(data) > 2 else False

            col = (id - 1) % 6
            row = (id - 1) // 6

            slot_x = x + col * 60
            slot_y = y + row * 60

            if active == True:
                pyg.draw.rect(
                    self.display,
                    (255, 255, 0),
                    (slot_x, slot_y, 50, 50)
                )

            pyg.draw.rect(
                self.display,
                (80, 80, 80),
                (slot_x + 2, slot_y + 2, 46, 46)
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

    def draw_inventory_button(self):
        pyg.draw.rect(
            self.display,
            (70, 70, 70),
            self.inventory_button
        )

        font = pyg.font.Font(None, 25)

        text = font.render(
            "Inventory",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=self.inventory_button.center
        )

        self.display.blit(
            text,
            text_rect
        )

    def draw_cameraDIR(self):
        x = WIDTH / 2
        y = HEIGHT / 2

        rad = math.radians(self.camdirangle)

        end_x = x + math.sin(rad) * self.linesizedir
        end_y = y - math.cos(rad) * self.linesizedir

        pyg.draw.line(
            self.display,
            (255, 255, 255),
            (x, y),
            (end_x, end_y),
            2
        )


    
