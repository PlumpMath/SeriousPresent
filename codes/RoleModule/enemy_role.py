# -*- coding:utf-8 -*-

from role_base import Role

class EnemyRole(Role):

    def __init__(self, modelId):


        Role.__init__(self,
                      roleId="EnemyRole",
                      modelId=modelId,
                      ableToTalk=False,
                      ableToCtrl=False,
                      ableToAtck=True,
                      )

        self.append_role_attr(key="hp", value=0)
        self.append_role_attr(key="attackForce", value=0)
        self.append_role_attr(key="walkSpeed", value=0)
        self.append_role_attr(key="runSpeed", value=0)
        self.append_role_attr(key="actions", value=dict())