# -*- coding:utf-8 -*-

from res_manager import ResManager
from RoleModule.role_manager import RoleManager
from ArchiveModule.archive_package import ArchivePackage
import SeriousTools.SeriousTools as SeriousTools
from SeriousTools.effert_msg_dispatcher import EffertMsgDispatcher

from direct.actor.Actor import Actor
from direct.interval.ActorInterval import ActorInterval
from direct.showbase.MessengerGlobal import messenger

import math

# 角色行为常量
ACTOR_MOVE_FORWARD  = "actor_move_forward"
ACTOR_MOVE_BACKWARD = "actor_move_backward"
ACTOR_MOVE_LEFT     = "actor_move_left"
ACTOR_MOVE_RIGHT    = "actor_move_right"
ACTOR_ROTATE_CW     = "actor_rotate_cw"
ACTOR_ROTATE_CCW    = "actor_rotate_ccw"
ACTOR_ATTACK        = "actor_attack"
ACTOR_BE_ATTACKED   = "actor_be_attacked"
ACTOR_TALK          = "actor_talk"

# 角色事件常量
FIND_ENEMY      = "find_enemy"
FIND_NPC        = "find_npc"
FIND_ATTACHMENT = "find_attachment"
FIND_NOTHING    = "find_nothing"

ACTOR_EFFERT = [
    ACTOR_MOVE_FORWARD,
    ACTOR_MOVE_BACKWARD,
    ACTOR_MOVE_LEFT,
    ACTOR_MOVE_RIGHT,
    ACTOR_ROTATE_CW,
    ACTOR_ROTATE_CCW,
    ACTOR_ATTACK,
    ACTOR_BE_ATTACKED,
    ACTOR_TALK,
]

