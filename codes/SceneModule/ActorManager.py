# -*- coding:utf-8 -*-

from ResManager import ResManager
import SeriousTools.SeriousTools as SeriousTools

from direct.actor.Actor import Actor
from direct.interval.ActorInterval import ActorInterval

class ActorManager(ResManager):

    def __init__(self, resType = "actor"):

        ResManager.__init__(self, resType)

        self.__itvlMap = dict()

    """""""""""""""
    动态模型管理函数
    """""""""""""""

    # 加载动态模型
    def load_res(self,
                 resPath,
                 extraResPath):

        res = Actor(resPath, extraResPath)

        self._resCount += 1
        resId = self._gen_resId()

        self._resMap[resId] = res
        self.__itvlMap[resId] = self.__gen_interval_for_actor(res)

        return res

    #########################################

    """""""""""""""""
    模型动作触发处理函数
    """""""""""""""""

    # 为Actor的某个动作添加触发事件
    def add_toggle_to_actor(self, toggleEvent, actorOrId, actionName):

        if isinstance(actorOrId, str):

            actorId = actorOrId

            actor = self.get_res(actorId)

            if actor is not None:

                if actionName in actor.getAnimNames():

                    itvl = self.__get_actor_interval(actorId, actionName)

                    actor.accept(event=toggleEvent,
                                 method=self.__interval_loop,
                                 extraArgs=[itvl])

                    actor.accept(event=toggleEvent + "-repeat",
                                method=self.__interval_loop,
                                extraArgs=[itvl])

                    actor.accept(event=toggleEvent + "-up",
                                method=self.__interval_stop,
                                extraArgs=[itvl, actor.getNumFrames(actionName)])


        elif isinstance(actorOrId, Actor):

            actor = actorOrId

            actorId = self.get_resId(actor)

            if actorId is not None:

                if actionName in actor.getAnimNames():

                    itvl = self.__get_actor_interval(actorId, actionName)

                    actor.accept(event = toggleEvent,
                                 method = self.__interval_loop,
                                 extraArgs = [itvl])

                    actor.accept(event = toggleEvent + "-repeat",
                                 method = self.__interval_loop,
                                 extraArgs = [itvl])

                    actor.accept(event = toggleEvent + "-up",
                                 method = self.__interval_stop,
                                 extraArgs = [itvl, actor.getNumFrames(actionName)])

    #########################################

    # 循环Interval
    def __interval_loop(self, itvl):


        if not itvl.isPlaying():

            itvl.loop()

        else:

            print itvl, " Is Playing"

    #########################################

    # 停止Interval
    def __interval_stop(self, itvl, endFrame):


        currFrame = itvl.getCurrentFrame()

        if currFrame is not None:

            itvl.start(startT = currFrame / endFrame)

        #itvl.finish()

    #########################################

    # 为每个Actor的每个动作生成ActorInterval
    def __gen_interval_for_actor(self, actor):

        actionItvlMap = {}

        for actionName in actor.getAnimNames():

            tmpItvl = ActorInterval(actor = actor,
                                    animName = actionName)

            actionItvlMap[actionName] = tmpItvl

        return actionItvlMap

    #########################################

    def __get_actor_interval(self, actorId, actionName):

        actionItvlMap = SeriousTools.find_value_in_dict(actorId, self.__itvlMap)

        if actionItvlMap is not None and \
            actionName in actionItvlMap.keys():

            return actionItvlMap[actionName]

        return None

    #########################################
