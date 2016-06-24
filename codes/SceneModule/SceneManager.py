# -*- coding:utf-8 -*-

from ActorManager import ActorManager
from ModelManager import ModelManager
from TerrainManager import TerrainManager
import SeriousTools.SeriousTools as SeriousTools

class SceneManager(object):

    def __init__(self):

        self.__actorMgr = ActorManager()
        self.__modelMgr = ModelManager()
        self.__terraMgr = TerrainManager()

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

        return task.cont

    """""""""""""""""""""
    读档存档的场景数据接口
    """""""""""""""""""""

    # 导入场景数据，用于读档
    def import_scene_data(self):
        pass

    #####################

    # 导出场景数据，用于存档
    def export_scene_data(self):
        pass

    """""""""""""""
    成员变量的get函数
    """""""""""""""

    def get_ActorMgr(self):

        return self.__actorMgr

    def get_ModelMgr(self):

        return self.__modelMgr

    def get_TerraMgr(self):

        return self.__terraMgr



