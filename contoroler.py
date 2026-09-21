import pygame as pyg
import math


class Contoroler_Key:
    def __init__(self, up=pyg.K_w, down=pyg.K_s, left=pyg.K_a, right=pyg.K_d, drap=pyg.K_e):
        self.key_up = up
        self.key_down = down
        self.key_left = left
        self.key_right = right
        self.key_drap = drap

    def getAPI(self, keys):
        x = 0
        y = 0
        drap = False
        if keys[self.key_up]:
            y -= 1
        if keys[self.key_down]:
            y += 1
        if keys[self.key_left]:
            x -= 1
        if keys[self.key_right]:
            x += 1

        if keys[self.key_drap]:
            drap = True

        move = x != 0 or y != 0
        dir = math.degrees(math.atan2(x, -y)) if move else 0

        return {"dir": dir, "move": move, "drap": drap}


class Contoroler_JoyStick:
    def __init__(self, display, x, y):
        self.display = display
        self.centerx = x
        self.centery = y
        self.x = x
        self.y = y
        self.radius1 = 120
        self.radius2 = 40
        self.active = False
        self.stick_finger = None

        # دکمه‌ی جدا برای drop
        self.drap_center = (x + 250, y)
        self.drap_radius = 45
        self.drap_pressed = False
        self.drap_finger = None

    def update(self, ev):
        # Mouse / Windows
        if ev.type == pyg.MOUSEBUTTONDOWN:
            mx, my = ev.pos

            stick_dist = math.hypot(mx - self.centerx, my - self.centery)
            if stick_dist <= self.radius1:
                self.active = True

            drap_dist = math.hypot(mx - self.drap_center[0], my - self.drap_center[1])
            if drap_dist <= self.drap_radius:
                self.drap_pressed = True

        elif ev.type == pyg.MOUSEBUTTONUP:
            if self.active:
                self.active = False
                self.x = self.centerx
                self.y = self.centery
            self.drap_pressed = False

        elif ev.type == pyg.MOUSEMOTION and self.active:
            mx, my = ev.pos
            self._move_stick(mx, my)

        # Android Multi-touch
        elif ev.type == pyg.FINGERDOWN:
            mx = ev.x * self.display.get_width()
            my = ev.y * self.display.get_height()

            stick_dist = math.hypot(mx - self.centerx, my - self.centery)
            if stick_dist <= self.radius1 and self.stick_finger is None:
                self.stick_finger = ev.finger_id
                self.active = True

            drap_dist = math.hypot(mx - self.drap_center[0], my - self.drap_center[1])
            if drap_dist <= self.drap_radius and self.drap_finger is None:
                self.drap_finger = ev.finger_id
                self.drap_pressed = True

        elif ev.type == pyg.FINGERMOTION:
            if ev.finger_id == self.stick_finger:
                mx = ev.x * self.display.get_width()
                my = ev.y * self.display.get_height()
                self._move_stick(mx, my)

        elif ev.type == pyg.FINGERUP:
            if ev.finger_id == self.stick_finger:
                self.stick_finger = None
                self.active = False
                self.x = self.centerx
                self.y = self.centery

            if ev.finger_id == self.drap_finger:
                self.drap_finger = None
                self.drap_pressed = False

    def _move_stick(self, mx, my):
        dx = mx - self.centerx
        dy = my - self.centery
        distance = math.hypot(dx, dy)

        if distance > self.radius1:
            dx = dx / distance * self.radius1
            dy = dy / distance * self.radius1

        self.x = self.centerx + dx
        self.y = self.centery + dy

    def getAPI(self, keys=None, ev=None):
        dx = self.x - self.centerx
        dy = self.y - self.centery
        distance = math.hypot(dx, dy)

        move = self.active and distance > 5
        dir = math.degrees(math.atan2(dx, -dy)) if move else 0

        return {"dir": dir, "move": move, "drap": self.drap_pressed}

    def draw(self):
        pyg.draw.circle(
            self.display,
            (200, 200, 200),
            (self.centerx, self.centery),
            self.radius1
        )

        pyg.draw.circle(
            self.display,
            (20, 20, 20),
            (int(self.x), int(self.y)),
            self.radius2
        )

        drap_color = (255, 110, 110) if self.drap_pressed else (150, 150, 150)

        pyg.draw.circle(
            self.display,
            drap_color,
            self.drap_center,
            self.drap_radius
        )