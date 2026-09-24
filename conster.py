import pygame as pyg

pyg.init()
info = pyg.display.Info()

WIDTH = info.current_w
HEIGHT = info.current_h

W_WORLD = 100
H_WORLD = 100

BLOCK_SIZE = 32
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