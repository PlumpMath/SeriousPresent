
from SceneModule.scene_manager import SceneManager
from SceneModule.camera_controller import CameraController
from SceneModule.light_controller import LightController
from RoleModule.role_manager import RoleManager
from ResourcesModule.load_plot import LoadPlot
from ResourcesModule.archives import Archives

from pandac.PandaModules import AntialiasAttrib
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

import sys

config = """
framebuffer-multisample 1
multisamples 2
fullscreen #f
interpolate-frames 1
window-title Reborn : The Soul Of Devil
preload-textures 0
preload-simple-textures 1
texture-compression 1
allow-incomplete-render 1
allow-async-bind 1
restore-initial-pose 0
hardware-animated-vertices #t
model-cache-textures #t
support-threads #t
#want-directtools #t
#want-tk #t
want-pstat #t
"""

loadPrcFileData("", config)

modelRootPath = "/e/Serious2"

village = modelRootPath + "/Material/ModelEGGS/Village/v6.egg"

hunterPath = modelRootPath + "/Material/ModelEGGS/Hunter/hunter_Alarm1.egg"
hunterActionsPath = {
    "run" : modelRootPath + "/Material/ModelEGGS/Hunter/Run.egg",
    "run_back" : modelRootPath + "/Material/ModelEGGS/Hunter/RunBack.egg",
    "rda" : modelRootPath + "/Material/ModelEGGS/Hunter/rightDefenceActionUpdate.egg",
    "lda" : modelRootPath + "/Material/ModelEGGS/Hunter/leftDefenceActionUpdate",
    "bda" : modelRootPath + "/Material/ModelEGGS/Hunter/backDefenceActionUpdate.egg",
}

wifeZombiePath = modelRootPath + "/Material/ModelEGGS/WifeZombie/WifeZombie_Stand.egg"
wifeZombieActionsPath = {
    "walk" : modelRootPath + "/Material/ModelEGGS/WifeZombie/WifeZombie_Walk.egg"
}

terrainH = modelRootPath + "/Material/Terrain/ground.jpg"
terrainMap = modelRootPath + "/Material/Terrain/ground.jpg"

house1Path = modelRootPath + "/Material/ModelEGGS/Village/house1.egg"

hookZombie = modelRootPath + "/Material/ModelEGGS/HookZombie/HookZombie_Pose.egg"

girl = modelRootPath + "/Material/ModelEGGS/GIRL_Pose.egg"

nunv = modelRootPath + "/Material/ModelEGGS/NUNV/NUNV_Pose.egg"

stealer = modelRootPath + "/Material/ModelEGGS/Stealer"

