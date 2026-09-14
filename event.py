import pygame as pyg

def eventManager(ev,world):
    if ev.type == pyg.KEYDOWN:
        print(ev.key)
        if ev.key == pyg.K_w:
            world.move(0,+5)
        elif ev.key == pyg.K_s:
            world.move(0,-5)
        elif ev.key == pyg.K_d:
            world.move(+5,0)
        elif ev.key == pyg.K_a:
            world.move(-5,0)
            

