# coding=utf-8
from direct.showbase.DirectObject import DirectObject
from direct.showbase.MessengerGlobal import messenger
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import *

class InputHandler(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)

        # 所有的状态类别
        self.menu = False
        self.load = False
        self.game = False
        self.save = False
        self.exitMenu = False

        # 人物动作
        self.walk = False
        self.reverse = False
        self.left = False
        self.right = False

        taskMgr.add(self.updateInput,"update input")

    def beginMenu():
        messenger.send("Menu-start")
        self.menu = True

    def endMenu():
        messenger.send("Menu-stop")
        self.menu = False

    def beginload():
        messenger.send("load-start")
        self.load = True

    def endload():
        messenger.send("load-stop")
        self.load = False

    def begingame():
        messenger.send("game-start")
        self.game = True

    def endgame():
        messenger.send("game-stop")
        self.game = False

    def beginsave():
        messenger.send("save-start")
        self.save = True

    def endsave():
        messenger.send("save-stop")
        self.save = False

    def beginexitMenu():
        messenger.send("exitMenu-start")
        self.exitMenu = True

    def endexitMenu():
        messenger.send("exitMenu-stop")
        self.exitMenu = False

    def beginWalk(self):
        messenger.send("walk-start")
        self.walk = True

    def endWalk(self):
        messenger.send("walk-stop")
        self.walk = False

    def beginReverse(self):
        messenger.send("reverse-start")
        self.reverse = True

    def endReverse(self):
        messenger.send("reverse-stop")
        self.reverse = False

    def beginTurnLeft(self):
        self.left = True

    def endTurnLeft(self):
        self.left = False

    def beginTurnRight(self):
        self.right = True

    def endTurnRight(self):
        self.right = False

    def dispatchMessages(self):
        if self.walk:
            messenger.send("walk", [-0.1])
        elif self.reverse:
            messenger.send("reverse", [0.1])
        if self.left:
            messenger.send("turn", [0.8])
        elif self.right:
            messenger.send("turn", [-0.8])

    def updateInput(self, task):
            return task.cont
