from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, CardMaker, Texture
from panda3d.core import WindowProperties
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

from pathlib import Path

from camera import FirstPersonCamera
from log import log
import resources


class MyApp(ShowBase):
    def __init__(self):
        log("Starting game...")
        ShowBase.__init__(self)
        self.fp_camera = FirstPersonCamera(self)

        def create_card(x: int, y: int, z: int, h, p, r) -> None:
            self.card_maker = CardMaker("square")
            self.card_maker.set_frame(-1, 1, -1, 1)
            self.card_maker.set_has_uvs(True)
            self.card_maker.set_has_normals(True)

            self.square = NodePath(self.card_maker.generate())
            self.square.reparent_to(self.render)
            self.square.set_pos(x, y, z)
            self.square.set_hpr(h, p, r)

            texture = self.loader.load_texture(resources.get_texture("dirt"))
            texture.set_magfilter(Texture.FT_nearest)
            self.square.set_texture(texture)

        def create_cube(x: int, y: int, z: int) -> None:
            create_card(x, y, z, 0, 0, 0)
            create_card(x, y + 1, z - 1, 0, 90, 0)
            create_card(x + 1, y + 1, z, 90, 0, 0)
            create_card(x - 1, y + 1, z, -90, 0, 0)
            create_card(x, y + 1, z + 1, 0, -90, 0)
            create_card(x, y + 2, z, 180, 0, 0)

        def create_chunk(x: int, y: int, z: int) -> None:
            for i in range(16):
                for j in range(16):
                    create_cube(x + i * 2, y + j * 2, z)

        create_chunk(0, 0, 0)


app = MyApp()
app.run()
