# -*- coding:utf-8 -*-

from direct.showbase.ShowBase import ShowBase

modelPath = "/e/models/ralph/ralph"

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        model = self.loader.loadModel(modelPath)
        model.reparentTo(self.render)
        model.setPos(0, 0, 0)

        self.cam.setPos(0, 10, 0)
        self.cam.lookAt(0, 0, 0)

demo = Demo()
demo.run()
