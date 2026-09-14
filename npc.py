import pygame as pyg
from conster import *
from object import obj

class NPC:
    npcs = []
    def __init__(self,w,h,x,y,display,world,color = COLORS["RED"],center = False,move = False):
        self.id = len(self.npcs) + 1
        self.color = color
        self.width = w
        self.height = h
        self.display = display
        self.realx = x
        self.realy = y
        self.world = world

        self.health = 100
        self.hungry = 0
        
        self.world_x = x
        self.world_y = y

        self.last_dx = 0
        self.last_dy = 0

        self.move = move
        self.direction = (0,1)
        

        self.npcs.append(self)


    def getAPI(self,API):
        x = API["x"] * NPC_SPEED
        y = API["y"] * NPC_SPEED

        self.direction = (API["x"],API["y"])

        self.world_x += x
        self.world_y += y

        self.last_dx = x
        self.last_dy = y

        if API["drap"]:
            self.drap()
            

    def drap(self):
        x ,y = self.directionManager()
        obj1 = obj(x,y,name="plank")

    def update(self):
        # print(self.world.getblock(self.world_x,self.world_y,self.width,self.height))
        pass

    def directionManager(self):
        x = int((self.world_x + self.width/2 )// BLOCK_SIZE) * BLOCK_SIZE + 11
        y = int((self.world_y + self.height/2)// BLOCK_SIZE) * BLOCK_SIZE


        if self.direction == (1,0):
            x += BLOCK_SIZE
        elif self.direction == (-1,0):
            x -= BLOCK_SIZE
        elif self.direction == (0,1):
            y += BLOCK_SIZE
        elif self.direction == (0,-1):
            y -= BLOCK_SIZE

        
        return x,y

            
    def getStatus(self):
        status = {"health":self.health,"hungry":self.hungry,"x":self.world_x,"y":self.world_y}
        return status

    @classmethod
    def drawNPC(cls):
        for npc in cls.npcs:
            pyg.draw.rect(npc.display,npc.color,(npc.world_x + npc.world.bx, npc.world_y + npc.world.by, npc.width, npc.height))

    

class NPC_Contoroler:
    def __init__(self,up = pyg.K_w,down=pyg.K_s,left=pyg.K_a,right=pyg.K_d,drap=pyg.K_e,s = True):
        self.key_up = up
        self.key_down = down
        self.key_left = left
        self.key_right = right
        self.key_drap = drap
        self.s = s

    def getAPI(self,keys):
        x = 0
        y = 0
        drap = False
        
        if keys[self.key_up]: y -= 1
        if keys[self.key_down]: y+=1
        if keys[self.key_left]: x-=1
        if keys[self.key_right]: x+=1

        
        if keys[self.key_drap]:
            drap = True
        api = {'x': x, 'y': y, "drap":drap}

        if self.s:
            return api
