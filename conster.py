import pygame as pyg

pyg.init()
info = pyg.display.Info()

Render = True

WIDTH = info.current_w
HEIGHT = info.current_h


def size(num ,type = "x"):
    if type == "x":
        max = WIDTH
    else:
        max = HEIGHT

    return int(max * (num/100))

W_WORLD = 100
H_WORLD = 100

BLOCK_SIZE = size(2.5,"x")
NPC_SPEED = 1
CAMERA_SPEED = 1

camdirline = 50

FPS = 60

TITLE = "Livter Game"

COLORS ={
    "BLACK" :(0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0,255,0),
    "BLUE": (0,0,255),
    "ORANGE": (230,117,5),
    "BACKGROUND": (184,91,33)
    }