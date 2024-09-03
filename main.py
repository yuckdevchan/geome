from numpy import double
from config import config, core
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CardMaker, NodePath, Texture, TransparencyAttrib

from camera import FirstPersonCamera
import resources
from log import log
log("Starting game...")
import disc

class Main(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.fp_camera = FirstPersonCamera(self)
        self.accept("t", self.create_next_chunk)
        self.accept("y", self.delete_next_chunk)
        self.create_chunk(0, 0)

    def create_card(self, x: int, y: int, z: int, h, p, r, texture, block_node, transparent, double_sided) -> None:
        self.card_maker = CardMaker("square")
        self.card_maker.set_frame(-1, 1, -1, 1)
        self.card_maker.set_has_uvs(True)
        self.card_maker.set_has_normals(True)

        self.square = NodePath(self.card_maker.generate())
        self.square.set_pos(x, y, z)
        self.square.set_hpr(h, p, r)

        texture = self.loader.load_texture(texture)
        texture.set_magfilter(Texture.FT_nearest)
        self.square.set_texture(texture)

        if transparent:
            self.square.set_transparency(TransparencyAttrib.M_alpha)
        if double_sided:
            self.square.set_two_sided(True)

        self.square.reparentTo(block_node)

    def create_cube(self, x: int, y: int, z: int, block, top_covered, bottom_covered, left_covered, right_covered, front_covered, back_covered, chunk_node) -> None:
        block_node = NodePath(f"block-{x}-{y}-{z}")
        block_data = resources.get_block_data(block)
        transparent = resources.is_block_transparent(block)
        billboard = resources.is_block_billboard(block)
        if billboard:
            self.create_card(x, y+1, z, 45, 0, 0, resources.get_texture(block, ""), block_node, transparent, double_sided=True)
            self.create_card(x, y+1, z, -45, 0, 0, resources.get_texture(block, ""), block_node, transparent, double_sided=True)
        else:
            if not front_covered:
                self.create_card(x, y, z, 0, 0, 0, resources.get_texture(block, ""), block_node, transparent, double_sided=False)
            if not bottom_covered:
                self.create_card(x, y + 1, z - 1, 0, 90, 0, resources.get_texture(block, ""), block_node, transparent, double_sided=False)
            if not right_covered:
                self.create_card(x + 1, y + 1, z, 90, 0, 0, resources.get_texture(block, ""), block_node, transparent, double_sided=False)
            if not left_covered:
                self.create_card(x - 1, y + 1, z, -90, 0, 0, resources.get_texture(block, ""), block_node, transparent, double_sided=False)
            if not top_covered:
                self.create_card(x, y + 1, z + 1, 0, -90, 0, resources.get_texture(block, ""), block_node, transparent, double_sided=False)
            if not back_covered:
                self.create_card(x, y + 2, z, 180, 0, 0, resources.get_texture(block, ""), block_node, transparent, double_sided=False)
        block_node.reparentTo(chunk_node)

    def create_chunk(self, x: int, y: int, z=0) -> None:
        chunk_node = NodePath(f"chunk-{x}-{y}")
        chunk = disc.get_chunk(x, y)
        for i in range(config["World"]["chunk_width"]):
            for j in range(config["World"]["chunk_width"]):
                for k in range(config["World"]["max_world_height"]):
                    block = chunk[i][j][k]
                    block_data = resources.get_block_data(block)
                    if block != "air":
                        top_covered = k < config["World"]["max_world_height"] - 1 and not resources.is_block_transparent(chunk[i][j][k + 1])
                        bottom_covered = k > 0 and not resources.is_block_transparent(chunk[i][j][k - 1])
                        left_covered = i > 0 and not resources.is_block_transparent(chunk[i - 1][j][k])
                        right_covered = i < config["World"]["chunk_width"] - 1 and not resources.is_block_transparent(chunk[i + 1][j][k])
                        front_covered = j > 0 and not resources.is_block_transparent(chunk[i][j - 1][k])
                        back_covered = j < config["World"]["chunk_width"] - 1 and not resources.is_block_transparent(chunk[i][j + 1][k])
                        block_x = i * 2 + x * config["World"]["chunk_width"] * 2
                        block_y = j * 2 + y * config["World"]["chunk_width"] * 2
                        block_z = k * 2 + z * config["World"]["max_world_height"] * 2
                        if block_z == 0:
                            bottom_covered = True
                        self.create_cube(block_x, block_y, block_z, block, top_covered, bottom_covered, left_covered, right_covered, front_covered, back_covered, chunk_node)
        chunk_node.reparentTo(self.render)
        chunk_node.flattenStrong()

    def create_next_chunk(self):
        self.create_chunk(5, 0)
        self.create_chunk(0, 1)

    def delete_chunk(self, x: int, y: int) -> None:
        self.render.find(f"chunk-{x}-{y}").removeNode()

    def delete_next_chunk(self):
        self.delete_chunk(5, 0)
        self.delete_chunk(0, 1)

    def delete_block(self, chunk_x: int, chunk_y: int, x: int, y: int, z: int) -> None:
        chunk_node = self.render.find(f"chunk-{chunk_x}-{chunk_y}")
        block_node = chunk_node.find(f"block-{x}-{y}-{z}")
        if block_node:
            block_node.removeNode()

app = Main()
app.run()