class ActorManager(ResManager):

    def __init__(self, resType = "actor"):

        ResManager.__init__(self, resType)

        self.__itvlMap = dict()

        self.__actorMoveSpeed = 10
        self.__actorRotateSpeed = 10

        self.__roleMgr = None

        self.__clock = None

        self.__playerMovingState = dict()

        self.__attackLock = False

        self.__effectSwitch = {
            ACTOR_MOVE_FORWARD  : False,
            ACTOR_MOVE_BACKWARD : False,
            ACTOR_MOVE_LEFT     : False,
            ACTOR_MOVE_RIGHT    : False,
            ACTOR_ROTATE_CW     : False,
            ACTOR_ROTATE_CCW    : False,
            ACTOR_ATTACK        : False,
            ACTOR_BE_ATTACKED   : False,
            ACTOR_TALK          : False,
        }

        self.__toggleEffert = {
            ACTOR_MOVE_FORWARD  : [self.__actor_move_forward, []],
            ACTOR_MOVE_BACKWARD : [self.__actor_move_backward, []],
            ACTOR_MOVE_LEFT     : [self.__actor_move_left, []],
            ACTOR_MOVE_RIGHT    : [self.__actor_move_right, []],
            ACTOR_ROTATE_CW     : [self.__actor_rotate_cw, []],
            ACTOR_ROTATE_CCW    : [self.__actor_rotate_ccw, []],
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

        self.__effertMsgDiptcr = EffertMsgDispatcher()

        self.__arcPkg = ArchivePackage(arcPkgName = "actor",
                                       itemsName = [
                                           "actorId",
                                           "actorPath",
                                           "actionsPath",
                                           "pos",
                                           "hpr",
                                           "scale",
                                           "parentId"
                                       ])
        self.__arcPkg.append_metaData(key = "toggleEvent")
        self.__arcPkg.append_metaData(key = "eventActionRecord")
        self.__arcPkg.append_metaData(key = "eventEffertRecord")

    """""""""""""""
    动态模型管理函数
    """""""""""""""

    # 加载动态模型
    def load_res(self,
                 resPath,
                 extraResPath,
                 _resId = None):

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
                                 method=self.__move_interval_loop,
                                 extraArgs=[toggleEvent, itvl])

                    # actor.accept(event=toggleEvent + "-repeat",
                    #             method=self.__interval_loop,
                    #             extraArgs=[toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-up",
                                method=self.__move_interval_stop,
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
                                 method=self.__move_interval_loop,
                                 extraArgs=[toggleEvent, itvl])

                    # actor.accept(event=toggleEvent + "-repeat",
                    #               method=self.__interval_loop,
                    #               extraArgs=[toggleEvent, itvl])

                    actor.accept(event=toggleEvent + "-up",
                                 method=self.__move_interval_stop,
                                 extraArgs=[toggleEvent, itvl, actor.getNumFrames(actionName)])

                    if self.__eventActionRecord.has_key(actorId) is False:

                        self.__eventActionRecord[actorId] = list()

                    self.__eventActionRecord[actorId].append([toggleEvent, actionName])

    #########################################

    isPlayerMoving = dict()

    # 循环Interval
    def __move_interval_loop(self, toggleEvent, itvl):

        self.__playerMovingState[toggleEvent] = True

        #print toggleEvent, " : ", self.__playerMovingState
        #print self.__directionsVector
        if not itvl.isPlaying():

            itvl.loop()

        # else:
        #
        #     print itvl, " Is Playing"

        #print toggleEvent + " happen"

        #messenger.send(toggleEvent + "_effect")

    #########################################

    # 停止Interval
    def __move_interval_stop(self, toggleEvent, itvl, endFrame):

        self.__playerMovingState[toggleEvent] = False

        currFrame = itvl.getCurrentFrame()

        #print toggleEvent, "-up : ", self.__playerMovingState
        # print "currFrame", currFrame
        # print "endFrame", endFrame

        if True not in self.__playerMovingState.values():

            if currFrame is not None:

                itvl.start(startT = currFrame / endFrame)

        #print toggleEvent + "-up happen"

        #messenger.send(toggleEvent + "_effect_end")

        #itvl.finish()

    #########################################

    #def __player_attack

    #########################################

    def __enemy_die_interval_play(self):

        pass

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

        print "In Method add_effect_to_actor : ", actor

        if actor is not None and effect in ACTOR_EFFERT:

            self.__effertMsgDiptcr.accept_msg(toggleEvent)
            #self.__effertMsgDiptcr.accept_msg(toggleEvent+"up")

            actor.accept(toggleEvent + "_effert", self.__turn_effect_switch, [effect, True])
            actor.accept(toggleEvent + "_effert_end", self.__turn_effect_switch, [effect, False])

            self.__toggleEffert[effect][1].append(actorId)

            #print self.__toggleEffert[effect]

            if self.__eventEffertRecord.has_key(actorId) is False:

                self.__eventEffertRecord[actorId] = list()

            self.__eventEffertRecord[actorId].append([toggleEvent, effect])

    #########################################

    def __turn_effect_switch(self, effect, onOrOff):

        print "turn '", effect, "' ", onOrOff

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

        player = self.__roleMgr.get_role("PlayerRole")

        self.__actorMoveSpeed = player.get_attr_value("runSpeed")
        self.__actorRotateSpeed = player.get_attr_value("rotateSpeed")

        for effect, switch in self.__effectSwitch.iteritems():

            if switch:

                print effect, " : ", switch

                for arg in self.__toggleEffert[effect][1]:

                    execTask = self.__toggleEffert[effect][0]

                    arg = self.get_actor(arg)

                    execTask(arg, task)

        self.__check_player_touch_area(task)

        return task.cont

    def __update_actor_direction(self):

        x = self.__directionsVector["N"].getX()
        y = self.__directionsVector["N"].getY()

        # f = open("ActorDirections.txt", "w")
        #
        # f.write(str(self.__directionsVector["N"]) + "\n")

        self.__N  = self.__camCtrlr.get_camToCtrl().getH()
        self.__NE = self.__N + 45
        self.__E  = self.__N + 90
        self.__ES = self.__N + 135
        self.__S  = self.__N + 180
        self.__SW = self.__N + 225
        self.__W  = self.__N + 270
        self.__WN = self.__N + 315

        # f.write(str(self.__N))
        # f.close()

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

        #messenger.send("update_camera")

        # if self.check_effectSwitch(ACTOR_MOVE_LEFT) is True:
        #
        #     dVector = self.__directionsVector["ES"]
        #
        #     actorH = self.__SW
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt * 0.5)
        #
        # elif self.check_effectSwitch(ACTOR_MOVE_RIGHT) is True:
        #
        #     dVector = self.__directionsVector["SW"]
        #
        #     actorH = self.__ES
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt * 0.5)
        #
        # else:
        #
        #     dVector = self.__directionsVector["S"]
        #
        #     actorH = self.__S
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        if self.__effectSwitch["actor_move_forward"] is True:

            dt = self.__clock.getDt()

            c = math.cos(actor.getH() * math.pi / 180 - math.pi / 2)
            s = math.sin(actor.getH() * math.pi / 180 - math.pi / 2)

            actor.setX(actor.getX() + c * dt * self.__actorMoveSpeed)
            actor.setY(actor.getY() + s * dt * self.__actorMoveSpeed)

        #actor.setH(actorH)

        #actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        #print actor, "currY : ", actor.getY()

        return task.cont

        #########################################

    def __actor_move_left(self, actor, task):

        #messenger.send("update_camera")

        # dt = self.__clock.getDt()
        # dVector = None
        # actorH = None
        #
        # if self.check_effectSwitch(ACTOR_MOVE_FORWARD) is True:
        #
        #     dVector = self.__directionsVector["ES"] #NE
        #
        #     actorH = self.__SW
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt * 0.5)
        #
        # elif self.check_effectSwitch(ACTOR_MOVE_BACKWARD) is True:
        #
        #     dVector = self.__directionsVector["NE"]#ES
        #
        #     actorH = self.__WN
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt * 0.5)
        #
        # else:
        #
        #     dVector = self.__directionsVector["E"]
        #
        #     actorH = self.__W
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)
        #
        # actor.setH(actorH)

           # actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        # print actor, "currX : ", actor.getX()

        # if self.__effectSwitch["actor_move_backward"] is True:
        #
        #     dt = self.__clock.getDt()
        #
        #     c = math.cos(actor.getH() * math.pi / 180 - math.pi / 2)
        #     s = math.sin(actor.getH() * math.pi / 180 - math.pi / 2)
        #
        #     actor.setX(actor.getX() - c * dt * self.__actorMoveSpeed)
        #     actor.setY(actor.getY() - s * dt * self.__actorMoveSpeed)

        return task.cont


    #########################################

    def __actor_move_backward(self, actor, task):

        #messenger.send("update_camera")

        # dt = self.__clock.getDt()
        #
        # actorH = None
        # #actor.setY(actor.getY() + dt * self.__actorMoveSpeed)
        #
        # if self.check_effectSwitch(ACTOR_MOVE_LEFT) is True:
        #
        #     dVector = self.__directionsVector["NE"]
        #
        #     actorH = self.__WN
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt * 0.5)
        #
        # elif self.check_effectSwitch(ACTOR_MOVE_RIGHT) is True:
        #
        #     dVector = self.__directionsVector["WN"]
        #
        #     actorH = self.__NE
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt * 0.5)
        #
        # else:
        #
        #     dVector = self.__directionsVector["N"]
        #
        #     actorH = self.__N
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)
        #
        # actor.setH(actorH)
        #
        # #actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        #print actor, "currY : ", actor.getY()

        if self.__effectSwitch["actor_move_backward"] is True:
            dt = self.__clock.getDt()

            c = math.cos(actor.getH() * math.pi / 180 - math.pi / 2)
            s = math.sin(actor.getH() * math.pi / 180 - math.pi / 2)

            actor.setX(actor.getX() - c * dt * self.__actorMoveSpeed)
            actor.setY(actor.getY() - s * dt * self.__actorMoveSpeed)

        return task.cont

    #########################################

    def __actor_move_right(self, actor, task):

        #messenger.send("update_camera")

        # dt = self.__clock.getDt()
        #
        # actorH = None
        #
        # if self.check_effectSwitch(ACTOR_MOVE_FORWARD) is True:
        #
        #     dVector = self.__directionsVector["SW"] #
        #
        #     actorH = self.__ES
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt * 0.5)
        #
        # elif self.check_effectSwitch(ACTOR_MOVE_BACKWARD) is True:
        #
        #     dVector = self.__directionsVector["WN"] #SW
        #
        #     actorH = self.__NE
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt * 0.5)
        #
        # else:
        #
        #     dVector = self.__directionsVector["W"]
        #
        #     actorH = self.__E
        #
        #     actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)
        #
        # actor.setH(actorH)

        #actor.setPos(actor.getPos() + dVector * self.__actorMoveSpeed * dt)

        #print actor, "currX : ", actor.getX()

        return task.cont

    #########################################

    # 角色顺时针旋转
    def __actor_rotate_cw(self, actor, task):

        dt = self.__clock.getDt()

        actor.setH(actor.getH() + self.__actorRotateSpeed * dt)
        print "the actor rotate cw : ", actor.getH()
        return task.cont

    # 角色逆时针旋转
    def __actor_rotate_ccw(self, actor, task):

        dt = self.__clock.getDt()

        actor.setH(actor.getH() - self.__actorRotateSpeed * dt)
        print "the actor rotate ccw : ", actor.getH()
        return task.cont

    #########################################

    #########################################

    def __actor_attack(self, args, task):

        return task.cont

    #########################################

    def __actor_be_attacked(self, args, task):

        return task.cont

    def __actor_talk(self, args, task):

        return task.cont

    #def __actor

    # 监测玩家角色可触碰区域内的其他角色, 监测到的不同事件具有不同优先级
    # 优先级1：发现Enemy
    # 优先级2：发现NPC
    # 优先级3：发现Attachment
    def __check_player_touch_area(self, task):

        playerRole = self.__roleMgr.get_role("PlayerRole")

        touchRadius = playerRole.get_attr_value("touchRadius")

        player = self.get_actor(playerRole.get_attr_value("modelId"))

        playerPos = player.getPos()

        # 首先监测Enemy
        enemies = self.__roleMgr.get_one_kind_of_roles("EnemyRole")

        for enemyRole in enemies:

            enemy = self.get_actor(enemyRole.get_attr_value("modelId"))

            enemyPos = enemy.getPos()

            dVector = playerPos - enemyPos
            dVector.setZ(0)

            #print "playerPos:", playerPos, " enemyPos:", enemyPos, " dVector length:", dVector.length()

            if dVector.length() <= touchRadius:

                messenger.send(FIND_ENEMY)

                return task.cont

        # 然后监测NPC
        NPCs = self.__roleMgr.get_one_kind_of_roles("NPCRole")

        for NPCRole in NPCs:

            NPC = self.get_actor(NPCRole.get_attr_value("modelId"))

            NPCPos = NPC.getPos()

            dVector = playerPos - NPCPos
            dVector.setZ(0)

            #print "playerPos:", playerPos, " enemyPos:", NPCPos, " dVector length:", dVector.length()

            if dVector.length() <= touchRadius:

                messenger.send(FIND_NPC)

                return task.cont

        # 最后监测Attachment
        attachments = self.__roleMgr.get_one_kind_of_roles("AttachmentRole")

        for attachmentRole in attachments:

            attachment = self.get_actor(attachmentRole.get_attr_value("modelId"))

            attachmentPos = attachment.getPos()

            dVector = playerPos - attachmentPos
            dVector.setZ(0)

            #print "playerPos:", playerPos, " enemyPos:", attachmentPos, " dVector length:", dVector.length()

            if dVector.length() <= touchRadius:

                messenger.send(FIND_ATTACHMENT)

                return task.cont

        messenger.send(FIND_NOTHING)

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

    def set_toggleEffert(self, toggleEffert):

        self.__toggleEffert = toggleEffert

    def get_toggleEffert(self):

        return self.__toggleEffert

    def set_eventActionRecord(self, eventActionRecord):

        self.__eventActionRecord = eventActionRecord

    def get_eventActionRecord(self):

        return self.__eventActionRecord

    def set_eventEffertRecord(self, eventEffertRecord):

        self.__eventEffertRecord = eventEffertRecord

    def get_eventEffertRecord(self):

        return self.__eventEffertRecord