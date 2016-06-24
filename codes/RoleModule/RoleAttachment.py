# -*- coding:utf-8 -*-

from Role import Role

class RoleAttachment(Role):

    def __init__(self,
                 name,
                 modelId,
                 pos):

        Role.__init__(self,
                      name = name,
                      modelId = modelId,
                      pos = pos,
                      living = False,
                      ableToTalk = False,
                      ableToCtrl = True,
                      ableToAtck = False,
                      actions = None)



