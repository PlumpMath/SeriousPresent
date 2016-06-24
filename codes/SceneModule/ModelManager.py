# -*- coding:utf-8 -*-

from ResManager import ResManager

from direct.showbase.Loader import Loader

class ModelManager(ResManager):

    def __init__(self, resType = "model"):

        ResManager.__init__(self, resType)

        self.__loader = Loader(self)

    #########################################

    # 加载静态模型
    def load_res(self,
                 resPath,
                 extraResPath = None):

        res = self.__loader.loadModel(resPath)

        self._resCount += 1
        resId = self._gen_resId()

        self._resMap[resId] = res

        return res

    #########################################
