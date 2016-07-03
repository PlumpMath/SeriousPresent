
from direct.interval.FunctionInterval import *
from direct.interval.Interval import *
from direct.interval.IntervalGlobal import *
from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import TransparencyAttrib

class Demo(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        modelPath = "/e/Material/finalHunter.egg"
        model = self.loader.loadModel(modelPath)
        model.reparentTo(self.render)
        model.setPos(0, 0, 0)

        ballPath = "/e/Material/Drop.egg"
        self.ball = self.loader.loadModel(ballPath)
        self.ball.reparentTo(self.render)
        self.ball.setPos(0, 0, 0)
        self.ball.hide()
        x = self.ball.getX()
        y = self.ball.getY()

        model.setTransparency(TransparencyAttrib.MAlpha)
        colorItvl = LerpColorInterval(
            nodePath = model,
            duration = 3,
            color = (0, 0, 0, 0),
        )
        colorItvl.start()

        posItvl = LerpPosInterval(
            nodePath = self.ball,
            duration = 1,
            pos = (x, y, 0)
        )

        seq = Sequence(colorItvl, Func(self.show_ball))
        seq.start()

        self.cam.setPos(0, 50, 20)
        self.cam.lookAt(0, 0, 0)

    def show_ball(self):

        self.ball.show()

demo = Demo()
demo.run()