class GameWorld_Test(ShowBase):

    def __init__(self):

        #PStatClient.connect()

        ShowBase.__init__(self)
        #self.oobeCull()
        self.backfaceCullingOn()
        self.setFrameRateMeter(True)
        #self.setSceneGraphAnalyzerMeter(True)
        self.render.flattenStrong()
        #self.render.setAttrib(LightRampAttrib.makeDefault())
        self.render.setTwoSided(True)
        self.render.setAntialias(AntialiasAttrib.MAuto)

        #self.cam.node().getLens().setNear(5)
        #self.openWindow(pipe = self.makeModulePipe("p3tinydisplay"))

        #self.disableMouse()
        sceneMgr = SceneManager()
        sceneMgr.build_on(self)

        model6 = self.loader.loadModel(village)
        model6.setPos(0, 0, 0)
        model6.setScale(5)
        model6.setTwoSided(True)
        model6.reparentTo(self.render)
        model6.clearLight()

        lod = LODNode("lod")
        lodnp = NodePath(lod)
        lodnp.reparentTo(self.render)


        actor = sceneMgr.add_actor_scene(hunterPath,
                                         hunterActionsPath,
                                         self.render)
        actor.setPos(50, 50, 0)
        actor.setScale(1.6)
        #actor.setAntialias(AntialiasAttrib.MAuto)
        actor.setTwoSided(True)
        # self.render.removeNode(actor.node())
        #base.setBackgroundColor(color)
        #model6.reparentTo(lodnp)
        house1 = sceneMgr.add_model_scene(house1Path, self.render)
        house1.setPos(200, 0, 0)

        self.accept("escape", sys.exit)

        sceneMgr.get_ActorMgr().set_clock(globalClock)
        actorId = sceneMgr.get_ActorMgr().get_resId(actor)
        sceneMgr.get_ActorMgr().add_toggle_to_actor("w", actorId, "run")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("s", actorId, "run_back")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("z", actorId, "rda")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("x", actorId, "lda")
        sceneMgr.get_ActorMgr().add_toggle_to_actor("c", actorId, "bda")
        print "actorId : ", actorId
        sceneMgr.get_ActorMgr().add_effert_to_actor("w", actorId, "actor_move_forward")
        sceneMgr.get_ActorMgr().add_effert_to_actor("s", actorId, "actor_move_backward")
        sceneMgr.get_ActorMgr().add_effert_to_actor("a", actorId, "actor_rotate_cw")
        sceneMgr.get_ActorMgr().add_effert_to_actor("d", actorId, "actor_rotate_ccw")

        _zombieWife = sceneMgr.add_actor_scene(wifeZombiePath,
                                               wifeZombieActionsPath,
                                               self.render)
        _zombieWife.setPos(20, 50, 0)
        zId = sceneMgr.get_resId(_zombieWife)
        sceneMgr.get_ActorMgr().add_toggle_to_actor("b", zId, "walk")
        sceneMgr.get_ActorMgr().add_effert_to_actor("b", zId, "actor_move_forward")
        self.cam.setPos(100, 100, 100)

        camCtrlr = CameraController()
        camCtrlr.bind_camera(self.cam)
        camCtrlr.bind_ToggleHost(self)
        camCtrlr.set_clock(globalClock)
        camCtrlr.focus_on(actor, 100)
        camCtrlr.set_rotateSpeed(10)

        sceneMgr.bind_CameraController(camCtrlr)
        sceneMgr.get_ActorMgr().bind_CameraController(camCtrlr)

        self.accept("space", sys.exit)

        print self.render.getName()

        lightCtrlr = LightController()
        lightCtrlr.bind_SceneManager(sceneMgr)

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
                                         lightPos = (5, 5, 50),
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

        #self.render.setShaderAuto()

        sceneMgr.bind_LightController(lightCtrlr)

        print sceneMgr.get_ActorMgr().get_eventActionRecord()
        print sceneMgr.get_ActorMgr().get_eventEffertRecord()

        # terra = sceneMgr.add_terrain_scene(terrainH,
        #                                    terrainMap,
        #                                    self.render)
        # terra.getRoot().setPos(-50, -50, 0)

        # model6.clearLight(light2)
        # model6.clearLight(light3)
        # model6.clearLight(light4)

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
        # arcPkgs = sceneMgr.export_sceneArcPkg()

        roleMgr = RoleManager()
        sceneMgr.get_ActorMgr().bind_RoleManager(roleMgr)
        player = roleMgr.create_role(roleType = "PlayerRole",
                                     modelId = actorId)
        player.print_all_attr()

        npc1 = roleMgr.create_role(roleType = "NPCRole",
                                   modelId = sceneMgr.get_resId(_zombieWife))
        npc1.print_all_attr()


        # roleArcPkg = roleMgr.export_arcPkg()
        # arcPkgs.append(roleArcPkg)

        # f = open("ArcPkgs.txt", "w")
        # f.write("---------- Archive Package ----------\n")
        # for arcPkg in arcPkgs:
        #     f.write("===========\n")
        #     f.write(arcPkg.get_ArchivePackageName() + "\n")
        #     f.write("itemsName : ")
        #     for name in arcPkg.get_itemsName():
        #         f.write(name+", ")
        #     f.write("\n===========\n")
        #     for data in arcPkg.get_itemsData():
        #         f.write(str(data)+"\n")
        #     f.write("==========\n")
        # f.write("------------------------------\n")

        #self.taskMgr.setupTaskChain("actorTaskChain", numThreads = 3)
        #self.taskMgr.setupTaskChain("terraTaskChain")
        #self.taskMgr.setupTaskChain("cameraTaskChain", numThreads = 3)


        self.taskMgr.add(sceneMgr.update_scene, "update_scene")

        self.accept("l", self.__save_archive, [sceneMgr, roleMgr])

        self.accept("space", self.dialog_show)
        self.accept("find_npc", self.print_accept_event, ["find_npc"])
        self.accept("find_nothing", self.print_accept_event, ["find_nothing"])

        self.accept("w_effert", self.check_event, ["w_effert"])

        self.render.analyze()

    def __save_archive(self, sceneMgr, roleMgr):

        print "Archiving.."

        archive = Archives()
        #archive.read_from_file()
        archive.save_archive(sceneMgr.export_sceneArcPkg(),
                             [roleMgr.export_arcPkg()],
                             -1,
                             "archive1")

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



