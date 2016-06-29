# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-26
#
# This tutorial shows play meida interface

from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class MediaPlayer():

    #载入视频文件
    #fileName：视频文件路径
    #render:ShowBase属性，render2d
    def __init__(self):

        # Load the texture. We could use loader.loadTexture for this,
        # but we want to make sure we get a MovieTexture, since it
        # implements synchronizeTo.
        self.__mediaFileName=""
        self.__tex = MovieTexture("name")

    # 播放视频文件
    def playMedia(self,render,fileName):

        self.__mediaFileName = fileName
        success = self.__tex.read(self.__mediaFileName)
        # Set up a fullscreen card to set the video texture on.
        cm = CardMaker("My Fullscreen Card")
        cm.setFrameFullscreenQuad()

        # Tell the CardMaker to create texture coordinates that take into
        # account the padding region of the texture.
        cm.setUvRange(self.__tex)

        # Now place the card in the scene graph and apply the texture to it.
        card = NodePath(cm.generate())
        card.reparentTo(render)
        card.setTexture(self.__tex)

        self.__sound = loader.loadSfx(self.__mediaFileName)
        # Synchronize the video to the sound.
        self.__tex.synchronizeTo(self.__sound)

        self.__sound.play()

    #移除视频
    def destroy(self):
        # self.__tex.
        # self.__sound.
        pass


