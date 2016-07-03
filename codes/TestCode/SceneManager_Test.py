
from SceneModule.scene_manager import SceneManager
from SceneModule.camera_controller import CameraController
from SceneModule.light_controller import LightController
from RoleModule.role_manager import RoleManager
from ResourcesModule.load_plot import LoadPlot

from pandac.PandaModules import AntialiasAttrib
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

import sys

config = """
framebuffer-multisample 1
multisamples 2
"""

loadPrcFileData("", "fullscreen #f")
loadPrcFileData("", "interpolate-frames 1")
loadPrcFileData("", config)

modelPath = "/e/Material/finalHunter.egg"
buildingPath = "/e/Material/building1.egg"

treeModel = "/e/Material/building1.egg"

actorPath = "/e/Material/hunter_WithGun.egg"
actionsPath = {
    "run" : "/e/Material/hunter_RunWithGun.egg",
    "run_back" : "/e/Material/hunter_RunBack.egg",
    "rda" : "/e/Material/rightDefenceActionUpdate.egg",
    "lda" : "/e/Material/leftDefenceActionUpdate.egg",
    "bda" : "/e/Material/backDefenceActionUpdate1.egg",
}

actorPath2 = "/e/Material/outter_child.egg"
actionsPath2 = {
    "run" : "/e/Material/outter_run.egg"
}

buildingPath1 = "/e/Material/building1.egg"

terrainH = "/e/models/ground.jpg"
terrainMap = "/e/models/ground.jpg"

class GameWorld_Test(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.render.setAntialias(AntialiasAttrib.MAuto)

        self.disableMouse()

        sceneMgr = SceneManager()
        sceneMgr.build_on(self)

        actor = sceneMgr.add_actor_scene(actorPath,
                                         actionsPath,
                                         self.render)
        actor.setPos(5, 0, 0)
        actor.setScale(1.2)
        actor.setAntialias(AntialiasAttrib.MAuto)
        actor.setTwoSided(True)

        color = (0.5, 0.5, 0.8, 1.0)
        fog = Fog("fog")
        fog.setColor(color)
        fog.setExpDensity(0.005)
        actor.setFog(fog)
        #base.setBackgroundColor(color)

        sceneMgr.get_ActorMgr().set_clock(globalClock)
        actorId = sceneMgr.get_ActorMgr().get_resId(actor)
        sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actorId, "run")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actorId, "run_back")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("z", actorId, "rda")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("x", actorId, "lda")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("c", actorId, "bda")
        print "actorId : ", actorId
        #sceneMgr.get_ActorMgr().add_effect_to_actor("w", actorId, "actor_move_forward")
        #sceneMgr.get_ActorMgr().add_effect_to_actor("s", actorId, "actor_move_backward")
        sceneMgr.get_ActorMgr().add_effect_to_actor("a", actorId, "actor_rotate_cw")
        sceneMgr.get_ActorMgr().add_effect_to_actor("d", actorId, "actor_rotate_ccw")

        self.cam.setPos(100, 0, 100)

        camCtrlr = CameraController(self.cam)
        camCtrlr.set_camToggleHost(self)
        camCtrlr.set_clock(globalClock)
        camCtrlr.focus_on(actor, 100)

        sceneMgr.set_camCtrlr(camCtrlr)
        sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

        self.accept("space", sys.exit)

        print self.render.getName()

        lightCtrlr = LightController()
        lightCtrlr.set_sceneMgr(sceneMgr)

        # light1 = lightCtrlr.create_light(lightType = "AmbientLight",
        #                                  lightColor = (0.2, 0.1, 0.2, 1),
        #                                  parentId = self.render.getName()
        #                                  )
        # lightId1 = lightCtrlr.get_lightId(light1)
        # lightCtrlr.set_light_to(lightId1, self.render.getName())

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
        model.setScale(0.22)
        model.setTwoSided(True)

        building = sceneMgr.add_model_scene(buildingPath1, self.render)
        building.setPos(-10, -30, 0)
        building.setScale(15)

        # building = sceneMgr.add_model_scene(buildingPath, self.render)
        # building.setPos(0, 10, 0)
        # building.setScale(5)
        # building.setTwoSided(True)

        #camCtrlr.focus_on(model, 60)

        tree = sceneMgr.add_model_scene(treeModel,
                                        self.render)

        tree.setPos(0, 0, 0)
        tree.setScale(5)
        tree.setTwoSided(True)

        terra = sceneMgr.add_terrain_scene(terrainH,
                                           terrainMap,
                                           self.render)
        terra.getRoot().setPos(-50, -50, 0)

        # print "terrain pos : ", terra.getRoot().getPos()
        # print "terrain hpr : ", terra.getRoot().getHpr()
        # print "terrain scale : ", terra.getRoot().getScale()
        # print "terrain parent : ", terra.getRoot().getParent()
        #
        # print "render name : ", self.render.getName()
        # print "terrain name : ", terra.getRoot().getName()
        # #print "model name : ", model.getName()
        # print "actor name : ", actor.getName()

        self.cam.setPos(0, 50, 5)
        self.cam.lookAt(0, 0, 0)

        camCtrlr.add_toggle_to_opt("u", "rotate_around_up")
        camCtrlr.add_toggle_to_opt("j", "rotate_around_down")
        camCtrlr.add_toggle_to_opt("h", "rotate_around_cw")
        camCtrlr.add_toggle_to_opt("k", "rotate_around_ccw")

        #print camCtrlr.get_directionsVector()
        arcPkgs = sceneMgr.export_sceneArcPkg()

        roleMgr = RoleManager()
        sceneMgr.get_ActorMgr().bind_RoleManager(roleMgr)
        player = roleMgr.create_role(roleType = "PlayerRole",
                                     modelId = actorId)
        player.print_all_attr()

        actor2 = sceneMgr.add_actor_scene(actorPath2, actionsPath2, self.render)
        actor2.setPos(20, 20, 0)
        actor2.setScale(0.1)

        npc1 = roleMgr.create_role(roleType = "NPCRole",
                                   modelId = sceneMgr.get_resId(actor2))
        npc1.print_all_attr()


        roleArcPkg = roleMgr.export_arcPkg()
        arcPkgs.append(roleArcPkg)

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

        for a, b in sceneMgr.get_ActorMgr().get_toggleEffert().iteritems():
            print a

        self.taskMgr.add(sceneMgr.update_scene, "update_scene")

        self.accept("space", self.dialog_show)
        self.accept("find_npc", self.print_accept_event, ["find_npc"])
        self.accept("find_nothing", self.print_accept_event, ["find_nothing"])

        self.accept("w_effert", self.check_event, ["w_effert"])

    def check_event(self, event):

        print event, " happen"

    def dialog_show(self):

        demo = LoadPlot()

        demo.init_interface(2)

        demo.dialogue_next()

    def print_accept_event(self, event):

        #print event
        pass

game = GameWorld_Test()
game.run()



