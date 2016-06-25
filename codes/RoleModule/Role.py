# -*- coding:utf-8 -*-

class Role(object):

    def __init__(self,
                 name = None,
                 pos = (0, 0, 0),
                 modelId = None,
                 living = False,
                 ableToTalk = False,
                 ableToCtrl = False,
                 ableToAtck = False,
                 actions = None):

        self.__roleAttr = dict()

        self.__roleAttr["name"] = name               # 角色名字
        self.__roleAttr["pos"] = pos                 # 角色在游戏世界中的位置
        self.__roleAttr["modelId"] = modelId         # 角色模型ID
        self.__roleAttr["living"] = living           # 角色是否为有生命的角色
        self.__roleAttr["ableToTalk"] = ableToTalk   # 角色能否交流
        self.__roleAttr["ableToCtrl"] = ableToCtrl   # 角色能否被玩家控制
        self.__roleAttr["ableToAtck"] = ableToAtck   # 角色能否攻击
        self.__roleAttr["actions"] = actions         # 角色动作以及其对应触发事件

        if actions is None:
            self.__roleAttr["actions"] = dict()

    #########################################

    # 添加角色属性以及其对应值
    def append_role_attr(self, key, value):
        if key in self.__roleAttr.keys():
            print "the key '%s' in roleAttr is already existed" % key
        else:
            self.__roleAttr[key] = value

    #########################################

    # 设置属性值
    def set_attr_value(self, key, value):

        if key not in self.__roleAttr.keys():

            print "the key '%s' is not in roleAttr" % key

        else:

            self.__roleAttr[key] = value

    #########################################

    # 获取属性值
    def get_attr_value(self, key):

        return self.__roleAttr[key]

    # 获取所有属性
    def get_all_attr(self):

        return self.__roleAttr

    # 打印出所有属性以及其对应值
    def print_all_attr(self):

        print "-- Attribute of Role '%s' --" % self.__roleAttr["name"]

        for key in sorted(self.__roleAttr.keys()):

            print "key:%s, value:%s" % (key, self.__roleAttr[key])

        print "-------------------------"