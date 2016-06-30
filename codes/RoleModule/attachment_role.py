# -*- coding:utf-8 -*-

from role_base import Role

class AttachmentRole(Role):

    def __init__(self,
                 name,
                 modelId
                 ):


        Role.__init__(self,
                      name=name,
                      roleId="AttachmentRole",
                      modelId=modelId,
                      ableToTalk=False,
                      ableToCtrl=False,
                      ableToAtck=False,
                      )

        self.append_role_attr("")


