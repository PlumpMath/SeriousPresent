
from SceneModule.scene_manager import SceneManager
from SceneModule.camera_controller import CameraController
from SceneModule.light_controller import LightController

from direct.showbase.ShowBase import ShowBase

modelPath = "/e/Material/finalHunter.egg"

actorPath = "/e/Material/finalHunter.egg"
actionsPath = {
    "run" : "/e/Material/hunter_WALK666.egg"
}

actorPath2 = "/e/models/panda.egg"
actionsPath2 = {
    "walk" : "/e/models/panda-walk.egg"
}


terrainH = "/e/models/ground.jpg"
terrainMap = "/e/models/ground.jpg"

class GameWorld_Test(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        sceneMgr = SceneManager(self.render)

        actor = sceneMgr.add_actor_scene(actorPath,
                                         actionsPath,
                                         self.render)
        actor.setPos(5, 0, 0)
        actor.setScale(0.1)

        actor.setTwoSided(True)

        sceneMgr.get_ActorMgr().set_clock(globalClock)
        sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actor, "run")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actor, "run")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("a", actor, "run")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("d", actor, "run")
        actorId = sceneMgr.get_ActorMgr().get_resId(actor)
        print "actorId : ", actorId
        sceneMgr.get_ActorMgr().add_effect_to_actor("w", actorId, "actor_move_forward")
        sceneMgr.get_ActorMgr().add_effect_to_actor("s", actorId, "actor_move_backward")
        sceneMgr.get_ActorMgr().add_effect_to_actor("a", actorId, "actor_move_left")
        sceneMgr.get_ActorMgr().add_effect_to_actor("d", actorId, "actor_move_right")

        self.cam.setPos(100, 0, 100)

        camCtrlr = CameraController(self.cam)
        camCtrlr.set_camToggleHost(self)
        camCtrlr.set_clock(globalClock)
        camCtrlr.focus_on(actor, 30)
        actor.setScale(0.5)
        sceneMgr.set_camCtrlr(camCtrlr)
        sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

        print self.render.getName()

        lightCtrlr = LightController()
        lightCtrlr.set_sceneMgr(sceneMgr)

        light1 = lightCtrlr.create_light(lightType = "AmbientLight",
                                         lightColor = (0.2, 0.1, 0.2, 1),
                                         parentId = self.render.getName()
                                         )
        lightId1 = lightCtrlr.get_lightId(light1)
        lightCtrlr.set_light_to(lightId1, self.render.getName())

        light2 = lightCtrlr.create_light(lightType = "DirectionalLight",
                                         lightColor = (1.0, 1.0, 1.0, 1.0),
                                         lightHpr = (0, 0, 0),
                                         parentId = "render")
        lightId2 = lightCtrlr.get_lightId(light2)
        lightCtrlr.set_light_to(lightId2, "render")

        light3 = lightCtrlr.create_light(lightType = "PointLight",
                                         lightColor = (0.8, 0.9, 0.7, 1.0),
                                         lightPos = (5, 5, 5),
                                         parentId = "render")
        lightId3 = lightCtrlr.get_lightId(light3)
        lightCtrlr.set_light_to(lightId3, "render")

        light4 = lightCtrlr.create_light(lightType = "SpotLight",
                                           lightColor = (1.0, 1.0, 1.0, 1.0),
                                           lightPos = (10, 10, 10),
                                           targetId = actorId,
                                           parentId = "render")
        lightId4 = lightCtrlr.get_lightId(light4)
        lightCtrlr.set_light_to(lightId4, "render")

        self.render.setShaderAuto()

        sceneMgr.set_lightCtrlr(lightCtrlr)

        print sceneMgr.get_ActorMgr().get_eventActionRecord()
        print sceneMgr.get_ActorMgr().get_eventEffertRecord()

        model = sceneMgr.add_model_scene(modelPath,
                                         self.render)
        model.setPos(0, 0, 0)

        model.setTwoSided(True)

        #camCtrlr.focus_on(model, 60)

        terra = sceneMgr.add_terrain_scene(terrainH,
                                           terrainMap,
                                           self.render)
        terra.getRoot().setPos(-50, -50, 0)

        print "terrain pos : ", terra.getRoot().getPos()
        print "terrain hpr : ", terra.getRoot().getHpr()
        print "terrain scale : ", terra.getRoot().getScale()
        print "terrain parent : ", terra.getRoot().getParent()

        print "render name : ", self.render.getName()
        print "terrain name : ", terra.getRoot().getName()
        #print "model name : ", model.getName()
        print "actor name : ", actor.getName()

        self.cam.setPos(0, 50, 5)
        self.cam.lookAt(0, 0, 0)

        camCtrlr.add_toggle_to_opt("u", "rotate_around_up")
        camCtrlr.add_toggle_to_opt("j", "rotate_around_down")
        camCtrlr.add_toggle_to_opt("h", "rotate_around_cw")
        camCtrlr.add_toggle_to_opt("k", "rotate_around_ccw")

        print camCtrlr.get_directionsVector()
        arcPkgs = sceneMgr.export_sceneArcPkg()

        f = open("ArcPkgs.txt", "w")
        f.write("---------- Archive Package ----------\n")
        for arcPkg in arcPkgs:
            f.write("===========\n")
            f.write(arcPkg.get_ArchivePackageName() + "\n")
            f.write("itemsName : ")
            for name in arcPkg.get_itemsName():
                f.write(name+", ")
            f.write("\n===========\n")
            for data in arcPkg.get_itemsData():
                f.write(str(data)+"\n")
            f.write("==========\n")
        f.write("------------------------------\n")

        self.taskMgr.add(sceneMgr.update_scene, "update_scene")

game = GameWorld_Test()
game.run()



