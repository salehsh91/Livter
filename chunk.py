import pygame as pyg
from conster import *
from block import *

class Chunk:
    def __init__(self, chunk_x, chunk_y, chunk_size, block_size, world_offset_x, world_offset_y):
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.chunk_size = chunk_size
        self.block_size = block_size
        
        self.world_x = world_offset_x + chunk_x * chunk_size * block_size
        self.world_y = world_offset_y + chunk_y * chunk_size * block_size
        
        self.blocks = {}
        self.is_loaded = False
    
    def generate(self, noise_functions):
        """تولید بلوک‌ها با استفاده از نویز"""
        if self.is_loaded: return
        
        for local_x in range(self.chunk_size):
            for local_y in range(self.chunk_size):
                global_x = self.chunk_x * self.chunk_size + local_x
                global_y = self.chunk_y * self.chunk_size + local_y
                _, texture = noise_functions(global_x, global_y)
                block = Block.getblock_status(texture)
                self.blocks[(local_x, local_y)] = block
        
        self.is_loaded = True

    def set_blocks(self, blocks_dict):
        """جایگزینی مستقیم بلوک‌ها (برای چانک‌های فیک/آینه‌ای)"""
        self.blocks = blocks_dict
        self.is_loaded = True
    
    def draw(self, display, camera_x, camera_y):
        if not self.is_loaded: return

        screen_x = self.world_x + camera_x
        screen_y = self.world_y + camera_y
        
        chunk_w = self.chunk_size * self.block_size
        chunk_h = self.chunk_size * self.block_size

        if screen_x + chunk_w < 0 or screen_x > WIDTH or screen_y + chunk_h < 0 or screen_y > HEIGHT:
            return

        for (lx, ly), block in self.blocks.items():
            texture = block["texture"]
            # pyg.draw.rect(display,(255,0,0),(screen_x + lx * self.block_size,screen_y + ly * self.block_size,self.block_size,self.block_size),1)

            display.blit(texture, (screen_x + lx * self.block_size, screen_y + ly * self.block_size))