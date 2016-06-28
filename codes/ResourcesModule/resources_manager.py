# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-28
#
# This tutorial shows resource module interface,

from load_plot import LoadPlot
from media_player import MediaPlayer
from sound import MySound

class ResourcesManager(object):

    #初始化
    def __init__(self):

        self.__sound = MySound()

        self.__dialogueFile = LoadPlot()

        self.__media=MediaPlayer()


    """""""""""
    音乐播放函数
    """""""""""

    #开关背景音乐
    def play_background_music(self):

        self.__sound.toggleMusicBox()

    #播放战斗音效
    def play_battle_music(self):
        self.__sound.play_battle_music()

    #播放平时音效
    def play_peace_music(self):
        self.__sound.play_peace_music()

    #播放对话音效
    def play_dialogue_music(self):
        self.__sound.play_dialogue_music()

    #播放枪击音效
    def play_shot_music(self):
        self.__sound.play_shot_music()

    #播放加载游戏音效
    def play_load_music(self):
        self.__sound.play_load_music()

    #播放退出游戏音效
    def play_exit_music(self):
        self.__sound.play_exit_music()

    #加载声音控制滑动条控件
    def show_volume_sliderbar(self):
        self.__sound.volume_slider()

    #移除滑动条等有关声音的控件
    def destroy_volume_sliderbar(self):
        self.__sound.destroy()

    """""""""""
    视频函数
    """""""""""

    #播放视频文件
    #fileName:视频文件路径
    def play_media(self,fileName):
        self.__media.playMedia(fileName)

    #移除视频控件
    def destroy_media(self):
        self.__media.destroy()

    """""""""""
    对话函数
    """""""""""

    #加载对话框，选择对话id
    #part:剧情对话id
    def show_dialog(self,part):
        self.__dialogueFile.init_interface()
        self.__dialogueFile.selectPart(part)

    #读取下一句对话
    def dialog_next(self):
        self.__dialogueFile.dialogue_next()

    #移除对话框等控件
    def destroy_dialog(self):
        self.__dialogueFile.destroy()

    """""""""""
    游戏存档读档函数
    """""""""""

    def save_archives(self):
        pass

    def select_archives(self):
        pass


