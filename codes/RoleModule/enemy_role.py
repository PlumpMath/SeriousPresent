# -*- coding:utf-8 -*-

from role_base import Role

class EnemyRole(Role):

    def __init__(self, modelId, hp):


        Role.__init__(self,
                      roleId="EnemyRole",
                      modelId=modelId,
                      ableToTalk=False,
                      ableToCtrl=False,
                      ableToAtck=True,
                      )

        self.append_role_attr(key="hp", value=hp)
        self.append_role_attr(key="actions", value=dict())
        self.append_role_attr(key="attachments", value=dict())