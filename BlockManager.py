import pygame as pyg
from mynoise import OpenSimplex

from worldchunk import Chunk
from conster import *
from texture import *


class BlocksWorld:

    speedCamera = CAMERA_SPEED
    CHUNK_SIZE = 16

    def __init__(self, seed):

        self.seed = seed

        # =====================================
        # World Size
        # =====================================

        self.w = W_WORLD
        self.h = H_WORLD

        # تعداد Chunkهای Real
        self.num_chunks_x = (
            self.w + self.CHUNK_SIZE - 1
        ) // self.CHUNK_SIZE

        self.num_chunks_y = (
            self.h + self.CHUNK_SIZE - 1
        ) // self.CHUNK_SIZE

        # =====================================
        # Block Size
        # =====================================

        self.bw = BLOCK_SIZE
        self.bh = BLOCK_SIZE

        # =====================================
        # Camera
        # =====================================

        self.bx = 0
        self.by = 0

        # =====================================
        # اندازه واقعی World بر اساس Chunk
        # =====================================

        self.real_world_width = (
            self.num_chunks_x
            * self.CHUNK_SIZE
            * self.bw
        )

        self.real_world_height = (
            self.num_chunks_y
            * self.CHUNK_SIZE
            * self.bh
        )

        # =====================================
        # مرکز کردن Real World
        # =====================================

        self.base_x = (
            WIDTH / 2
            - self.real_world_width / 2
        )

        self.base_y = (
            HEIGHT / 2
            - self.real_world_height / 2
        )

        # =====================================
        # Chunk Loading
        # =====================================

        self.margin_chunks = 2

        # تمام Chunkها
        self.Chunks = {}

        # فقط Chunkهای Real
        self.RealChunks = {}

        # =====================================
        # Textures
        # =====================================

        self.texture()

        # =====================================
        # Noise
        # =====================================

        self.elevation_noise = OpenSimplex(
            seed=self.seed
        )

        self.river_noise = OpenSimplex(
            seed=self.seed + 2000
        )

        # =====================================
        # Background Loading
        # =====================================

        self.last_chunk_load_time = 0
        self.background_loader_index = 0

    # ==================================================
    # Noise
    # ==================================================

    def get_noise_val(
        self,
        x,
        y,
        gen,
        scale
    ):

        return (
            gen.noise2(
                x / scale,
                y / scale
            ) + 1
        ) / 2

    # ==================================================
    # Block Type
    # ==================================================

    def determine_block_type(
        self,
        x,
        y
    ):

        elev = self.get_noise_val(
            x,
            y,
            self.elevation_noise,
            150.0
        )

        river = abs(
            self.river_noise.noise2(
                x / 80.0,
                y / 80.0
            )
        )

        if river < 0.08:
            return "water", self.water

        if elev < 0.35:
            return "water", self.water

        if elev < 0.40:
            return "sand", self.sand

        if elev > 0.65:
            return "stone", self.stone

        return "grass", self.grass

    # ==================================================
    # Create
    # ==================================================

    def create(self, display):

        print("Loading initial chunks...")

        # ==============================================
        # Real World
        # ==============================================

        for key in self.get_real_visible_chunks():

            self.load_chunk(key)

        # ==============================================
        # ذخیره Realها
        # ==============================================

        self.RealChunks = self.Chunks.copy()

        # ==============================================
        # چهار طرف
        # ==============================================

        directions = [
            "up",
            "down",
            "right",
            "left"
        ]

        for direction in directions:

            self.faketoreal(direction)

        # ==============================================
        # چهار گوشه
        # ==============================================

        corners = [
            "up_right",
            "up_left",
            "down_right",
            "down_left"
        ]

        for corner in corners:

            self.faketoreal(corner)

        print("Initial load done!")

    # ==================================================
    # Real Visible Chunks
    # ==================================================

    def get_real_visible_chunks(self):

        chunk_w = (
            self.CHUNK_SIZE
            * self.bw
        )

        chunk_h = (
            self.CHUNK_SIZE
            * self.bh
        )

        start_cx = int(
            (-self.base_x - self.bx)
            // chunk_w
        ) - self.margin_chunks

        end_cx = int(
            (WIDTH - self.base_x - self.bx)
            // chunk_w
        ) + self.margin_chunks + 1

        start_cy = int(
            (-self.base_y - self.by)
            // chunk_h
        ) - self.margin_chunks

        end_cy = int(
            (HEIGHT - self.base_y - self.by)
            // chunk_h
        ) + self.margin_chunks + 1

        visible = []

        for cx in range(
            start_cx,
            end_cx
        ):

            for cy in range(
                start_cy,
                end_cy
            ):

                if (
                    0 <= cx < self.num_chunks_x
                    and
                    0 <= cy < self.num_chunks_y
                ):

                    visible.append(
                        (cx, cy)
                    )

        return visible

    # ==================================================
    # All Visible Chunks
    # ==================================================

    def get_visible_chunks(self):

        chunk_w = (
            self.CHUNK_SIZE
            * self.bw
        )

        chunk_h = (
            self.CHUNK_SIZE
            * self.bh
        )

        start_cx = int(
            (-self.base_x - self.bx)
            // chunk_w
        ) - self.margin_chunks

        end_cx = int(
            (WIDTH - self.base_x - self.bx)
            // chunk_w
        ) + self.margin_chunks + 1

        start_cy = int(
            (-self.base_y - self.by)
            // chunk_h
        ) - self.margin_chunks

        end_cy = int(
            (HEIGHT - self.base_y - self.by)
            // chunk_h
        ) + self.margin_chunks + 1

        visible = []

        for cx in range(
            start_cx,
            end_cx
        ):

            for cy in range(
                start_cy,
                end_cy
            ):

                # ======================================
                # Real
                # ======================================

                is_real = (
                    0 <= cx < self.num_chunks_x
                    and
                    0 <= cy < self.num_chunks_y
                )

                # ======================================
                # Up
                # ======================================

                is_up_fake = (
                    0 <= cx < self.num_chunks_x
                    and
                    -self.num_chunks_y <= cy < 0
                )

                # ======================================
                # Down
                # ======================================

                is_down_fake = (
                    0 <= cx < self.num_chunks_x
                    and
                    self.num_chunks_y
                    <= cy
                    <
                    self.num_chunks_y * 2
                )

                # ======================================
                # Left
                # ======================================

                is_left_fake = (
                    -self.num_chunks_x
                    <= cx
                    < 0
                    and
                    0 <= cy < self.num_chunks_y
                )

                # ======================================
                # Right
                # ======================================

                is_right_fake = (
                    self.num_chunks_x
                    <= cx
                    <
                    self.num_chunks_x * 2
                    and
                    0 <= cy < self.num_chunks_y
                )

                # ======================================
                # Up Left
                # ======================================

                is_up_left_fake = (
                    -self.num_chunks_x
                    <= cx
                    < 0
                    and
                    -self.num_chunks_y
                    <= cy
                    < 0
                )

                # ======================================
                # Up Right
                # ======================================

                is_up_right_fake = (
                    self.num_chunks_x
                    <= cx
                    <
                    self.num_chunks_x * 2
                    and
                    -self.num_chunks_y
                    <= cy
                    < 0
                )

                # ======================================
                # Down Left
                # ======================================

                is_down_left_fake = (
                    -self.num_chunks_x
                    <= cx
                    < 0
                    and
                    self.num_chunks_y
                    <= cy
                    <
                    self.num_chunks_y * 2
                )

                # ======================================
                # Down Right
                # ======================================

                is_down_right_fake = (
                    self.num_chunks_x
                    <= cx
                    <
                    self.num_chunks_x * 2
                    and
                    self.num_chunks_y
                    <= cy
                    <
                    self.num_chunks_y * 2
                )

                # ======================================
                # Add
                # ======================================

                if (
                    is_real
                    or is_up_fake
                    or is_down_fake
                    or is_left_fake
                    or is_right_fake
                    or is_up_left_fake
                    or is_up_right_fake
                    or is_down_left_fake
                    or is_down_right_fake
                ):

                    visible.append(
                        (cx, cy)
                    )

        return visible

    # ==================================================
    # Load Chunk
    # ==================================================

    def load_chunk(
        self,
        key,
        blocks1=None,
        fake=False
    ):

        if blocks1 is None:

            blocks1 = {}

        if (
            key in self.Chunks
            and
            self.Chunks[key].is_loaded
        ):

            return

        cx, cy = key

        chunk = Chunk(
            cx,
            cy,
            self.CHUNK_SIZE,
            self.bw,
            self.base_x,
            self.base_y
        )

        # ==============================================
        # Fake Chunk
        # ==============================================

        if fake:

            chunk.set_blocks(
                blocks1
            )

        # ==============================================
        # Real Chunk
        # ==============================================

        else:

            chunk.generate(
                self.determine_block_type
            )

        self.Chunks[key] = chunk

    # ==================================================
    # Create Fake World
    # ==================================================

    def faketoreal(self, type):

        # فقط Realها
        real_chunks = list(
            self.RealChunks.items()
        )

        for keyc, chunk in real_chunks:

            cx, cy = keyc

            # ==========================================
            # Fake Chunk Position
            # ==========================================

            if type == "up":

                new_keyc = (
                    cx,
                    -cy - 1
                )

            elif type == "down":

                new_keyc = (
                    cx,
                    self.num_chunks_y * 2
                    - cy
                    - 1
                )

            elif type == "right":

                new_keyc = (
                    self.num_chunks_x * 2
                    - cx
                    - 1,
                    cy
                )

            elif type == "left":

                new_keyc = (
                    -cx - 1,
                    cy
                )

            # ==========================================
            # Up Right
            # ==========================================

            elif type == "up_right":

                new_keyc = (
                    self.num_chunks_x * 2
                    - cx
                    - 1,

                    -cy - 1
                )

            # ==========================================
            # Up Left
            # ==========================================

            elif type == "up_left":

                new_keyc = (
                    -cx - 1,
                    -cy - 1
                )

            # ==========================================
            # Down Right
            # ==========================================

            elif type == "down_right":

                new_keyc = (
                    self.num_chunks_x * 2
                    - cx
                    - 1,

                    self.num_chunks_y * 2
                    - cy
                    - 1
                )

            # ==========================================
            # Down Left
            # ==========================================

            elif type == "down_left":

                new_keyc = (
                    -cx - 1,

                    self.num_chunks_y * 2
                    - cy
                    - 1
                )

            else:

                continue

            # ==========================================
            # اگر قبلاً وجود دارد
            # ==========================================

            if new_keyc in self.Chunks:

                continue

            # ==========================================
            # Mirror Blocks
            # ==========================================

            bl = {}

            for keyb, block in chunk.blocks.items():

                texture = block["texture"]
                bx, by = keyb

                new_keyb = self.getAlgoritm(
                    type,
                    bx,
                    by
                )

                bl[new_keyb] = block

            # ==========================================
            # ساخت Fake
            # ==========================================

            self.load_chunk(
                new_keyc,
                bl,
                True
            )

            print(
                f"Load Fake {type}: "
                f"{keyc} -> {new_keyc}"
            )

    # ==================================================
    # Block Mirror Algorithm
    # ==================================================

    def getAlgoritm(
        self,
        type,
        bx,
        by
    ):

        S = self.CHUNK_SIZE

        # ==============================================
        # Up
        # ==============================================

        if type == "up":

            return (
                bx,
                S - by - 1
            )

        # ==============================================
        # Down
        # ==============================================

        elif type == "down":

            return (
                bx,
                S - by - 1
            )

        # ==============================================
        # Right
        # ==============================================

        elif type == "right":

            return (
                S - bx - 1,
                by
            )

        # ==============================================
        # Left
        # ==============================================

        elif type == "left":

            return (
                S - bx - 1,
                by
            )

        # ==============================================
        # Up Right
        # ==============================================

        elif type == "up_right":

            return (
                S - bx - 1,
                S - by - 1
            )

        # ==============================================
        # Up Left
        # ==============================================

        elif type == "up_left":

            return (
                S - bx - 1,
                S - by - 1
            )

        # ==============================================
        # Down Right
        # ==============================================

        elif type == "down_right":

            return (
                S - bx - 1,
                S - by - 1
            )

        # ==============================================
        # Down Left
        # ==============================================

        elif type == "down_left":

            return (
                S - bx - 1,
                S - by - 1
            )

        return (
            bx,
            by
        )

    # ==================================================
    # Background Loading
    # ==================================================

    def update_background_loading(
        self,
        display
    ):

        if (
            pyg.time.get_ticks()
            -
            self.last_chunk_load_time
            > 50
        ):

            self.last_chunk_load_time = (
                pyg.time.get_ticks()
            )

            total = (
                self.num_chunks_x
                *
                self.num_chunks_y
            )

            if (
                self.background_loader_index
                <
                total
            ):

                cx = (
                    self.background_loader_index
                    %
                    self.num_chunks_x
                )

                cy = (
                    self.background_loader_index
                    //
                    self.num_chunks_x
                )

                key = (
                    cx,
                    cy
                )

                if key not in self.Chunks:

                    self.load_chunk(
                        key
                    )

                self.background_loader_index += 1

    # ==================================================
    # Camera Move
    # ==================================================

    def move(self, x, y):

        self.bx += (
            x *
            self.speedCamera
        )

        self.by -= (
            y *
            self.speedCamera
        )


        

    # ==================================================
    # Draw
    # ==================================================

    def drawBlocks(self, display):

        for key in self.get_visible_chunks():

            if key in self.Chunks:

                self.Chunks[key].draw(
                    display,
                    self.bx,
                    self.by
                )


    def texture(self):
        
        self.grass = Texture.grass

        self.stone = Texture.stone

        self.water = Texture.water

        self.sand = Texture.sand

        

    def getblock(self,world_x,world_y,w,h):
        # print("1")
        startx = (world_x + self.bx)
        starty = (world_y + self.by)
        lastx = startx+w
        lasty = starty+h
        blocks = {}
        for keyc ,chunk in self.Chunks.items():
            for keyb , block in chunk.blocks.items():
                x=chunk.x+keyb[0]+self.bx
                y=chunk.y+keyb[1]+self.by
                
                if startx<x and x<lastx and starty<y and y<lasty:
                    blocks[keyb] = block
                    
                    
                    


        return blocks
                    

        


                    
                
    