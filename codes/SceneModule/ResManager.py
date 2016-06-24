# -*- coding:utf-8 -*-

import SeriousTools.SeriousTools as SeriousTools

class ResManager(object):

    _resType = ""
    _resCount = 0
    _resMap = dict()

    def __init__(self, resType):

        self._resType = resType
        self._resCount = 0
        self._resMap = dict()

    """""""""""""""""
    加载资源,子类必须重写
    """""""""""""""""

    def load_res(self, resPath, extraResPath):

        # load the resource here
        res = None

        self._resCount += 1
        resId = self._gen_resId()

        self._resMap[resId] = res

        return res



    # 生成资源ID
    def _gen_resId(self):

        return self._resType + str(self._resCount)

    """""""""""
    资源查询函数
    """""""""""
    # 根据资源ID获取资源
    def get_resId(self, res):

        return SeriousTools.find_key_in_dict(res, self._resMap)

    # 根据资源获取资源ID
    def get_res(self, resId):

        return SeriousTools.find_value_in_dict(resId, self._resMap)

    """""""""""""""""
    成员变量的get函数
    """""""""""""""""

    def get_resType(self):

        return self._resType

    def get_resCount(self):

        return self._resCount

    def get_resMap(self):

        return self._resMap

    #####################