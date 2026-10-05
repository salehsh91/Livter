import pygame as pyg
import math

from texture import Texture
from conster import WIDTH, HEIGHT, camdirline


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
        self.Hungertexture = Texture.hungry

        self.inventory_button = pyg.Rect(
            WIDTH - 140,
            10,
            130,
            45
        )

        # تنظیمات Slot
        self.slot_size = 50
        self.slot_gap = 10
        self.slot_columns = 6

        self.inventory_x = 20
        self.inventory_y = 50

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(self, API):

        self.health = max(
            0,
            API["health"] // 10
        )

        self.hungry = max(
            0,
            API["hungry"] // 10
        )

        self.playerx = API["x"]
        self.playery = API["y"]

        self.camdirangle = API["cameradir"]

    # --------------------------------------------------
    # SLOT POSITION
    # --------------------------------------------------

    def get_slot_rect(self, id):

        col = (id - 1) % self.slot_columns
        row = (id - 1) // self.slot_columns

        slot_x = (
            self.inventory_x
            + col * (self.slot_size + self.slot_gap)
        )

        slot_y = (
            self.inventory_y
            + row * (self.slot_size + self.slot_gap)
        )

        return pyg.Rect(
            slot_x,
            slot_y,
            self.slot_size,
            self.slot_size
        )

    # --------------------------------------------------
    # INVENTORY SIZE
    # --------------------------------------------------

    def get_inventory_rect(self):

        rows = (
            self.maxslots + self.slot_columns - 1
        ) // self.slot_columns

        width = (
            self.slot_columns * self.slot_size
            + (self.slot_columns - 1) * self.slot_gap
        )

        height = (
            rows * self.slot_size
            + (rows - 1) * self.slot_gap
        )

        return pyg.Rect(
            self.inventory_x,
            self.inventory_y,
            width,
            height
        )

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    def update_event(self, ev):

        if ev.type == pyg.MOUSEBUTTONDOWN:

            if ev.button != 1:
                return

            # Inventory button
            if self.inventory_button.collidepoint(ev.pos):

                self.invertoryOpened = not self.invertoryOpened

                return

            # اگر Inventory بسته است
            if not self.invertoryOpened:
                return

            # بررسی Slotها
            for id in range(
                1,
                self.maxslots + 1
            ):

                slot_rect = self.get_slot_rect(id)

                if slot_rect.collidepoint(ev.pos):

                    self.click_slot(id)

                    return

    # --------------------------------------------------
    # SLOT CLICK
    # --------------------------------------------------

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

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self):

        self.draw_health()
        self.draw_hunger()
        self.draw_invertory()
        self.draw_inventory_button()
        self.draw_cameraDIR()

    # --------------------------------------------------
    # HEALTH
    # --------------------------------------------------

    def draw_health(self):

        y = self.objsize * 2

        for i in range(int(self.health)):

            x = (
                WIDTH / 2
                - self.objsize * 5
                + i * (12 + self.objsize)
            )

            self.display.blit(
                self.Healthtexture,
                (
                    int(x),
                    int(y)
                )
            )

    # --------------------------------------------------
    # HUNGER
    # --------------------------------------------------

    def draw_hunger(self):

        y = self.objsize * 5

        for i in range(self.hungry):

            x = (
                WIDTH / 2
                - self.objsize * 5
                + i * (12 + self.objsize)
            )

            self.display.blit(
                self.Hungertexture,
                (
                    int(x),
                    int(y)
                )
            )

    # --------------------------------------------------
    # INVENTORY
    # --------------------------------------------------

    def draw_invertory(self):

        if not self.invertoryOpened:
            return

        inventory_rect = self.get_inventory_rect()

        # پس زمینه Inventory
        pyg.draw.rect(
            self.display,
            (50, 50, 50),
            inventory_rect
        )

        # Slotها
        for id, data in list(
            self.invertory.items()
        ):

            # اگر ID از تعداد Slotها بیشتر بود
            if id < 1 or id > self.maxslots:
                continue

            item = data[0]
            count = data[1]

            if len(data) > 2:
                active = data[2]
            else:
                active = False

            # جای دقیق Slot
            slot_rect = self.get_slot_rect(id)

            slot_x = slot_rect.x
            slot_y = slot_rect.y

            # Slot فعال
            if active:

                pyg.draw.rect(
                    self.display,
                    (255, 255, 0),
                    slot_rect
                )

            # خود Slot
            pyg.draw.rect(
                self.display,
                (80, 80, 80),
                (
                    slot_x + 2,
                    slot_y + 2,
                    46,
                    46
                )
            )

            # Texture آیتم
            texture = pyg.transform.scale(
                item.texture,
                (40, 40)
            )

            self.display.blit(
                texture,
                (
                    slot_x + 5,
                    slot_y + 5
                )
            )

            # تعداد آیتم
            if count > 1:

                font = pyg.font.Font(
                    None,
                    20
                )

                text = font.render(
                    str(count),
                    True,
                    (255, 255, 255)
                )

                self.display.blit(
                    text,
                    (
                        slot_x + 35,
                        slot_y + 32
                    )
                )

    # --------------------------------------------------
    # INVENTORY BUTTON
    # --------------------------------------------------

    def draw_inventory_button(self):

        pyg.draw.rect(
            self.display,
            (70, 70, 70),
            self.inventory_button
        )

        font = pyg.font.Font(
            None,
            25
        )

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

    # --------------------------------------------------
    # CAMERA DIRECTION
    # --------------------------------------------------

    def draw_cameraDIR(self):

        x = WIDTH / 2
        y = HEIGHT / 2

        rad = math.radians(
            self.camdirangle
        )

        end_x = (
            x
            + math.sin(rad)
            * self.linesizedir
        )

        end_y = (
            y
            - math.cos(rad)
            * self.linesizedir
        )

        pyg.draw.line(
            self.display,
            (255, 255, 255),
            (x, y),
            (end_x, end_y),
            2
        )