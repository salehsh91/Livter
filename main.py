import pygame as pyg
import random
from init import *
from world import *
from npc import *
from hud import *




running = True

seed = random.randint(0, 999999999)
print("seed:", seed)

world = World(seed,screen)




player = world.newPlayer(
    50,
    50,
    WIDTH / 2,
    HEIGHT / 2,
    COLORS["RED"]
)

npc = world.newNPC(
    50,
    50,
    WIDTH / 2 + 200,
    HEIGHT / 2,
    COLORS["BLUE"],
    NPC_Contoroler(pyg.K_i,pyg.K_k,pyg.K_j,pyg.K_l,pyg.K_u)
)

healthbar = HealthBar(screen,player.getStatus())
print("game started")
clock = pyg.time.Clock()

while running:
    for ev in pyg.event.get():
        if ev.type == pyg.QUIT:
            running = False
        if ev.type == pyg.KEYDOWN:
            if ev.key == pyg.K_ESCAPE:
                running = False
    
    

    
    world.update()
    healthbar.update(player.getStatus())
    
    screen.fill((0, 0, 0)) # پس زمینه مشکی تا پرش‌ها دیده نشوند
    
    world.draw()
    healthbar.draw()
    
    
    pyg.display.update()
    clock.tick(60)

pyg.quit()