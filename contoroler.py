
import pygame as pyg
from conster import *
from Button import *
import math

# =========================================================
# Keyboard Controller
# =========================================================

class Contoroler_Key:

    def __init__(
        self,
        display,
        up=pyg.K_w,
        down=pyg.K_s,
        left=pyg.K_a,
        right=pyg.K_d,
        drap=pyg.K_q,
        undrap=pyg.K_e,
        debug=pyg.K_BACKSPACE
    ):

        self.key_up = up
        self.key_down = down
        self.key_left = left
        self.key_right = right

        self.key_drap = drap
        self.key_undrap = undrap
        self.key_debug = debug

        self.display = display

        self.cameradir = 0

        self.grond = False

        self.grondButton = Button(
            display,
            WIDTH - 140,
            10 + 45 + 10,
            130,
            45,
            "hand Grond"
        )

    def getAPI(self, keys):

        x = 0
        y = 0
        drap = 0
        debug = False

        if keys[self.key_up]:
            y -= 1

        if keys[self.key_down]:
            y += 1

        if keys[self.key_left]:
            x -= 1

        if keys[self.key_right]:
            x += 1

        if keys[self.key_drap]:
            drap = 1

        if keys[self.key_undrap]:
            drap = -1

        if keys[self.key_debug]:
            debug = True

        move = x != 0 or y != 0

        direction = (
            math.degrees(
                math.atan2(x, -y)
            )
            if move
            else 0
        )

        return {
            "dir": direction,
            "move": move,
            "cameradir": direction,
            "drap": drap,
            "debug": debug,
            "Ground": self.grond
        }

    def update(self, ev):

        self.grondButton.update(ev)

        self.grond = self.grondButton.is_pressed()

        # Ground should toggle, not stay pressed
        if ev.type == pyg.MOUSEBUTTONDOWN:

            if (
                ev.button == 1
                and self.grondButton.rect.collidepoint(ev.pos)
            ):

                self.grond = not self.grond
                self.grondButton.pressed = False

    def draw(self):

        self.grondButton.set_text(
            "Auto Grond"
            if self.grond
            else "hand Grond"
        )

        self.grondButton.draw()


# =========================================================
# Joystick Controller
# =========================================================

