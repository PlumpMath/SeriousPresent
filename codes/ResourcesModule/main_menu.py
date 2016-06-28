# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-28
#
# This tutorial shows mainMemu interface,
# include begin new game and select archives operations.

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.DirectButton import DirectButton
from pandac.PandaModules import TransparencyAttrib
from panda3d.core import loadPrcFileData
from direct.task import Task
from resources_manager import ResourcesManager

# loadPrcFileData('', 'fullscreen 1')
loadPrcFileData('','win-size 1000 750')#设置窗口大小


class MainMenu(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        #load background image
        self.__image = OnscreenImage(image='../../resources/images/main_menu.jpg', pos=(0, 0, 0), scale=1)
        self.__image.setSx(self.getAspectRatio())
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

        #Three main opertaions
        self.__newGameButton = DirectButton(pos=(-0.9, 0, 0.5,), text=("新的游戏"), scale=0.1,
                                            command=self.new_game,frameColor=(0,0,0,0),
                                            image=("../../resources/images/main_menu.jpg","../../resources/images/main_menu.jpg",
                                                   "../../resources/images/main_menu.jpg"))
        self.__selectArchiveButton = DirectButton(pos=(-0.9, 0, 0.3,), text="选择存档", scale=0.1,text_fg=(1,1,1,1),
                                            command=self.select_archives, frameColor=(0, 0, 0, 0),
                                            image=("../../resources/images/main_menu.jpg", "../../resources/images/main_menu.jpg",
                                                   "../../resources/images/main_menu.jpg"))
        self.__exitGameButton = DirectButton(pos=(-0.9, 0, 0.1,), text="退出游戏", scale=0.1,text_fg=(1,1,1,1),
                                            command=self.exit_game, frameColor=(0, 0, 0, 0),
                                            image=("../../resources/images/main_menu.jpg", "../../resources/images/main_menu.jpg",
                                                   "../../resources/images/main_menu.jpg"))

        #add task to update background-image scale
        self.taskMgr.add(self.example_task, 'exampleTask')

        self.__rm=ResourcesManager()

    # 移除界面上的按钮与图片
    def destroy(self):
        self.__newGameButton.destroy()
        self.__selectArchiveButton.destroy()
        self.__exitGameButton.destroy()
        self.__image.destroy()
        self.taskMgr.remove('exampleTask')

    def new_game(self):
        self.destroy()
        self.__rm.show_volume_sliderbar()
        self.__rm.show_dialog(1)
        #调用对话
        # lp=LoadPlot()
        # lp.init_interface()
        #调用声音
        # ms=MySound()
        # ms.volume_slider()
        # 调用视频
        # mm=MediaPlayer('../../resources/media/PandaSneezes.ogv')
        # mm.playMedia(self.render2d)

    def select_archives(self):
        self.destroy()

    def exit_game(self):
        self.destroy()

    def example_task(self,task):
        self.__image.setSx(self.getAspectRatio())
        return Task.cont


mm=MainMenu()
mm.run()