# coding=utf-8
from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from panda3d.core import *
from FollowCam import FollowCam
from direct.showbase.DirectObject import DirectObject
from keyboard_mouse_handler import GameControlMouseHandler
from keyboard_mouse_handler import GamePlayerMouseHandler
from test_application import testApplication
from main_menu import MainMenu

class SeriousGame():
	def __init__(self):
		self.app = MainMenu()
		self.app.run()

game = SeriousGame()
