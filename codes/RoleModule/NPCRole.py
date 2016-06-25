# -*- coding:utf-8 -*-

from Role import Role

class NPCRole(Role):

    def __init__(self,
                 name,
                 modelId,
                 actions,
                 pos=(0, 0, 0)):

        Role.__init__(self,
                      name = name,
                      pos = pos,
                      modelId = modelId,
                      living = True,
                      ableToTalk = True,
                      ableToCtrl = False,
                      ableToAtck = False,
                      actions = actions)




