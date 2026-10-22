
import ctypes
from conster import *
from blockitem import *


class Chunk:

    def __init__(
        self,
        chunk_x,
        chunk_y,
        chunk_size,
        block_size,
        world_offset_x,
        world_offset_y
    ):
        self.chunk_x = chunk_x
        self.chunk_y = chunk_y
        self.chunk_size = chunk_size
        self.block_size = block_size

        self.world_x = (
            world_offset_x
            + chunk_x * chunk_size * block_size
        )

        self.world_y = (
            world_offset_y
            + chunk_y * chunk_size * block_size
        )

        

        # Z → {"blocks": {}, "surface": Surface}
        self.blocksa = (ctypes.c_int32 * (chunk_size * chunk_size))
        self.blocks = self.blocksa()

        self.is_loaded = False

    # ==========================================
    # ساخت Surface یک لایه
    # ==========================================

    

    # ==========================================
    # Generate
    # ==========================================

    def generate(self, noise_functions):

        if self.is_loaded:
            return

        

        for local_x in range(self.chunk_size):

            for local_y in range(self.chunk_size):

                global_x = (
                    self.chunk_x * self.chunk_size
                    + local_x
                )

                global_y = (
                    self.chunk_y * self.chunk_size
                    + local_y
                )

                _, texture = noise_functions(
                    global_x,
                    global_y
                )

                block = 1
                # Block.getblock_status(
                #     texture
                # )

                self.blocks[
                    ( local_y*self.chunk_size+local_x)
                ] = block

                

        self.is_loaded = True

    # ==========================================
    # Set blocks
    # ==========================================

    def set_blocks(self, blocks_dict):

        self.blocks = blocks_dict
        self.is_loaded = True

    # ==========================================
    # Draw
    # ==========================================

    def draw(
        self,
        display,
        camera_x,
        camera_y
    ):

        if not self.is_loaded:
            return

        chunk_w = (
            self.chunk_size
            * self.block_size
        )

        chunk_h = (
            self.chunk_size
            * self.block_size
        )

        screen_x = self.world_x + camera_x
        screen_y = self.world_y + camera_y

        # اگر کل Chunk خارج صفحه است
        if (
            screen_x + chunk_w < 0
            or screen_x > WIDTH
            or screen_y + chunk_h < 0
            or screen_y > HEIGHT
        ):
            return

        # لایه‌ها را از پایین به بالا رسم کن
        for z in sorted(self.blocks):

            layer = self.blocks[z]

            surface = layer["surface"]

            display.blit(
                surface,
                (
                    screen_x,
                    screen_y - z * self.block_size
                )
            )