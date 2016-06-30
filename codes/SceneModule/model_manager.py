# <<<<<<< .mine
# # -*- coding:utf-8 -*-
#
# import ResManager
#
# from direct.showbase.Loader import Loader
#
# class ModelManager(ResManager):
#
#     def __init__(self, resType = "model"):
#
#         super.__init__(self, resType)
#
#         self.__loader = Loader(self)
#
#     #########################################
#
#     def load_res(self, resPath, extraResPath = None):
#
#         res = self.__loader.loadModel(resPath)
#
#         self.__resCount += 1
#         resId = self._gen_resId()
#
#         self.__resMap[resId] = res
#
#         return res
#
#     #########################################
# ||||||| .r0
# =======
# -*- coding:utf-8 -*-

from res_manager import ResManager
from ArchiveModule.archive_package import ArchivePackage

from direct.showbase.Loader import Loader

class ModelManager(ResManager):

    def __init__(self, resType = "model"):

        ResManager.__init__(self, resType)

        self.__loader = Loader(self)

        self.__arcPkg = ArchivePackage(arcPkgName = "model",
                                       itemsName = [
                                           "modelId",
                                           "modelPath",
                                           "pos",
                                           "hpr",
                                           "scale",
                                           "parentId"
                                       ])

    #########################################

    # 加载静态模型
    def load_res(self,
                 resPath,
                 extraResPath = None):

        res = self.__loader.loadModel(resPath)

        self._resCount += 1
        resId = self._gen_resId()

        self._resMap[resId] = res
        self._resPath[resId] = resPath

        return res

    #########################################

    def get_arcPkg(self):

        return self.__arcPkg