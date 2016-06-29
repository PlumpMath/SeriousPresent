# -*- coding:utf-8 -*-

from res_manager import ResManager
from RoleModule.role_manager import RoleManager
from ArchiveModule.archive_package import ArchivePackage
import SeriousTools.SeriousTools as SeriousTools

from direct.actor.Actor import Actor
from direct.interval.ActorInterval import ActorInterval
from direct.showbase.MessengerGlobal import messenger

import math

ACTOR_MOVE_FORWARD  = "actor_move_forward"
ACTOR_MOVE_BACKWARD = "actor_move_backward"
ACTOR_MOVE_LEFT     = "actor_move_left"
ACTOR_MOVE_RIGHT    = "actor_move_right"
ACTOR_ATTACK        = "actor_attack"
ACTOR_BE_ATTACKED   = "actor_be_attacked"
ACTOR_TALK          = "actor_talk"

ACTOR_EFFERT = [
    ACTOR_MOVE_FORWARD,
    ACTOR_MOVE_BACKWARD,
    ACTOR_MOVE_LEFT,
    ACTOR_MOVE_RIGHT,
    ACTOR_ATTACK,
    ACTOR_BE_ATTACKED,
    ACTOR_TALK,
]

class ActorManager(ResManager):

    def __init__(self, resType = "actor"):

        ResManager.__init__(self, resType)

        self.__itvlMap = dict()

        self.__actorMoveSpeed = 4

        self.__roleMgr = None

        self.__camCtrlr = None

        self.__clock = None

        self.__effectSwitch = {
            ACTOR_MOVE_FORWARD  : False,
            ACTOR_MOVE_BACKWARD : False,
            ACTOR_MOVE_LEFT     : False,
            ACTOR_MOVE_RIGHT    : False,
            ACTOR_ATTACK        : False,
            ACTOR_BE_ATTACKED   : False,
            ACTOR_TALK          : False,
        }

        self.__toggleEffert = {
            ACTOR_MOVE_FORWARD  : [self.__actor_move_forward, []],
            ACTOR_MOVE_BACKWARD : [self.__actor_move_backward, []],
            ACTOR_MOVE_LEFT     : [self.__actor_move_left, []],
            ACTOR_MOVE_RIGHT    : [self.__actor_move_right, []],
            ACTOR_ATTACK        : [self.__actor_attack, []],
            ACTOR_BE_ATTACKED   : [self.__actor_be_attacked, []],
            ACTOR_TALK          : [self.__actor_talk, []],
        }

        self.__eventActionRecord = dict() # actorId : [ toggleEvent, actionName ]
        self.__eventEffertRecord = dict() # actorId : [ toggleEvent, effert ]

        self.__camCurrH = None

        self.__N  = 0
        self.__NE = 45
        self.__E  = 90
        self.__ES = 135
        self.__S  = 180
        self.__SW = 225
        self.__W  = 270
        self.__WN = 315
        self.__directionsVector = None

        self.__arcPkg = ArchivePackage(arcPkgName = "actor",
                                       itemsName = [
                                           "actorId",
                                           "actorPath",
                                           "actionsPath",
                                           "pos",
                                           "hpr",
                                           "scale",
                                           "eventActionRecord",
                                           "eventEffertRecord",
                                           "parentId"
                                       ])

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
        self._resPath[resId] = [resPath, extraResPath]

        self.__itvlMap[resId] = self.__gen_interval_for_actor(res)

        return res

    #########################################

    """""""""""""""""
    模型动作触发处理函数
    """""""""""""""""

    # 为Actor的某个动作添加触发事件
    def add_toggle_to_actor(self,
                            toggleEvent,
                            actorOrId,
                            actionName,
                            ):

        if isinstance(actorOrId, str):

            actorId = actorOrId

            actor = self.get_res(actorId)

            if actor is not None:

                if actionName in actor.getAnimNames():

                    itvl = self.__get_actor_interval(actorId, actionName)

                    actor.accept(event=toggleEvent,
                                 method=self.__interval_loop,
                                 extraArgs=[toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-repeat",
                                method=self.__interval_loop,
                                extraArgs=[toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-up",
                                method=self.__interval_stop,
                                extraArgs=[toggleEvent, itvl, actor.getNumFrames(actionName)])

                    if self.__eventActionRecord.has_key(actorId) is False:

                        self.__eventActionRecord[actorId] = list()

                    self.__eventActionRecord[actorId].append([toggleEvent, actionName])

        elif isinstance(actorOrId, Actor):

            actor = actorOrId

            actorId = self.get_resId(actor)

            if actorId is not None:

                if actionName in actor.getAnimNames():

                    itvl = self.__get_actor_interval(actorId, actionName)

                    actor.accept(event=toggleEvent,
                                 method=self.__interval_loop,
                                 extraArgs=[toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-repeat",
                                  method=self.__interval_loop,
                                  extraArgs=[toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-up",
                                 method=self.__interval_stop,
                                 extraArgs=[toggleEvent, itvl, actor.getNumFrames(actionName)])

                    if self.__eventActionRecord.has_key(actorId) is False:

                        self.__eventActionRecord[actorId] = list()

                    self.__eventActionRecord[actorId].append([toggleEvent, actionName])

    #########################################

    # 循环Interval
    def __interval_loop(self, toggleEvennt, itvl):

        if not itvl.isPlaying():

            itvl.loop()

        else:

            print itvl, " Is Playing"

        messenger.send(toggleEvennt + "_effect")

    #########################################

    # 停止Interval
    def __interval_stop(self, toggleEvent, itvl, endFrame):


        currFrame = itvl.getCurrentFrame()

        if currFrame is not None and endFrame is not None:

            itvl.start(startT = currFrame / endFrame)

        messenger.send(toggleEvent + "_effect_end")

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

    def add_effect_to_actor(self,
                            toggleEvent,
                            actorId,
                            effect,
                            extraArgs = None):

        actor = self.get_actor(actorId)

        if actor is not None and effect in ACTOR_EFFERT:

            actor.accept(toggleEvent + "_effect", self.__turn_effect_switch, [effect, True])
            actor.accept(toggleEvent + "_effect_end", self.__turn_effect_switch, [effect, False])

            self.__toggleEffert[effect][1].append(actorId)

            if self.__eventEffertRecord.has_key(actorId) is False:

                self.__eventEffertRecord[actorId] = list()

            self.__eventEffertRecord[actorId].append([toggleEvent, effect])

    #########################################

    def __turn_effect_switch(self, effect, onOrOff):

        self.__effectSwitch[effect] = onOrOff

    #########################################

    """""""""""""""""""""""""""""""""""
    预设角色所做动作所产生的在场景或属性中的变化,
    如人物角色"奔跑"的动作，会导致人物角色在场景中
    位置的变化，受到攻击则血量减少，更换武器攻击力
    和攻击速度变化等等
    """""""""""""""""""""""""""""""""""

    def update_actors(self, task):

        self.__directionsVector = self.__camCtrlr.get_directionsVector()
        self.__update_actor_direction()

        for effect, switch in self.__effectSwitch.iteritems():

            if switch:

                print effect, " : ", switch

                for arg in self.__toggleEffert[effect][1]:

                    execTask = self.__toggleEffert[effect][0]

                    arg = self.get_res(arg)

                    execTask(arg, task)

        return task.cont

    def __update_actor_direction(self):

        x = self.__directionsVector["N"].getX()
        y = self.__directionsVector["N"].getY()

        f = open("ActorDirections.txt", "w")

        f.write(str(self.__directionsVector["N"]) + "\n")

        self.__N  = self.__camCtrlr.get_camToCtrl().getH()
        self.__NE = self.__N + 45
        self.__E  = self.__N + 90
        self.__ES = self.__N + 135
        self.__S  = self.__N + 180
        self.__SW = self.__N + 225
        self.__W  = self.__N + 270
        self.__WN = self.__N + 315

        f.write(str(self.__N))
        f.close()

    #########################################

    def bind_RoleManager(self, roleMgr):

        self.__roleMgr = roleMgr

    def get_roleMgr(self):

        return self.__roleMgr

    def bind_CameraController(self, camCtrlr):

        self.__camCtrlr = camCtrlr

    def get_camCtrlr(self):

        return self.__camCtrlr

    #########################################

    def __actor_move_forward(self, actor, task):

        dt = self.__clock.getDt()
        dVector = None

        actorH = None

        if self.check_effectSwitch(ACTOR_MOVE_LEFT) is True:

            dVector = self.__directionsVector["ES"]

            actorH = self.__SW


        elif self.check_effectSwitch(ACTOR_MOVE_RIGHT) is True:

            dVector = self.__directionsVector["SW"]

            actorH = self.__ES

        else:

            dVector = self.__directionsVector["S"]

            actorH = self.__S

        actor.setH(actorH)

        actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        print actor, "currY : ", actor.getY()

        return task.cont

    #########################################

    def __actor_move_backward(self, actor, task):

        dt = self.__clock.getDt()

        actorH = None
        #actor.setY(actor.getY() + dt * self.__actorMoveSpeed)

        if self.check_effectSwitch(ACTOR_MOVE_LEFT) is True:

            dVector = self.__directionsVector["NE"]

            actorH = self.__WN

        elif self.check_effectSwitch(ACTOR_MOVE_RIGHT) is True:

            dVector = self.__directionsVector["WN"]

            actorH = self.__NE

        else:

            dVector = self.__directionsVector["N"]

            actorH = self.__N

        actor.setH(actorH)

        actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        print actor, "currY : ", actor.getY()

        return task.cont

    #########################################

    def __actor_move_left(self, actor, task):

        dt = self.__clock.getDt()
        dVector = None
        actorH = None

        if self.check_effectSwitch(ACTOR_MOVE_FORWARD) is True:

            dVector = self.__directionsVector["NE"]

            actorH = self.__SW

        elif self.check_effectSwitch(ACTOR_MOVE_BACKWARD) is True:

            dVector = self.__directionsVector["ES"]

            actorH = self.__WN

        else:

            dVector = self.__directionsVector["E"]

            actorH = self.__W

        actor.setH(actorH)

        actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        print actor, "currX : ", actor.getX()

        return task.cont

    #########################################

    def __actor_move_right(self, actor, task):

        dt = self.__clock.getDt()

        actorH = None

        if self.check_effectSwitch(ACTOR_MOVE_FORWARD) is True:

            dVector = self.__directionsVector["WN"]

            actorH = self.__ES

        elif self.check_effectSwitch(ACTOR_MOVE_BACKWARD) is True:

            dVector = self.__directionsVector["SW"]

            actorH = self.__NE

        else:

            dVector = self.__directionsVector["W"]

            actorH = self.__E

        actor.setH(actorH)

        actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        print actor, "currX : ", actor.getX()

        return task.cont

    #########################################

    def __actor_attack(self, args, task):

        return task.cont

    #########################################

    def __actor_be_attacked(self, args, task):

        return task.cont

    def __actor_talk(self, args, task):

        return task.cont

    #########################################

    def check_effectSwitch(self, key):

        return SeriousTools.find_value_in_dict(key, self.__effectSwitch)

    def set_clock(self, clock):

        self.__clock = clock

    def get_clock(self, clock):

        return self.__clock

    def set_actorMoveSpeed(self, speed):

        self.__actorMoveSpeed = speed

    def get_actorMoveSpeed(self):

        return self.__actorMoveSpeed

    def get_actorId(self, actor):

        return self.get_resId(actor)

    def get_actor(self, actorId):

        return self.get_res(actorId)

    def get_arcPkg(self):

        return self.__arcPkg

    def get_eventActionRecord(self):

        return self.__eventActionRecord

    def get_eventEffertRecord(self):

        return self.__eventEffertRecord
