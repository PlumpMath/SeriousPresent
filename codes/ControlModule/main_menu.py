# -*-coding:utf-8 -*-
# Author: codingblack
# Last Updated: 2016-06-29
#
# 游戏的开始界面

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from ResourcesModule.resources_manager import ResourcesManager
from keyboard_mouse_handler import *
from serious_state_manager import SeriousFSM


# # loadPrcFileData('', 'fullscreen 1')
# loadPrcFileData('','win-size 1000 750')#设置窗口大小


class MainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("Exit",self.__exit)
        self.__rm=ResourcesManager()
        self.__fsm = SeriousFSM(self)
        self.__fsm.request('Menu')


    # 移除界面上的按钮与图片
    def __destroy_menu(self):
        self.__image.destroy()
        self.__keyInput.destroy()

    def __new_game(self):
        self.__destroy_menu()
        self.__rm.show_volume_sliderbar()
        self.__rm.show_dialog(1)



    def __load_game(self):
        self.__destroy_menu()
        print '进入load game'


    def __description(self):
        self.__destroy_menu()
        print '进入description'

    def __exit(self):
        self.__destroy_menu()
        print '进入exit'
        # self.__del__()
        # exit()

    def __setFullscreen(self, width, height, posX, posY, full):
        winProps = WindowProperties()
        winProps.setOrigin(posX, posY)
        winProps.setSize(width, height)
        winProps.setFullscreen(full)
        self.win.requestProperties(winProps)

    def setFullScreen(self,full):
        if full == 1 :
            self.__setFullscreen(2560,1600,0,0,1)
        else:
            self.__setFullscreen(800,600,150,50,0)

    def menu(self):
        #全屏
        self.setFullScreen(0)

        #load background image
        self.__image = OnscreenImage(image='../../resources/images/menu/home1.png',
                                     scale=1)
        self.__image.setSx(self.getAspectRatio())
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

        self.__keyInput = MenuPlayerInputHandler()
        self.accept("NewGame",self.__new_game)
        self.accept("LoadGame",self.__load_game)
        self.accept("Description",self.__description)
