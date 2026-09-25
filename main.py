import pygame as pyg
import random

from init import *
from world import *
from npc import *
from contoroler import *
from hud import *


running = True
playerContoroler = Contoroler_JoyStick(screen,200,HEIGHT-200)
playerContoroler = Contoroler_Key(screen)
seed = random.randint(0, 999999999)
print("seed:", seed)

world = World(seed, screen)

font = pyg.font.Font(None, 30)

player = world.newPlayer(
    50,
    50,
    WIDTH / 2-50/2,
    HEIGHT / 2-50/2,
    COLORS["RED"],
    playerContoroler
)

# for _ in range( 100):

#     world.newNPC(
#         50,
#         50,
#         WIDTH / 2 + 200,
#         HEIGHT / 2,
#         COLORS["BLUE"],
#         Contoroler_Key(
#             pyg.K_i,
#             pyg.K_k,
#             pyg.K_j,
#             pyg.K_l,
#             pyg.K_u
#         )
#     )

world.getHUD(HUD(screen, player.getStatus(world.blockManager)))

print("game started")

clock = pyg.time.Clock()

while running:

    for ev in pyg.event.get():

        if ev.type == pyg.QUIT:
            running = False

        if ev.type == pyg.KEYDOWN:
            if ev.key == pyg.K_ESCAPE:
                running = False

        world.ev(ev)

    world.update()

    screen.fill((0, 0, 0))

    if Render:
        world.draw()

        fps_text = font.render(
            str(int(clock.get_fps())),
            True,
            (0,0,0)
        )

        z_text = font.render(
                    f"playerZ: {player.world_z}",
                    True,
                    (0,0,0)
                )

        screen.blit(fps_text, (10, 10))
        screen.blit(z_text, (60, 10))


        pyg.display.update()

    clock.tick(60)

pyg.quit()