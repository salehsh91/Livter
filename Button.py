import pygame as pyg


class Button:

    def __init__(
        self,
        display,
        x,
        y,
        width,
        height,
        text="Button",
        color=(70, 70, 70),
        pressed_color=(120, 120, 120),
        text_color=(255, 255, 255),
        font_size=25
    ):

        self.display = display

        self.rect = pyg.Rect(
            x,
            y,
            width,
            height
        )

        self.text = text

        self.color = color
        self.pressed_color = pressed_color
        self.text_color = text_color

        self.font = pyg.font.Font(
            None,
            font_size
        )

        self.pressed = False
        self.fingers = set()

    def update(self, ev):

        # Mouse
        if ev.type == pyg.MOUSEBUTTONDOWN:

            if ev.button == 1:

                if self.rect.collidepoint(ev.pos):

                    self.pressed = True

        elif ev.type == pyg.MOUSEBUTTONUP:

            if ev.button == 1:

                self.pressed = False

        # Android touch
        elif ev.type == pyg.FINGERDOWN:

            x = ev.x * self.display.get_width()
            y = ev.y * self.display.get_height()

            if self.rect.collidepoint((x, y)):

                self.fingers.add(ev.finger_id)

                self.pressed = True

        elif ev.type == pyg.FINGERUP:

            if ev.finger_id in self.fingers:

                self.fingers.remove(ev.finger_id)

            self.pressed = len(self.fingers) > 0

    def draw(self):

        color = (
            self.pressed_color
            if self.pressed
            else self.color
        )

        pyg.draw.rect(
            self.display,
            color,
            self.rect
        )

        text = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text.get_rect(
            center=self.rect.center
        )

        self.display.blit(
            text,
            text_rect
        )

    def is_pressed(self):

        return self.pressed

    def set_text(self, text):

        self.text = text


import pygame as pyg


class CButton:

    def __init__(
        self,
        display,
        x,
        y,
        radius,
        text="Button",
        color=(70, 70, 70),
        pressed_color=(120, 120, 120),
        text_color=(255, 255, 255),
        font_size=25
    ):
        self.display = display
        self.x = x
        self.y = y
        self.radius = radius

        self.text = text
        self.color = color
        self.pressed_color = pressed_color
        self.text_color = text_color

        self.font = pyg.font.Font(
            None,
            font_size
        )

        self.pressed = False
        self.fingers = set()

    def is_inside(self, x, y):
        dx = x - self.x
        dy = y - self.y

        return dx * dx + dy * dy <= self.radius * self.radius

    def update(self, ev):

        # Mouse
        if ev.type == pyg.MOUSEBUTTONDOWN:
            if ev.button == 1:
                if self.is_inside(*ev.pos):
                    self.pressed = True

        elif ev.type == pyg.MOUSEBUTTONUP:
            if ev.button == 1:
                self.pressed = False

        # Android touch
        elif ev.type == pyg.FINGERDOWN:
            x = ev.x * self.display.get_width()
            y = ev.y * self.display.get_height()

            if self.is_inside(x, y):
                self.fingers.add(ev.finger_id)
                self.pressed = True

        elif ev.type == pyg.FINGERUP:
            if ev.finger_id in self.fingers:
                self.fingers.remove(ev.finger_id)

            self.pressed = len(self.fingers) > 0

    def draw(self):

        color = (
            self.pressed_color
            if self.pressed
            else self.color
        )

        pyg.draw.circle(
            self.display,
            color,
            (self.x, self.y),
            self.radius
        )

        text = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text.get_rect(
            center=(self.x, self.y)
        )

        self.display.blit(
            text,
            text_rect
        )

    def is_pressed(self):
        return self.pressed

    def set_text(self, text):
        self.text = text