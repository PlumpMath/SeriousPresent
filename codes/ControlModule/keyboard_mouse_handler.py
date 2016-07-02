# coding=utf-8
from input_handler import *
from panda3d.core import *

"""游戏流程的监听"""
class GameControlMouseHandler(InputHandler):
    def __init__(self):
        InputHandler.__init__(self)

        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        self.accept("escape",exit)
        self.accept("w",self.beginWalk)
        self.accept("w-up",self.endWalk)
        self.accept("s",self.beginReverse)
        self.accept("s-up",self.endReverse)
        self.accept("a",self.beginTurnLeft)
        self.accept("a-up",self.endTurnLeft)
        self.accept("d",self.beginTurnRight)
        self.accept("d-up",self.endTurnRight)

        taskMgr.add(self.updateInput,"update input")

    def resetMouse(self):
        cx = base.win.getProperties().getXSize()/2
        cy = base.win.getProperties().getYSize()/2
        base.win.movePointer(0,cx,cy)

    def updateInput(self,task):
        if base.mouseWatcherNode.hasMouse():
            messenger.send("turn",[-base.mouseWatcherNode.getMouseX()*10])

            self.resetMouse()
            self.dispatchMessages()

            return task.cont

"""玩家场景的监听"""
class GamePlayerMouseHandler(InputHandler):
    def __init__(self):
        InputHandler.__init__(self)

        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        self.accept("escape",exit)
        self.accept("w",self.beginWalk)
        self.accept("w-up",self.endWalk)
        self.accept("s",self.beginReverse)
        self.accept("s-up",self.endReverse)
        self.accept("a",self.beginTurnLeft)
        self.accept("a-up",self.endTurnLeft)
        self.accept("d",self.beginTurnRight)
        self.accept("d-up",self.endTurnRight)

        taskMgr.add(self.updateInput,"update input")

    def resetMouse(self):
        cx = base.win.getProperties().getXSize()/2
        cy = base.win.getProperties().getYSize()/2
        base.win.movePointer(0,cx,cy)

    def updateInput(self,task):
        if base.mouseWatcherNode.hasMouse():
            messenger.send("turn",[-base.mouseWatcherNode.getMouseX()*10])

            self.resetMouse()
            self.dispatchMessages()

            return task.cont

class MenuPlayerInputHandler(MenuInputHandler):
    def __init__(self):
        MenuInputHandler.__init__(self)

        base.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        self.__count = 0
        self.accept("w",self.__countDecress)
        self.accept("arrow_up",self.__countDecress)
        self.accept("s",self.__countIncress)
        self.accept("arrow_down",self.__countIncress)
        self.accept("enter",self.__decide)
        self.accept("escape",exit)

        taskMgr.add(self.updateInput, "update input")

    def __countDecress(self):
        self.__count = self.__count - 1

    def __countIncress(self):
        self.__count = self.__count + 1

    def __decide(self):
        tmp = 4
        tmp = self.__count % tmp
        print tmp
        switchInput = {0:self.beginNewGame,
        			   1:self.beginLoadGame,
        			   2:self.beginDescription,
        			   3:self.beginExit}
        switchInput[tmp]()


    def updateInput(self,task):
        self.dispatchMessages()
        return task.cont
