# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-07-09

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib
from direct.gui.DirectGui import *


class Main(DirectObject):
    def __init__(self):
        self.__imagePath = "../../resources/images/main/"

        self.__imageDict=dict()
        self.__imageDict["cbg"]=self.__imagePath+"charactor_bg.png"
        self.__imageDict["ctop"] = self.__imagePath + "charactor_top.png"
        self.__imageDict["charactor"] = self.__imagePath + "charactor3.png"
        self.__imageDict["hpbg"] = self.__imagePath + "hp_bg.png"
        self.__imageDict["hp"] = self.__imagePath + "hp.png"
        self.__imageDict["mf"] = self.__imagePath + "medicine_frame.png"
        self.__imageDict["medicine"] = self.__imagePath + "medicine.png"
        self.__imageDict["gf"] = self.__imagePath + "gun_frame.png"
        self.__imageDict["gun1"] = self.__imagePath + "gun_1.png"
        self.__imageDict["gun2"] = self.__imagePath + "gun_2.png"
        self.__imageDict["gun3"] = self.__imagePath + "gun_3.png"
        self.__imageDict["coin"] = self.__imagePath + "coin.png"

        self.__destroyMain=False

        self.__money=200000
        self.__medicineNum=10

        self.__blood=100

    def show(self):
        if self.__destroyMain==False:
            self.__charactorBg=OnscreenImage(image=self.__imageDict["cbg"], pos=(-1.6, 0, 0.8),scale=(0.16, 0, 0.16))
            self.__charactorBg.setTransparency(TransparencyAttrib.MAlpha)

            self.__charactorTop = OnscreenImage(image=self.__imageDict["ctop"], pos=(-1.6, 0, 0.8), scale=(0.16, 0, 0.16))
            self.__charactorTop.setTransparency(TransparencyAttrib.MAlpha)

            self.__charactor = OnscreenImage(image=self.__imageDict["charactor"], pos=(-1.6, 0, 0.8), scale=(0.15, 0, 0.15))
            self.__charactor.setTransparency(TransparencyAttrib.MAlpha)

            self.__hpBg = OnscreenImage(image=self.__imageDict["hpbg"], pos=(-1.14, 0, 0.85), scale=(0.30, 0, 0.02))
            self.__hpBg.setTransparency(TransparencyAttrib.MAlpha)

            # self.__hp = OnscreenImage(image=self.__imageDict["hp"], pos=(-1.14, 0, 0.85), scale=(0.30, 0, 0.02))
            # self.__hp.setTransparency(TransparencyAttrib.MAlpha)

            self.__hpBar=DirectWaitBar(text = "", value = 100, pos=(-1.14, 0, 0.85), scale=(0.297, 0, 0.22),
                                       barTexture=self.__imageDict["hp"],frameColor=(0,0,0,0))
            self.__hpBar.setTransparency(TransparencyAttrib.MAlpha)

            self.__medicineFrame = OnscreenImage(image=self.__imageDict["mf"], pos=(-1.33, 0, 0.72), scale=(0.09, 0, 0.09))
            self.__medicineFrame.setTransparency(TransparencyAttrib.MAlpha)

            self.__medicine = OnscreenImage(image=self.__imageDict["medicine"], pos=(-1.33, 0, 0.72), scale=(0.09, 0, 0.09))
            self.__medicine.setTransparency(TransparencyAttrib.MAlpha)

            self.__gunFrame = OnscreenImage(image=self.__imageDict["gf"], pos=(-0.95, 0, 0.72), scale=(0.27, 0, 0.09))
            self.__gunFrame.setTransparency(TransparencyAttrib.MAlpha)

            self.__gun = OnscreenImage(image=self.__imageDict["gun2"], pos=(-0.95, 0, 0.72), scale=(0.27, 0, 0.09))
            self.__gun.setTransparency(TransparencyAttrib.MAlpha)

            self.__coin = OnscreenImage(image=self.__imageDict["coin"], pos=(1.35, 0, 0.8), scale=(0.40, 0, 0.065))
            self.__coin.setTransparency(TransparencyAttrib.MAlpha)

            self.__medicineNumber = OnscreenText(str(self.__medicineNum), pos=(-1.27, 0.65), scale=0.05, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                       mayChange=True)

            self.__coinNumber = OnscreenText(str(self.__money), pos=(1.40, 0.78), scale=0.07, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                                 mayChange=True)

            self.__destroyMain=True

    def destroy_main(self):
        if self.__destroyMain==True:
            self.__charactorBg.destroy()
            self.__charactorTop.destroy()
            self.__charactor.destroy()

            self.__hpBg.destroy()
            self.__hpBar.destroy()
            # self.__hp.destroy()

            self.__medicineFrame.destroy()
            self.__medicine.destroy()
            self.__medicineNumber.destroy()

            self.__gunFrame.destroy()
            self.__gun.destroy()

            self.__coin.destroy()
            self.__coinNumber.destroy()

            self.__destroyMain=False

    def set_money(self,money):
        if money>=0:
            self.__money=money
            self.__coinNumber.setText(str(self.__money))

    def get_money(self):
        return self.__money

    def set_medicine_number(self, number):
        if number>=0:
            self.__medicineNum = number
            self.__medicineNumber.setText(str(self.__medicineNum))

    def get_medicine_number(self):
        return self.__medicineNum

    def set_gun1(self):
        self.__gun.setImage(self.__imageDict["gun1"])
        self.__gun.setTransparency(TransparencyAttrib.MAlpha)

    def set_gun2(self):
        self.__gun.setImage(self.__imageDict["gun2"])
        self.__gun.setTransparency(TransparencyAttrib.MAlpha)

    def set_gun3(self):
        self.__gun.setImage(self.__imageDict["gun3"])
        self.__gun.setTransparency(TransparencyAttrib.MAlpha)

    def addBlood(self):
        if(self.__hpBar['value']<100):
            self.__hpBar['value'] += 10

    def minusBlood(self):
        if (self.__hpBar['value'] >0):
            self.__hpBar['value'] -= 10

    def set_blood(self,blood):
        self.__blood=blood
        self.__hpBar['value']=self.__blood