# -*- coding:utf-8 -*-

from ResManager import ResManager
import SeriousTools.SeriousTools as SeriousTools

from panda3d.core import GeoMipTerrain

class TerrainManager(ResManager):

    def __init__(self, resType = "terrain"):

        ResManager.__init__(self, resType)

        self.__currTerrainId = None

    #########################################

    # 加载地形资源
    def load_res(self,
                 resPath,
                 extraResPath):

        self._resCount += 1
        resId = self._gen_resId()

        self.__currTerrainId = resId

        res = GeoMipTerrain(resId)

        res.setHeightfield(resPath)
        res.setColorMap(extraResPath)

        self._resMap[resId] = res

        return res

    #########################################

    # 设置当前所使用的地形
    def set_curr_terrain(self, terrainId):

        self.__currTerrainId = terrainId

        for id in self._resMap.keys():

            if id == self.__currTerrainId:

                self._resMap[id].show()

            else:

                self._resMap[id].hide()

    #########################################

    # 更新地形
    def update_terrain(self, task):

        self._resMap[self.__currTerrainId].update()

        return task.cont

