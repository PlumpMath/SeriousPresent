# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-26
#
# This tutorial play music and adjust volume

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectButton import DirectButton
from direct.interval.SoundInterval import SoundInterval


class MySound(DirectObject):
    # 载入所有音乐与音效
    def __init__(self):

        self.__music=dict()
        self.__music["background"]=loader.loadMusic("../../resources/music/test.mp3")#背景音乐
        self.__music["battle"] = loader.loadSfx('../../resources/music/openclose.ogg')#战斗音效
        self.__music["peace"] = loader.loadSfx('../../resources/music/openclose.ogg')#平时音效
        self.__music["dialogue"] = loader.loadSfx('../../resources/music/openclose.ogg')#对话音效
        self.__music["shot"] = loader.loadSfx('../../resources/music/openclose.ogg')#枪击音效
        self.__music["load"] = loader.loadSfx('../../resources/music/openclose.ogg')#载入游戏音效
        self.__music["exit"] = loader.loadSfx('../../resources/music/openclose.ogg')#退出游戏音效

        self.__music["background"].setVolume(0.5)
        self.__music["background"].setLoop(True)

        self.__volume=0.5#滑动条值

        self.__musicTime = 0#背景音乐所处时间

        self.__musicOpen = True

        self.__music["background"].play()


    #初始化声音滑动条，开关声音按钮
    def volume_slider(self):
        self.__sliderText = OnscreenText("Volume", pos=(0, 0.87), scale=0.07, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1))
        self.__slider = DirectSlider(pos=(-0.1, 0, 0.75), scale=0.8, value=0.5, command=self.setMusicBoxVolume)
        self.__musicButton = DirectButton(pos=(0.9, 0, 0.75), text="Close", scale=0.1, pad=(0.2, 0.2), rolloverSound=None,
                                     clickSound=None, command=self.toggleMusicBox)

        self.__slider['value']=self.__volume

    #移除所有控件
    def destroy(self):
        self.__volume=self.__slider['value']
        self.__slider.destroy()
        self.__sliderText.destroy()
        self.__musicButton.destroy()

    #设置背景音乐声音大小
    def setMusicBoxVolume(self):
        newVolume=self.__slider.guiItem.getValue()
        self.__music["background"].setVolume(newVolume)

    #开关背景音乐
    def toggleMusicBox(self):

        #关闭音乐
        if (self.__musicOpen==True):
            self.__musicTime=self.__music["background"].getTime()
            self.__music["background"].stop()
            self.__musicButton["text"]="Open"
        #开启音乐
        else:
            self.__music["background"].setTime(self.__musicTime)
            self.__music["background"].play()
            self.__musicButton["text"]="Close"

        self.__musicButton.setText()
        self.__musicOpen=not self.__musicOpen

    #播放战斗音效
    def play_battle_music(self):
        self.music["battle"].play()

    # 播放平时音效
    def play_peace_music(self):
        self.music["peace"].play()

    # 播放对话音效
    def play_dialogue_music(self):
        self.music["dialogue"].play()

    # 播放枪击音效
    def play_shot_music(self):
        self.music["shot"].play()

    # 播放载入游戏音效
    def play_load_music(self):
        self.music["load"].play()

    # 播放退出游戏音效
    def play_exit_music(self):
        self.music["exit"].play()



