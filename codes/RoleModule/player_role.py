# -*- coding:utf-8 -*-

from role_base import Role

class PlayerRole(Role):

    def __init__(self,
                 name,
                 modelId
                 ):


        Role.__init__(self,
                      name = name,
                      roleId = "PlayerRole",
                      modelId = modelId,
                      ableToTalk = True,
                      ableToCtrl = True,
                      ableToAtck = True,
                      )

        self.append_role_attr(key = "hp", value = 100)
        self.append_role_attr(key = "attackForce", value = 10)
        self.append_role_attr(key = "moveSpeed", value = 10)
        self.append_role_attr(key = "actions", value = dict())
        self.append_role_attr(key = "attachments", value = dict())



    # 添加附属物
    def add_attachment(self):
        pass

