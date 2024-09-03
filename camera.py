from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, CardMaker, Texture
from panda3d.core import WindowProperties
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

import os

from config import config, core
from log import log

class FirstPersonCamera(DirectObject):
    def __init__(self, base):
        self.base = base
        self.camera = base.camera
        self.speed = core["Settings"]["player_speed"]
        self.sensitivity = 0.2
        self.base.camLens.set_fov(config["Graphics"]["fov"])
        # Fullscreen
        window_props = WindowProperties()
        window_props.set_fullscreen(config["Graphics"]["fullscreen"])
        self.base.win.requestProperties(window_props)
        # Framerate Display
        self.base.set_frame_rate_meter(config["Debug"]["show_framerate"])
        self.disable_mouse()
        self.setup_controls()

    def disable_mouse(self):
        self.base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        self.base.win.requestProperties(props)

    def setup_controls(self):
        self.accept(config["Controls"]["break_block"], self.break_block)
        self.accept(config["Controls"]["move_forward"], self.set_move_forward, [True])
        self.accept(config["Controls"]["move_forward"] + "-up", self.set_move_forward, [False])
        self.accept(config["Controls"]["move_backward"], self.set_move_backward, [True])
        self.accept(config["Controls"]["move_backward"] + "-up", self.set_move_backward, [False])
        self.accept(config["Controls"]["move_left"], self.set_move_left, [True])
        self.accept(config["Controls"]["move_left"] + "-up", self.set_move_left, [False])
        self.accept(config["Controls"]["move_right"], self.set_move_right, [True])
        self.accept(config["Controls"]["move_right"] + "-up", self.set_move_right, [False])
        # self.accept(config["Controls"]["sprint"], self.toggle_sprint)
        # self.accept(config["Controls"]["jump"], self.jump)
        self.accept(config["Controls"]["select"], self.start_mouse_look)
        self.accept("o", self.stop_mouse_look)
        self.accept(config["Controls"]["exit_to_desktop"], self.exit_game)
        self.accept(config["Controls"]["wireframe"], self.base.toggle_wireframe)
    
        self.moving_forward = False
        self.moving_backward = False
        self.moving_left = False
        self.moving_right = False
    
        self.base.taskMgr.add(self.update_camera, "update_camera")
    
    def break_block(self):
        pass
    
    def set_move_forward(self, value):
        self.moving_forward = value
    
    def set_move_backward(self, value):
        self.moving_backward = value
    
    def set_move_left(self, value):
        self.moving_left = value
    
    def set_move_right(self, value):
        self.moving_right = value

    def jump(self):
        pass
    
    def update_camera(self, task):
        dt = globalClock.getDt()
        pos = self.camera.getPos()
        if self.moving_forward:
            pos += self.camera.getNetTransform().getMat().getRow3(1) * self.speed * dt
        if self.moving_backward:
            pos -= self.camera.getNetTransform().getMat().getRow3(1) * self.speed * dt
        if self.moving_left:
            pos -= self.camera.getNetTransform().getMat().getRow3(0) * self.speed * dt
        if self.moving_right:
            pos += self.camera.getNetTransform().getMat().getRow3(0) * self.speed * dt
        self.camera.setPos(pos)
        return Task.cont
    
    def move_forward(self):
        self.camera.setPos(self.camera.getPos() + self.camera.getNetTransform().getMat().getRow3(1) * self.speed * globalClock.getDt())
    
    def move_backward(self):
        self.camera.setPos(self.camera.getPos() - self.camera.getNetTransform().getMat().getRow3(1) * self.speed * globalClock.getDt())
    
    def move_left(self):
        self.camera.setPos(self.camera.getPos() - self.camera.getNetTransform().getMat().getRow3(0) * self.speed * globalClock.getDt())
    
    def move_right(self):
        self.camera.setPos(self.camera.getPos() + self.camera.getNetTransform().getMat().getRow3(0) * self.speed * globalClock.getDt())
    
    def start_mouse_look(self):
        self.base.taskMgr.add(self.mouse_look, "mouse_look")
    
    def stop_mouse_look(self):
        self.base.taskMgr.remove("mouse_look")
    
    def mouse_look(self, task):
        md = self.base.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        if self.base.win.movePointer(0, self.base.win.getXSize() // 2, self.base.win.getYSize() // 2):
            self.camera.setH(self.camera.getH() - (x - self.base.win.getXSize() // 2) * self.sensitivity)
            self.camera.setP(self.camera.getP() - (y - self.base.win.getYSize() // 2) * self.sensitivity)
        return Task.cont
    
    def exit_game(self):
        log("Exiting game...")