class Contoroler_JoyStick:

    def __init__(self, display, x, y):

        self.display = display

        # =================================================
        # Movement joystick
        # =================================================

        self.centerx = x
        self.centery = y

        self.x = x
        self.y = y

        self.radius1 = 120
        self.radius2 = 40

        self.active = False
        self.stick_finger = None

        self.dir = 0

        # =================================================
        # Ground
        # =================================================

        self.grond = False

        self.grondButton = Button(
            display,
            WIDTH - 140,
            10 + 45 + 10,
            130,
            45,
            "hand Grond"
        )

        # =================================================
        # Joy2
        # =================================================

        self.Joy2 = True

        self.Joy2Button = Button(
            display,
            WIDTH - 140,
            10 + 45 + 10 + 60,
            130,
            45,
            "Joy2 ON"
        )

        # =================================================
        # Camera joystick
        # =================================================

        self.cameracenterx = (
            display.get_width() - x
        )

        self.cameracentery = y

        self.camerax = self.cameracenterx
        self.cameray = self.cameracentery

        self.camera_active = False
        self.camera_finger = None

        self.cameradir = 0

        # =================================================
        # Drop
        # =================================================

        self.drap_center = (
            x + 250,
            y
        )

        self.drap_radius = 45

        self.drap_pressed = False
        self.drap_finger = None

        # =================================================
        # Pick Up
        # =================================================

        self.pickupButton = CButton(
            display,
            WIDTH - 440,
            HEIGHT-400,
            50,

            "P"
        )
        self.drapButton = CButton(
                    display,
                    440,
                    HEIGHT-400,
                    50,
        
                    "D"
                )

    # =====================================================
    # Update
    # =====================================================

    def update(self, ev):

        # =================================================
        # Buttons
        # =================================================

        self.grondButton.update(ev)
        self.Joy2Button.update(ev)
        self.pickupButton.update(ev)
        self.drapButton.update(ev)


        # Ground toggle
        if (
            ev.type == pyg.MOUSEBUTTONDOWN
            and ev.button == 1
        ):

            if self.grondButton.rect.collidepoint(ev.pos):

                self.grond = not self.grond

                self.grondButton.pressed = False

            elif self.Joy2Button.rect.collidepoint(ev.pos):

                self.Joy2 = not self.Joy2

                self.Joy2Button.pressed = False

                if not self.Joy2:

                    self.camera_active = False
                    self.camera_finger = None

                    self.camerax = (
                        self.cameracenterx
                    )

                    self.cameray = (
                        self.cameracentery
                    )

        # =================================================
        # Mouse
        # =================================================

        if ev.type == pyg.MOUSEBUTTONDOWN:

            if ev.button != 1:
                return

            mx, my = ev.pos

            # -------------------------
            # Movement
            # -------------------------

            stick_dist = math.hypot(
                mx - self.centerx,
                my - self.centery
            )

            if stick_dist <= self.radius1:

                self.active = True

                self._move_stick(
                    mx,
                    my
                )

            # -------------------------
            # Camera
            # -------------------------

            if self.Joy2:

                camera_dist = math.hypot(
                    mx - self.cameracenterx,
                    my - self.cameracentery
                )

                if camera_dist <= self.radius1:

                    self.camera_active = True

                    self._move_camera(
                        mx,
                        my
                    )

            # -------------------------
            # Drop
            # -------------------------

            

        # =================================================
        # Mouse release
        # =================================================

        elif ev.type == pyg.MOUSEBUTTONUP:

            if ev.button != 1:
                return

            self.active = False

            self.x = self.centerx
            self.y = self.centery

            self.camera_active = False

            self.camerax = self.cameracenterx
            self.cameray = self.cameracentery

            self.drap_pressed = False

        # =================================================
        # Mouse motion
        # =================================================

        elif ev.type == pyg.MOUSEMOTION:

            mx, my = ev.pos

            if self.active:

                self._move_stick(
                    mx,
                    my
                )

            if self.Joy2 and self.camera_active:

                self._move_camera(
                    mx,
                    my
                )

        # =================================================
        # Android finger down
        # =================================================

        elif ev.type == pyg.FINGERDOWN:

            mx = (
                ev.x *
                self.display.get_width()
            )

            my = (
                ev.y *
                self.display.get_height()
            )

            # -------------------------
            # Movement
            # -------------------------

            stick_dist = math.hypot(
                mx - self.centerx,
                my - self.centery
            )

            if (
                stick_dist <= self.radius1
                and self.stick_finger is None
            ):

                self.stick_finger = ev.finger_id
                self.active = True

                self._move_stick(
                    mx,
                    my
                )

            # -------------------------
            # Camera
            # -------------------------

            if self.Joy2:

                camera_dist = math.hypot(
                    mx - self.cameracenterx,
                    my - self.cameracentery
                )

                if (
                    camera_dist <= self.radius1
                    and self.camera_finger is None
                ):

                    self.camera_finger = ev.finger_id
                    self.camera_active = True

                    self._move_camera(
                        mx,
                        my
                    )

            # -------------------------
            # Drop
            # -------------------------

            drap_dist = math.hypot(
                mx - self.drap_center[0],
                my - self.drap_center[1]
            )

            if (
                drap_dist <= self.drap_radius
                and self.drap_finger is None
            ):

                self.drap_finger = ev.finger_id
                self.drap_pressed = True

        # =================================================
        # Android finger motion
        # =================================================

        elif ev.type == pyg.FINGERMOTION:

            mx = (
                ev.x *
                self.display.get_width()
            )

            my = (
                ev.y *
                self.display.get_height()
            )

            if ev.finger_id == self.stick_finger:

                self._move_stick(
                    mx,
                    my
                )

            if (
                self.Joy2
                and ev.finger_id == self.camera_finger
            ):

                self._move_camera(
                    mx,
                    my
                )

        # =================================================
        # Android finger up
        # =================================================

        elif ev.type == pyg.FINGERUP:

            if ev.finger_id == self.stick_finger:

                self.stick_finger = None
                self.active = False

                self.x = self.centerx
                self.y = self.centery

            if ev.finger_id == self.camera_finger:

                self.camera_finger = None
                self.camera_active = False

                self.camerax = (
                    self.cameracenterx
                )

                self.cameray = (
                    self.cameracentery
                )

            if ev.finger_id == self.drap_finger:

                self.drap_finger = None
                self.drap_pressed = False

    # =====================================================
    # Movement
    # =====================================================

    def _move_stick(self, mx, my):

        dx = mx - self.centerx
        dy = my - self.centery

        distance = math.hypot(
            dx,
            dy
        )

        if distance > self.radius1:

            dx = (
                dx / distance *
                self.radius1
            )

            dy = (
                dy / distance *
                self.radius1
            )

        self.x = self.centerx + dx
        self.y = self.centery + dy

        if distance > 5:

            self.dir = math.degrees(
                math.atan2(
                    dx,
                    -dy
                )
            )

    # =====================================================
    # Camera
    # =====================================================

    def _move_camera(self, mx, my):

        dx = mx - self.cameracenterx
        dy = my - self.cameracentery

        distance = math.hypot(
            dx,
            dy
        )

        if distance > self.radius1:

            dx = (
                dx / distance *
                self.radius1
            )

            dy = (
                dy / distance *
                self.radius1
            )

        self.camerax = (
            self.cameracenterx + dx
        )

        self.cameray = (
            self.cameracentery + dy
        )

        if distance > 5:

            self.cameradir = math.degrees(
                math.atan2(
                    dx,
                    -dy
                )
            )

    # =====================================================
    # API
    # =====================================================

    def getAPI(
        self,
        keys=None,
        ev=None
    ):

        dx = self.x - self.centerx
        dy = self.y - self.centery

        distance = math.hypot(
            dx,
            dy
        )

        move = (
            self.active
            and distance > 5
        )

        # Drop / Pick Up
        drap = 0

        if self.drapButton.is_pressed():

            drap = 1

        elif self.pickupButton.is_pressed():

            drap = -1

        return {
            "dir": self.dir,
            "move": move,

            # Joy2 ON:
            # camera joystick
            #
            # Joy2 OFF:
            # movement joystick
            "cameradir": (
                self.cameradir
                if self.Joy2
                else self.dir
            ),

            "drap": drap,

            "debug": False,

            "Ground": self.grond
        }

    # =====================================================
    # Draw
    # =====================================================

    def draw(self):

        # =================================================
        # Movement joystick
        # =================================================

        pyg.draw.circle(
            self.display,
            (200, 200, 200),
            (
                self.centerx,
                self.centery
            ),
            self.radius1
        )

        pyg.draw.circle(
            self.display,
            (20, 20, 20),
            (
                int(self.x),
                int(self.y)
            ),
            self.radius2
        )

        # =================================================
        # Camera joystick
        # =================================================

        if self.Joy2:

            pyg.draw.circle(
                self.display,
                (200, 200, 200),
                (
                    self.cameracenterx,
                    self.cameracentery
                ),
                self.radius1
            )

            pyg.draw.circle(
                self.display,
                (20, 20, 20),
                (
                    int(self.camerax),
                    int(self.cameray)
                ),
                self.radius2
            )

        # =================================================
        # Drop
        # =================================================

        

        # =================================================
        # Ground
        # =================================================

        self.grondButton.set_text(
            "Auto Grond"
            if self.grond
            else "hand Grond"
        )

        self.grondButton.draw()

        # =================================================
        # Joy2
        # =================================================

        self.Joy2Button.set_text(
            "Joy2 ON"
            if self.Joy2
            else "Joy2 OFF"
        )

        self.Joy2Button.draw()

        # =================================================
        # Pick Up
        # =================================================

        self.pickupButton.draw()
        self.drapButton.draw()

