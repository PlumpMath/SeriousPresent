# -*- coding:utf-8 -*-

from actor_manager import ActorManager
from model_manager import ModelManager
from terrain_manager import TerrainManager
import SeriousTools.SeriousTools as SeriousTools

class SceneManager(object):

    def __init__(self, render):

        self.__actorMgr = ActorManager()
        self.__modelMgr = ModelManager()
        self.__terraMgr = TerrainManager()

        self.__render = render

        self.__camCtrlr = None
        self.__lightCtrlr = None

    """""""""""""""""""""""""""""""""""""""
    场景管理函数，包括创建、更新、剔除、隐藏等
    """""""""""""""""""""""""""""""""""""""

    # 添加动态模型场景
    def add_actor_scene(self,
                        resPath,
                        extraResPath,
                        parentNode):

        actor = self.__actorMgr.load_res(resPath, extraResPath)

        actor.reparentTo(parentNode)

        return actor

    #####################

    # 添加静态模型场景
    def add_model_scene(self,
                        resPath,
                        parentNode):

        model = self.__modelMgr.load_res(resPath)

        model.reparentTo(parentNode)

        return model

    #####################

    # 添加地形场景
    def add_terrain_scene(self,
                          resPath,
                          extraResPath,
                          parentNode):

        terrain = self.__terraMgr.load_res(resPath, extraResPath)

        terrain.getRoot().reparentTo(parentNode)

        return terrain

    #####################

    # 更新场景
    def update_scene(self, task):

        # 更新地形
        self.__terraMgr.update_terrain(task)

        self.__camCtrlr.update_camera(task)

        self.__actorMgr.update_actors(task)

        return task.cont

    #####################

    # 总的资源ID查询
    def get_resId(self, res):

        resId = None

        resId =  self.__actorMgr.get_resId(res)

        if resId is None:

            resId = self.__modelMgr.get_resId(res)

            if resId is None:

                resId = self.__terraMgr.get_resId(res)

        return resId

    #####################

    # 总的资源查询
    def get_res(self, resId):

        if resId == "render":

            return self.__render

        res = self.__actorMgr.get_res(resId)

        if res is None:

            res = self.__modelMgr.get_res(resId)

            if res is None:

                res = self.__terraMgr.get_res(resId)

        return res

    def set_camCtrlr(self, camCtrlr):

        self.__camCtrlr = camCtrlr

    def get_camCtrlr(self):

        return self.__camCtrlr

    def set_lightCtrlr(self, lightCtrlr):

        self.__lightCtrlr = lightCtrlr

    def get_lightCtrlr(self):

        return self.__lightCtrlr

    """""""""""""""""""""
    读档存档的场景数据接口
    """""""""""""""""""""

    # 导入场景数据，用于读档
    def import_sceneArcPkg(self, sceneArcPkg):

        # Actor数据读档
        actorArcPkg = sceneArcPkg[0]

        


        # Model数据读档

        # Terrain数据读档

        # Camera数据读档

        # Light数据读档

        pass

    #####################

    # 导出场景数据，用于存档
    # 考虑到获取父节点ID的全局性，故将其他几种资源的存档数据放到这里进行保存
    def export_sceneArcPkg(self):

        # Actor数据存档
        actorArcPkg = self.__actorMgr.get_arcPkg()

        actorResPath = self.__actorMgr.get_resPath()

        actorEventActionRecord = self.__actorMgr.get_eventActionRecord()
        actorEventEffertRecord = self.__actorMgr.get_eventEffertRecord()

        for actorId, actor in self.__actorMgr.get_resMap().iteritems():

            actorItem = []

            actorItem.append(actorId)
            actorItem.append(actorResPath[actorId][0])
            actorItem.append(actorResPath[actorId][1])
            actorItem.append(actor.getPos())
            actorItem.append(actor.getHpr())
            actorItem.append(actor.getScale())
            actorItem.append(actorEventActionRecord[actorId])
            actorItem.append(actorEventEffertRecord[actorId])

            parentNode = actor.getParent()

            if parentNode.getName() is "render":

                actorItem.append("render")

            else:

                parentId = self.get_resId(parentNode)

                if parentId is None:

                    actorItem.append("render")

                else:

                    actorItem.append(parentId)

            actorArcPkg.add_item(actorItem)

        ##########

        # Model数据存档
        modelArcPkg = self.__modelMgr.get_arcPkg()

        modelResPath = self.__modelMgr.get_resPath()

        for modelId, model in self.__modelMgr.get_resMap().iteritems():

            modelItem = []

            modelItem.append(modelId)
            modelItem.append(modelResPath[modelId])
            modelItem.append(model.getPos())
            modelItem.append(model.getHpr())
            modelItem.append(model.getScale())

            parentNode = model.getParent()

            if parentNode.getName() is "render":

                modelItem.append("render")

            else:

                parentId = self.get_resId(parentNode)

                if parentId is None:

                    modelItem.append("render")

                else:

                    modelItem.append(parentId)

            modelArcPkg.add_item(modelItem)

        ##########

        # Terrain数据存档
        terraArcPkg = self.__terraMgr.get_arcPkg()

        terraArcPkg.set_metaData("currTerraId", self.__terraMgr.get_currTerrain())

        terraResPath = self.__terraMgr.get_resPath()

        for terrainId, terrain in self.__terraMgr.get_resMap().iteritems():

            terrainItem = []

            terrainItem.append(terrainId)
            terrainItem.append(terraResPath[terrainId][0])
            terrainItem.append(terraResPath[terrainId][1])
            terrainItem.append(terrain.getRoot().getPos())
            terrainItem.append(terrain.getRoot().getHpr())
            terrainItem.append(terrain.getRoot().getScale())

            parentNode = terrain.getRoot().getParent()

            if parentNode.getName() is "render":

                terrainItem.append("render")

            else:

                parentId = self.get_resId(parentNode)

                if parentId is None:

                    terrainItem.append("render")

                else:

                    terrainItem.append(parentId)

            terraArcPkg.add_item(terrainItem)

        ##########

        # Camera数据存档
        camArcPkg = self.__camCtrlr.get_arcPkg()

        cam = self.__camCtrlr.get_camToCtrl()

        camItem = []

        camItem.append(cam.getPos())
        camItem.append(cam.getHpr())
        camItem.append(self.__camCtrlr.get_moveSpeed())
        camItem.append(self.__camCtrlr.get_rotateSpeed())

        focusObjId = self.get_resId(self.__camCtrlr.get_focusObj())
        camItem.append(focusObjId)

        camItem.append(self.__camCtrlr.get_rotateRadius())
        camItem.append(self.__camCtrlr.get_optsSwitch())
        camItem.append(self.__camCtrlr.get_toggleEventToOpts())

        camArcPkg.add_item(camItem)

        ##########

        # Light数据存档
        lightArcPkg = self.__lightCtrlr.get_arcPkg()

        lightTargetMap = self.__lightCtrlr.get_targetMap()

        lightSetorMap = self.__lightCtrlr.get_setorMap()

        for lightId, light in self.__lightCtrlr.get_lightMap().iteritems():

            lightItem = []

            lightItem.append(lightId)
            lightItem.append(light.node().getColor())
            lightItem.append(light.getPos())
            lightItem.append(light.getHpr())

            if lightTargetMap.has_key(lightId) is True:

                lightItem.append(lightTargetMap[lightId])

            else:

                lightItem.append(None)

            lightItem.append(lightSetorMap[lightId])

            parentNode = light.getParent()

            if parentNode.getName() is "render":

                lightItem.append("render")

            else:

                parentId = self.get_resId(parentNode)

                if parentId is None:

                    lightItem.append("render")

                else:

                    lightItem.append(parentId)

            lightArcPkg.add_item(lightItem)

        ##########

        sceneArcPkg = [
            actorArcPkg,
            modelArcPkg,
            terraArcPkg,
            camArcPkg,
            lightArcPkg
        ]

        return sceneArcPkg


    """""""""""""""
    成员变量的get函数
    """""""""""""""

    def set_render(self, render):

        self.__render = render

    def get_render(self):

        return self.__render

    def get_ActorMgr(self):

        return self.__actorMgr

    def get_ModelMgr(self):

        return self.__modelMgr

    def get_TerraMgr(self):

        return self.__terraMgr



