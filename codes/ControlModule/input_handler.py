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

class MenuInputHandler(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)

        # 所有的状态类别
        self.__new_game = False
        self.__load_game = False
        self.__description = False
        self.__exit = False
        self.__select = False

        taskMgr.add(self.updateInput,"update input")

    def beginNewGame(self):
        self.__new_game = True

    def endNewGame(self):
        self.__new_game = False

    def beginLoadGame(self):
        self.__load_game = True

    def endLoadGame(self):
        self.__load_game = False

    def beginDescription(self):
        self.__description = True

    def endDescription(self):
        self.__description = False

    def beginExit(self):
        self.__exit = True

    def endExit(self):
        self.__exit = False

    def beginSelect(self):
        self.__select = True

    def endSelect(self):
        self.__select = False

    def dispatchMessages(self):
        if self.__new_game:
            messenger.send("NewGame")
            print '已经发送 new game'
            self.endNewGame()
        elif self.__load_game:
            messenger.send("LoadGame")
            self.endLoadGame()
        if self.__description:
            messenger.send("Description")
            self.endDescription()
        elif self.__exit:
            messenger.send("Exit")
            self.endExit()
        if  self.__select:
            messenger.send("ChangeMenu")
            self.endSelect()

    def updateInput(self, task):
        return task.cont

    def destroy(self):
        self.ignoreAll()

    def __exit(self):
        exit()