# import threading
import random
import ctypes
# from init import *
from world import *

# from npc import *
# from contoroler import *
# from hud import *
screen = None




running = True
# playerContoroler = Contoroler_JoyStick(None,200,HEIGHT-200)
# playerContoroler = Contoroler_Key(screen)
seed = random.randint(0, 999999999)
print("seed:", seed)

world = World(seed)

# font = pyg.font.Font(None, 30)

# player = world.newPlayer(
#     50,
#     50,
#     WIDTH / 2-50/2,
#     HEIGHT / 2-50/2,
#     COLORS["RED"],
#     playerContoroler
# )

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

# world.getHUD(HUD(screen, player.getStatus(world.blockManager)))

print("game started")

# cpp_thread = threading.Thread(target=GameLoop(GetRenderer(),GetWindow()),
#                               daemon=True)


Init()
LoadTexture(GetRenderer(),255,0,255,255,1)
renderer = GetRenderer()

LoadImageTexture(
    renderer,
    b"assets/grass.png",
    1
)

LoadImageTexture(
    renderer,
    b"assets/water.png",
    2
)

LoadImageTexture(
    renderer,
    b"assets/stone.png",
    3
)


running = 1
while running == 1:

    

    # world.update()

    # screen.fill((0, 0, 0))

    if Render:
        
        WIDTH,HEIGHT = getWinSize()
        
        running = world.draw()
        

Quit()

            # fps_text = font.render(
            #     str(int(clock.get_fps())),
            #     True,
            #     (0,0,0)
            # )

            # z_text = font.render(
            #             f"playerZ: {player.world_z}",
            #             True,
            #             (0,0,0)
            #         )

            # screen.blit(fps_text, (200, 10))
            # screen.blit(z_text, (60, 10))


            

        # clock.tick(60)

    # pyg.quit()

# logic_thread = threading.Thread(target=run(),
#                               daemon=True)
# cpp_thread.start()
# logic_thread.start()

# cpp_thread.join()