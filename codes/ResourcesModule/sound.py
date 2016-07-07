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
from pandac.PandaModules import TransparencyAttrib
from direct.interval.SoundInterval import SoundInterval
from panda3d.core import *


class MySound(DirectObject):
    # 载入所有音乐与音效
    def __init__(self):

        self.__music=dict()
        self.__music["1"]=loader.loadMusic("../../resources/music/test.mp3")#主界面背景音乐
        self.__music["2"] = loader.loadMusic('../../resources/music/test.mp3')#平时音乐
        self.__music["3"] = loader.loadMusic('../../resources/music/test.mp3')#战斗音乐
        # self.__music["4"] = loader.loadSfx('../../resources/music/openclose.ogg')#对话音效
        self.__music["4"] = loader.loadSfx('../../resources/music/openclose.ogg')#枪击音效
        self.__music["5"] = loader.loadSfx('../../resources/music/openclose.ogg')#载入游戏音效
        self.__music["6"] = loader.loadSfx('../../resources/music/openclose.ogg')#退出游戏音效

        #设置音乐与音效的音量
        for index in self.__music:
            self.__music[index].setVolume(0.5)

        # 设置音乐与音效的循环次数
        self.__music["1"].setLoop(0)
        self.__music["2"].setLoop(0)
        self.__music["3"].setLoop(0)
        self.__music["4"].setLoop(1)
        self.__music["5"].setLoop(1)
        self.__music["6"].setLoop(1)

        self.__volume=0.5#滑动条值

        self.__musicTime = 0#背景音乐所处时间

        self.__backgroundId=1#背景音乐ID

        self.__musicOpen = True#音乐是否开启

        self.__music["1"].play()#主界面背景音乐自动开启

        self.__destroy=False#是否可以移除控件


    #初始化暂停设置界面
    def init_setting(self,base):
        if self.__destroy==False:
            self.__image = OnscreenImage(image='../../resources/images/menu/home1.png', pos=(0, 0, 0), scale=1)
            self.__image.setSx(base.getAspectRatio())
            self.__image.setTransparency(TransparencyAttrib.MAlpha)

            #设置界面背景图
            self.__background = OnscreenImage(image='../../resources/images/settings/setting_frame.png', pos=(0, 0, 0), scale=(1.0,0,0.7))
            self.__background.setTransparency(TransparencyAttrib.MAlpha)

            ##滑动条
            self.__slider = DirectSlider(pos=(0.16, 0, 0.26), scale=0.5, value=0.5, command=self.setMusicBoxVolume,
                                         frameSize=(-1.0, 0.9, -0.06, 0.06) , image = '../../resources/images/settings/slide_bar.png',
                                         image_pos = (-0.05, 0, 0.0), image_scale = (1.0,0,0.05),
                                         thumb_image='../../resources/images/settings/slide_btn.png',
                                         thumb_image_pos=(-0.0, 0, 0.0),thumb_image_scale=0.1,thumb_frameSize=(0.0, 0.0,0.0, 0.0))
            self.__slider.setTransparency(TransparencyAttrib.MAlpha)


            # self.__musicButton = DirectButton(pos=(0.9, 0, 0.75), text="Close", scale=0.1, pad=(0.2, 0.2), rolloverSound=None,
            #                                   clickSound=None, command=self.toggleMusicBox,extraArgs=[base])

            #继续按钮
            self.__continueButton=DirectButton(pos=(-0.25, 0, 0.0), text="", scale=(0.2,0,0.1),command=self.continue_game,
                                               image=("../../resources/images/settings/btn_continue_0.png",
                                                      "../../resources/images/settings/btn_continue_0.png"
                                                      ,"../../resources/images/settings/btn_continue_1.png"),
                                               frameColor=(0,0,0,0))
            self.__continueButton.setTransparency(TransparencyAttrib.MAlpha)

            #存档按钮
            self.__saveButton = DirectButton(pos=(0.33, 0, 0.0), text="", scale=(0.2, 0, 0.1),command=self.save_game,
                                                 image=("../../resources/images/settings/btn_save_0.png",
                                                        "../../resources/images/settings/btn_save_0.png"
                                                        , "../../resources/images/settings/btn_save_1.png"),
                                                 frameColor=(0, 0, 0, 0))
            self.__saveButton.setTransparency(TransparencyAttrib.MAlpha)

            #帮助按钮
            self.__helpButton = DirectButton(pos=(-0.25, 0, -0.25), text="", scale=(0.2, 0, 0.1),command=self.help,
                                                 image=("../../resources/images/settings/btn_help_0.png",
                                                        "../../resources/images/settings/btn_help_0.png"
                                                        , "../../resources/images/settings/btn_help_1.png"),
                                                 frameColor=(0, 0, 0, 0))
            self.__helpButton.setTransparency(TransparencyAttrib.MAlpha)

            #回到主界面按钮
            self.__homeButton = DirectButton(pos=(0.33, 0, -0.25), text="", scale=(0.2, 0, 0.1),command=self.return_home,
                                                 image=("../../resources/images/settings/btn_home_0.png",
                                                        "../../resources/images/settings/btn_home_0.png"
                                                        , "../../resources/images/settings/btn_home_1.png"),
                                                 frameColor=(0, 0, 0, 0))
            self.__homeButton.setTransparency(TransparencyAttrib.MAlpha)

            #设置滑动条value
            self.__slider['value']=self.__volume

            self.__destroy=True

    #移除所有控件
    def destroy(self):
        if self.__destroy==True:
            self.__background.destroy()
            self.__volume=self.__slider['value']
            self.__slider.destroy()
            # self.__musicButton.destroy()
            self.__continueButton.destroy()
            self.__saveButton.destroy()
            self.__helpButton.destroy()
            self.__homeButton.destroy()
            self.__destroy=False

    #设置音乐声音大小
    def setMusicBoxVolume(self):
        print self.__slider.guiItem
        newVolume=self.__slider.guiItem.getValue()
        for index in self.__music:
            self.__music[index].setVolume(newVolume)

    #开关背景音乐
    def toggleMusicBox(self,base):

        #关闭音乐
        if (self.__musicOpen==True):
            base.disableAllAudio()
            # self.__musicButton["text"]="Open"
        #开启音乐
        else:
            base.enableAllAudio()
            self.__music[str(self.__backgroundId)].play()
            # self.__musicButton["text"]="Close"

        # self.__musicButton.setText()
        self.__musicOpen=not self.__musicOpen

    #播放音乐
    #id：音乐与音效id
    def play_music(self,id):
        if(id==1 or id==2 or id==3):
            self.__backgroundId=id
        id=str(id)
        self.__music[id].play()

    #关闭音乐
    def stop_music(self,id):
        id=str(id)
        self.__music[id].stop()

    #继续游戏
    def continue_game(self):
        self.destroy()

    #存档
    def save_game(self):
        self.destroy()

    #游戏帮助
    def help(self):
        self.destroy()

    #回到主界面
    def return_home(self):
        self.destroy()

    # #播放战斗音效
    # def play_battle_music(self):
    #     self.music["battle"].play()
    #
    # # 播放平时音效
    # def play_peace_music(self):
    #     self.music["peace"].play()
    #
    # # 播放对话音效
    # def play_dialogue_music(self):
    #     self.music["dialogue"].play()
    #
    # # 播放枪击音效
    # def play_shot_music(self):
    #     self.music["shot"].play()
    #
    # # 播放载入游戏音效
    # def play_load_music(self):
    #     self.music["load"].play()
    #
    # # 播放退出游戏音效
    # def play_exit_music(self):
    #     self.music["exit"].play()



