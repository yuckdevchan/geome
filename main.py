from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, CardMaker, Texture
from panda3d.core import WindowProperties
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from pathlib import Path

from camera import FirstPersonCamera
from log import log
from world import world
from config import config, core
import resources


class Main(ShowBase):
    def __init__(self):
        log("Starting game...")
        ShowBase.__init__(self)
        self.fp_camera = FirstPersonCamera(self)

        def create_card(x: int, y: int, z: int, h, p, r, texture) -> None:
            self.card_maker = CardMaker("square")
            self.card_maker.set_frame(-1, 1, -1, 1)
            self.card_maker.set_has_uvs(True)
            self.card_maker.set_has_normals(True)

            self.square = NodePath(self.card_maker.generate())
            self.square.reparent_to(self.render)
            self.square.set_pos(x, y, z)
            self.square.set_hpr(h, p, r)

            texture = self.loader.load_texture(texture)
            texture.set_magfilter(Texture.FT_nearest)
            self.square.set_texture(texture)

        def create_cube(x: int, y: int, z: int, block, top_covered, bottom_covered, left_covered, right_covered, front_covered, back_covered) -> None:
            if not front_covered:
                create_card(x, y, z, 0, 0, 0, resources.get_texture(block, ""))
            if not bottom_covered:
                create_card(x, y + 1, z - 1, 0, 90, 0, resources.get_texture(block, ""))
            if not right_covered:
                create_card(x + 1, y + 1, z, 90, 0, 0, resources.get_texture(block, ""))
            if not left_covered:
                create_card(x - 1, y + 1, z, -90, 0, 0, resources.get_texture(block, ""))
            if not top_covered:
                create_card(x, y + 1, z + 1, 0, -90, 0, resources.get_texture(block, ""))
            if not back_covered:
                create_card(x, y + 2, z, 180, 0, 0, resources.get_texture(block, ""))

        def create_chunk(x: int, y: int, z: int) -> None:
            chunk_node = NodePath("chunk")
            chunk = world[x][y]
            for i in range(config["World"]["chunk_width"]):
                for j in range(config["World"]["chunk_width"]):
                    for k in range(config["World"]["max_world_height"]):
                        block = chunk[i][j][k]
                        if block != "air":
                            top_covered = True if k < config["World"]["max_world_height"] - 1 and chunk[i][j][k + 1] and chunk[i][j][k + 1] != "air" else False
                            bottom_covered = True if k > 0 and chunk[i][j][k - 1] and chunk[i][j][k - 1] != "air" else False
                            left_covered = True if i > 0 and chunk[i - 1][j][k] and chunk[i - 1][j][k] != "air" else False
                            right_covered = True if i < config["World"]["chunk_width"] - 1 and chunk[i + 1][j][k] and chunk[i + 1][j][k] != "air" else False
                            front_covered = True if j > 0 and chunk[i][j - 1][k] and chunk[i][j - 1][k] != "air" else False
                            back_covered = True if j < config["World"]["chunk_width"] - 1 and chunk[i][j + 1][k] and chunk[i][j + 1][k] != "air" else False
                            create_cube(x + i * 2, y + j * 2, z + k * 2, block, top_covered, bottom_covered, left_covered, right_covered, front_covered, back_covered)
            chunk_node.flattenStrong()

        create_chunk(0, 0, 0)

app = Main()
app.run()
