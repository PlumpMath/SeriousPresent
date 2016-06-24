# -*- coding:utf-8 -*-

from PlayerRole import PlayerRole
from EnemyRole import EnemyRole
from NPCRole import NPCRole
from AttachmentRole import AttachmentRole

# 常量，表示角色类型
PLAYER_ROLE     = "PlayerRole"
ENEMY_ROLE      = "EnemyRole"
NPC_ROLE        = "NPCRole"
ATTACHMENT_ROLE = "AttachmentRole"

class RoleManager(object):

    def __init__(self):

        self.__roleType = [ PLAYER_ROLE,
                            ENEMY_ROLE,
                            NPC_ROLE,
                            ATTACHMENT_ROLE ]

        self.__roleModelMap = dict()
        self.__roleNameMap = dict()

    """""""""""
    角色创建函数
    """""""""""

    # 创建角色
    def create_role(self,
                    roleType,
                    name,
                    modelId,
                    actions,
                    attachments = None,
                    pos = (0, 0, 0),
                    hp=-1,
                    num = 1,):

        role = []

        if roleType is self.__roleType[0]:

            playerRole = PlayerRole(name = name,
                                    modelId = modelId,
                                    actions = actions,
                                    attachments = attachments,
                                    hp = hp,
                                    pos = pos)

            role.append(playerRole)

            self.__roleNameMap[name] = playerRole

        elif roleType is self.__roleType[1]:

            names = self.__gen_name_batch(name, num)

            for i in range(num):

                enemyRole = EnemyRole(name = names[i],
                                      modelId = modelId,
                                      actions = actions,
                                      hp = hp,
                                      attachments = attachments,
                                      pos = pos)

                role.append(enemyRole)

                self.__roleNameMap[names[i]] = enemyRole

        elif roleType is self.__roleType[2]:

            npcRole = NPCRole(name=name,
                              modelId=modelId,
                              actions=actions,
                              pos=pos)

            role.append(npcRole)

            self.__roleNameMap[name] = npcRole

        elif roleType is self.__roleType[3]:

            names = self.__gen_name_batch(name, num)

            for i in range(num):

                attachRole = AttachmentRole(name=names[i],
                                                modelId=modelId,
                                                pos=pos)

                role.append(attachRole)

                self.__roleNameMap[names[i]] = attachRole

        self.__roleModelMap[modelId] = role

        if len(role) == 1:

            return role[0]

        else:

            return role

    #####################

    # 批量生成角色名称，如"Zombie1"、"Zombie2"、"Zombie3"等
    def __gen_name_batch(self, namePrefix, num):

        names = []

        for i in range(num):

            names.append(namePrefix + str(i))

        return names

    """""""""""""""""""""
    读档存档的角色数据接口
    """""""""""""""""""""

    # 导入角色属性，用于读档
    def import_role_attr(self):
        pass

    #####################

    # 导出角色属性，用于存档
    def export_role_attr(self):
        pass

    """""""""""""""""""""
    成员变量的set和get函数
    """""""""""""""""""""

    def get_role_model(self, sceneMgr, modelId):

        return sceneMgr.get_res(modelId)

    def get_role(self, name):

        return self.__roleNameMap[name]

    def set_role_attr_value(self, name, key, value):

        if self.__roleNameMap[name] is not None:

            self.__roleNameMap[name].set_attr_value(key, value)

    def append_role_attr(self, name, key, value):

        if self.__roleNameMap[name] is not None:

            self.__roleNameMap[name].append_role_value(key, value)

    def get_roleModelMap(self):

        return self.__roleModelMap

    def get_roleNameMap(self):

        return self.__roleNameMap

    """""""""""
    角色信息打印
    """""""""""

    def print_roleModelMap(self):

        print "--Role Model Map--"

        for modelId in self.__roleModelMap.keys():

            print modelId, " : ", self.__roleModelMap[modelId]

        print "--------------------"

    def print_roleNameMap(self):

        print "--Role Name Map--"

        for name in self.__roleNameMap.keys():

            print name, " : ", self.__roleNameMap[name]

        print "--------------------"

    def destroy_role(self, role):
        pass




