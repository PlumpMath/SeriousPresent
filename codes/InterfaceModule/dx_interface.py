# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData
from pandac.PandaModules import AntialiasAttrib

from SceneModule.scene_manager import SceneManager
from SceneModule.light_controller import LightController
from SceneModule.camera_controller import CameraController
from RoleModule.role_manager import RoleManager

extraConfiguration = """
fullscreen #f
framebuffer-multisample 1
multisamples 2
interpolate-frames 1
"""

loadPrcFileData("", extraConfiguration)

class DXInterface(object):

    def __init__(self):

        object.__init__(self)

        self.__showbase = ShowBase()

        self.__showbase.disableMouse()

        self.__showbase.render.setAntialias(AntialiasAttrib.MAuto)
        self.__showbase.render.setShaderAuto()

        self.__sceneMgr = SceneManager()
        self.__sceneMgr.build_on(self.__showbase)

        self.__roleMgr = RoleManager()
        self.__roleMgr.bind_SceneManager(self.__sceneMgr)

    def get_game_window(self):

        return self.__showbase.win

    def add_scenery(self):

        pass

    def add_figure(self):

        pass

    def get_figure(self):

        pass

    def get_figure_node(self):

        pass

    def set_figure_move(self):

        pass

    def set_figure_attack(self):

        pass

