# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-25
#
# This tutorial shows load plot and display

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib
import codecs

#读取对话文件
class LoadPlot(DirectObject):
    def __init__(self):

        #打开对话文件
        self.__file = open("D:/YCJ/test/test.txt", 'r')

        self.accept("a",self.dialogue_next)

    #初始化对话与人物头像
    def init_interface(self):
        # 显示对话内容
        self.__dialogue = OnscreenText("", pos=(0, -0.9), scale=0.07, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                       mayChange=True)
        # 人物头像
        self.__image = OnscreenImage(image='/e/YCJ/1.jpg', pos=(0, 0, 0), scale=0.5)
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

    #移除控件
    def destroy(self):
        self.__dialogue.destroy()
        self.__image.destroy()

    #读取下一句对话
    def dialogue_next(self):
        #按行读取文件
        line = self.__file.readline()
        line = line.strip('\n')
        index=0

        #去掉首三个字符
        if line[:3] == codecs.BOM_UTF8:
            line = line[3:]

        #分离角色与对话内容
        for f in line:
            index=index+1
            if(f==":"):
                break
        role=line[:index-1]
        dia=line[index:]

        #判断角色
        if role=="猎人":
            self.__image.setImage("/d/YCJ/test/1.jpg")
        elif role=="修女":
            self.__image.setImage("/d/YCJ/test/2.jpg")
        else:
            self.__image.setImage("/d/YCJ/test/3.jpg")

        self.__dialogue.setText(dia.decode('utf-8'))


