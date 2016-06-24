# -*- coding:utf-8 -*-

from Role import Role

class PlayerRole(Role):

    def __init__(self,
                 name,
                 modelId,
                 actions,
                 hp,
                 attachments,
                 pos = (0, 0, 0)):


        Role.__init__(self,
                      name=name,
                      pos=pos,
                      modelId=modelId,
                      living=True,
                      ableToTalk=True,
                      ableToCtrl=True,
                      ableToAtck=True,
                      actions=actions)

        self.append_role_attr(key="hp", value=hp)
        self.append_role_attr(key="attachments", value=attachments)

