
import random
from conster import *
from BlockManager import *
from npc import *
from contoroler import *
from object import *
from inventory import *
from cppfuncs import *
from structures import Structers



class World:
    def __init__(self, seed ,display = None):
        self.npcs = {}
        self.player = None
        self.seed = seed
        self.display = display
        
        self.playerContoroler = None
        self.blockManager = BlocksWorld(seed)
        self.blockManager.create()

        self.npc_update_counter = 0
        self.npc_update_every = 15

        self.HUD = None
        # self.create()

    def ev(self, ev):
        self.playerContoroler.update(ev)
        self.HUD.update_event(ev)


    def create(self):
        
        ts = []
        num = random.randint(10,50)
        for _ in range(num):
            x = random.randint(0,W_WORLD)
            y = random.randint(0,H_WORLD)
            ts.append([x*BLOCK_SIZE,y*BLOCK_SIZE])
            print([x,y])

        for t in ts:
            Structers.Tree(self.blockManager,t[0],t[1])






    def update(self):
        self.blockManager.update_background_loading(self.display)

        for id, npc in self.npcs.items():
            data = npc[0]
            contoroler = npc[1]

            api = contoroler.getAPI()
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

    def render_all_chunks(self, camera_x, camera_y):
        chunks = [
            chunk
            for chunk in self.blockManager.Chunks.values()
            if chunk.is_loaded
        ]

        if not chunks:
            return

        chunk_size = chunks[0].chunk_size
        block_size = chunks[0].block_size
        blocks_per_chunk = chunk_size * chunk_size
        chunk_count = len(chunks)

        # آرایهٔ پیوستهٔ شناسهٔ تمام بلوک‌ها
        BlocksArray = ctypes.c_int32 * (
            chunk_count * blocks_per_chunk
        )
        all_blocks = BlocksArray()

        # مختصات هر چانک: x, y, x, y, ...
        CoordsArray = ctypes.c_int32 * (chunk_count * 2)
        all_coords = CoordsArray()

        block_offset = 0

        for i, chunk in enumerate(chunks):
            ctypes.memmove(
                ctypes.addressof(all_blocks)
                + block_offset * ctypes.sizeof(ctypes.c_int32),
                ctypes.addressof(chunk.blocks),
                blocks_per_chunk * ctypes.sizeof(ctypes.c_int32)
            )

            all_coords[i * 2] = chunk.chunk_x
            all_coords[i * 2 + 1] = chunk.chunk_y

            block_offset += blocks_per_chunk

        pr(
            all_blocks,
            all_coords,
            chunk_count,
            chunk_size,
            block_size,
            camera_x,
            camera_y,
            chunks[0].world_x
            - chunks[0].chunk_x * chunk_size * block_size,
            chunks[0].world_y
            - chunks[0].chunk_y * chunk_size * block_size
        )

    def updateNPC(self):
        for key, npc in self.npcs.items():
            npc[0].update(self.blockManager)

    def newNPC(
        self,
        w,
        h,
        x,
        y,
        color,
        contoroler=None,
        HUD=None,
        inventory=Invertory(),
        player=False
    ):
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

            # center
            # فقط Player باید True باشد
            player,

            # move
            player
        )

        npc.addinvertory(inventory)

        self.npcs[id] = (
            npc,
            contoroler,
            HUD,
            inventory
        )

        if player:
            self.player = npc

        return npc

    def newPlayer(
        self,
        w,
        h,
        x,
        y,
        color,
        contoroler=None
    ):
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

    def getHUD(self, HUD):
        self.HUD = HUD

    def updateHUD(self):
        self.HUD.update(
            self.player.getStatus(
                self.blockManager
            )
        )

    def draw(self):
        # ==========================================
        # رندر بلوک‌ها
        # ==========================================

        # self.blockManager.drawBlocks(
        #     self.display
        # )

        if Render():
            self.render_all_chunks(0, 0)
            present()
            return True

        return False
            


        # ==========================================
        # Object ها
        # ==========================================

        # for o in obj.getObjs(self.blockManager,self.player).values():
        #     drawables.append(
        #         (
        #             o.world_z,
        #             o.world_y,
        #             o,
        #             "obj"
        #         )
        #     )

        # # ==========================================
        # # NPC ها
        # # ==========================================

        # for id, npc in self.npcs.items():
        #     data = npc[0]

        #     drawables.append(
        #         (
        #             data.world_z,
        #             data.world_y,
        #             data,
        #             "npc"
        #         )
        #     )

        # # ==========================================
        # # مرتب‌سازی برای Z / Y
        # # ==========================================

        # drawables.sort(
        #     key=lambda d: (
        #         d[0],
        #         d[1]
        #     )
        # )

        # # ==========================================
        # # Draw
        # # ==========================================

        # for z, y, item, kind in drawables:

        #     if kind == "obj":

        #         item.draw(
        #             self.display,
        #             bx,
        #             by,
        #             self.player
        #         )

        #     else:

        #         item.draw(
        #             self.display,
        #             bx,
        #             by
        #         )

        # # ==========================================
        # # HUD
        # # ==========================================

        # self.HUD.draw()

        # self.playerContoroler.draw()
