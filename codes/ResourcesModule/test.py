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
from blood import Blood
import os
import Image, ImageFilter
from panda3d.core import *
from main import Main

from trade import Trade

# loadPrcFileData('', 'fullscreen 1')
loadPrcFileData('','win-size 1324 725')#设置窗口大小


class MainMenu(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.__image = OnscreenImage(image='../../resources/images/menu/home1.png', pos=(0, 0, 0), scale=1)
        self.__image.setSx(self.getAspectRatio())
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

        self.__main=Main()

        self.__trade=Trade()

        self.__yn=False

        self.__blood=100

        self.accept("a",self.show_main)
        self.accept("b", self.destroy_main)

        self.accept("c", self.__trade.show)

        self.taskMgr.add(self.example_task, 'exampleTask')

        self.accept("d",self.__main.addBlood)
        self.accept("e",self.__main.minusBlood)

    def show_main(self):
        if self.__yn==False:
            self.__main.show()
            self.__yn = True

    def destroy_main(self):
        if self.__yn == True:
            self.__main.destroy_main()
            self.__yn = False

    def example_task(self, task):
        # if self.__yn == True:
        #     self.__blood-=1
        #     self.__main.set_blood(self.__blood)

        if self.__trade.get_destroy_trade()==False and self.__yn==True:
            money=int(self.__main.get_money())
            medicineNumber=int(self.__main.get_medicine_number())
            spendMoney=int(self.__trade.get_purchase()[0])
            purchaseMedicine=int(self.__trade.get_purchase()[1])
            self.__main.set_money(str(money-spendMoney))
            self.__main.set_medicine_number((str(medicineNumber+purchaseMedicine)))
            self.__trade.set_purchase_medicine_number()
            self.__trade.set_purchase_money()
        return Task.cont


mm=MainMenu()
mm.run()