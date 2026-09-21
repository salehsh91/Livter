import pygame as pyg
from conster import *
from BlockManager import *
from npc import *
from contoroler import *
from object import *
from inventory import *


class World:
    def __init__(self, seed, display):
        self.npcs = {}
        self.player = None
        self.seed = seed
        self.display = display
        self.playerContoroler = None
        self.blockManager = BlocksWorld(seed)
        self.blockManager.create(self.display)

        self.npc_update_counter = 0
        self.npc_update_every = 15

        self.HUD = None

    def ev(self, ev):
        self.playerContoroler.update(ev)

    def update(self):
        self.blockManager.update_background_loading(self.display)

        for id, npc in self.npcs.items():
            data = npc[0]
            contoroler = npc[1]

            api = contoroler.getAPI(pyg.key.get_pressed())
            data.getAPI(api)

        if self.player:
            self.blockManager.move(
                -self.player.last_dx,
                self.player.last_dy
            )

        self.npc_update_counter += 1

        if self.npc_update_counter >= self.npc_update_every:
            self.npc_update_counter = 0
            self.updateNPC()
            self.updateHUD()

    def updateNPC(self):
        for key, npc in self.npcs.items():
            npc[0].update(self.blockManager)

    def draw(self):
        self.blockManager.drawBlocks(self.display)
        obj.drawObjects(
            self.display,
            self.blockManager.bx,
            self.blockManager.by
        )
        NPC.drawNPC()
        
        self.HUD.draw()
        self.playerContoroler.draw()

    def newNPC(self, w, h, x, y, color, contoroler=None,HUD=None,inventory = Invertory(), player=False):
        if contoroler is None:
            contoroler = Contoroler_Key()

        id = len(self.npcs) + 1
        npc = NPC(
            w,
            h,
            x,
            y,
            self.display,
            self.blockManager,
            color,
            True,
            player
        )

        npc.addinvertory(inventory)

        self.npcs[id] = (npc, contoroler,HUD,inventory)

        if player:
            self.player = npc

        return npc

    def newPlayer(self, w, h, x, y, color, contoroler=None):
        self.playerContoroler = contoroler
        return self.newNPC(
            w,
            h,
            x,
            y,
            color,
            contoroler,
            self.HUD,
            Invertory(),
            True
        )

    def getHUD(self,HUD):
        self.HUD = HUD

    def updateHUD(self):
        self.HUD.update(self.player.getStatus(self.blockManager))
            