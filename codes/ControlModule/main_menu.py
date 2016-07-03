# -*-coding:utf-8 -*-
# Author: codingblack
# Last Updated: 2016-06-29
# menu菜单
# 游戏的开始界面
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from ResourcesModule.resources_manager import ResourcesManager
from keyboard_mouse_handler import *
from serious_state_manager import SeriousFSM

class MainMenu(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("Exit",self.__exit)
        self.__rm = ResourcesManager()

    # 菜单界面
    def start(self):
        #全屏
        self.setFullScreen(0)

        #load background image
        self.__image = OnscreenImage(image='../../resources/images/menu/home1.png',scale=1)
        self.__image.setSx(self.getAspectRatio())
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

        # 监听输入
        self.__keyInput = MenuPlayerInputHandler()
        self.accept("NewGame",self.__new_game)
        self.accept("LoadGame",self.__load_game)
        self.accept("Description",self.__description)
        self.accept("ChangeMenu",self.__change_menu)

    # 设置全屏
    def setFullScreen(self,full):
        if full == 1 :
            self.__setFullscreen(2560,1600,0,0,1)
        else:
            self.__setFullscreen(800,600,150,50,0)

    # 清除界面，清除监听
    def destroy(self):
        self.__image.destroy()
        self.__keyInput.destroy()

    # 私有函数，选择全屏
    def __setFullscreen(self, width, height, posX, posY, full):
        winProps = WindowProperties()
        winProps.setOrigin(posX, posY)
        winProps.setSize(width, height)
        winProps.setFullscreen(full)
        self.win.requestProperties(winProps)

    # 私有函数，进入新建游戏界面
    def __new_game(self):
        print '进入new game'
        messenger.send("serious_new_game")
        print '发送了serious_new_game'

    # 私有函数，进入读取游戏界面
    def __load_game(self):
        print '进入load game'
        messenger.send("serious_load_game")
        print '发送了serious_load_game'

    # 私有函数，进入about界面
    def __description(self):
        print '进入description'
        messenger.send("serious_description")
        print '发送了serious_description'

    # 私有函数，用来自建的选择进入的游戏界面
    def __change_mode(self,image_path):
        self.__image.setImage(image_path)

    def __exit(self):
        print '进入exit'
        # self.__del__()
        exit()

    # 私有函数，更改游戏目录
    def __change_menu(self):
        switch_count = {0:'../../resources/images/menu/home1.png',
                        1:'../../resources/images/menu/home2.png',
                        2:'../../resources/images/menu/home3.png',
                        3:'../../resources/images/menu/home4.png',}
        self.__change_mode(switch_count[self.__keyInput.get_count()])
