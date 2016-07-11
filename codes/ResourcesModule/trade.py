# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-07-09

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *


class Trade(DirectObject):
    def __init__(self):
        self.__imagePath = "../../resources/images/trade/"

        self.__imageDict=dict()
        self.__imageDict["tf"]=self.__imagePath+"trade_frame.png"
        self.__imageDict["tfbg"] = self.__imagePath + "trade_frame_bg.png"
        self.__imageDict["purchase1"] = self.__imagePath + "btn_perchase_0.png"
        self.__imageDict["purchase2"] = self.__imagePath + "btn_perchase_1.png"
        self.__imageDict["btnUp"] = self.__imagePath + "btn_up.png"
        self.__imageDict["btnDown"] = self.__imagePath + "btn_down.png"
        self.__imageDict["close"]=self.__imagePath+"close.png"

        self.__tradeMedicineNumber=0
        self.__tradeGun1Number = 0
        self.__tradeGun2Number = 0
        self.__medicineUnitPrice=800
        self.__gun1UnitPrice = 800
        self.__gun2UnitPrice = 800

        self.__medicineTotalPrice=0
        self.__gun1TotalPrice = 0
        self.__gun2TotalPrice = 0

        self.__totalPrice=0

        self.__destroyTrade=False

        self.__purchaseMedicineNumber = 0
        self.__purchaseMoney = 0


    def show(self):
        if self.__destroyTrade==False:
            #实际购买所花费钱数，药品数量
            self.__purchaseMedicineNumber=0
            self.__purchaseMoney=0
            # 购买数量
            self.__tradeMedicineNumber = 0
            self.__tradeGun1Number = 0
            self.__tradeGun2Number = 0
            #分别购买钱数
            self.__medicineTotalPrice = 0
            self.__gun1TotalPrice = 0
            self.__gun2TotalPrice = 0
            #总钱数
            self.__totalPrice = 0

            #交易背景
            self.__tradeFrame=OnscreenImage(image=self.__imageDict["tf"], pos=(0.0,0.0,0.0),scale=(1.0, 0, 0.5))
            self.__tradeFrame.setTransparency(TransparencyAttrib.MAlpha)

            #交易药品输入框
            self.__tradeMedicine = DirectEntry(text="", scale=.042,width=2.0, pos=(-0.71, 0.0, -0.005),text_scale=1.2,
                                               numLines=1, focus=0, text_fg=(0.5, 0.5, 0.5,1),frameColor=(0,0,0,0),initialText="0",
                                               command=self.set_medicine_total_price)
            #增加药品按钮
            self.__medicineUpBtn = DirectButton(pos=(-0.625, 0, 0.03), text="", scale=(0.035, 0, 0.035),
                                               command=self.__add_medicine,
                                               image=self.__imageDict["btnUp"],
                                               frameColor=(0, 0, 0, 0))
            self.__medicineUpBtn.setTransparency(TransparencyAttrib.MAlpha)
            #减少药品按钮
            self.__medicineDownBtn = DirectButton(pos=(-0.625, 0, -0.02), text="", scale=(0.035, 0, 0.029),
                                                command=self.__minus_medicine,
                                                image=self.__imageDict["btnDown"],
                                                frameColor=(0, 0, 0, 0))
            self.__medicineDownBtn.setTransparency(TransparencyAttrib.MAlpha)

            #交易枪支1输入框
            self.__tradeGun1 = DirectEntry(text="12", scale=.042, width=2.0, pos=(-0.17, 0.0, -0.005), text_scale=1.2,
                                           numLines=1, focus=0, text_fg=(0.5, 0.5, 0.5, 1), frameColor=(0, 0, 0, 0),initialText="0",
                                           command=self.set_gun1_total_price)
            #增加枪支1按钮
            self.__gun1UpBtn = DirectButton(pos=(-0.08, 0, 0.03), text="", scale=(0.035, 0, 0.035),
                                                command=self.__add_gun1,
                                                image=self.__imageDict["btnUp"],
                                                frameColor=(0, 0, 0, 0))
            self.__gun1UpBtn.setTransparency(TransparencyAttrib.MAlpha)
            #减少枪支1按钮
            self.__gun1DownBtn = DirectButton(pos=(-0.08, 0, -0.02), text="", scale=(0.035, 0, 0.029),
                                                  command=self.__minus_gun1,
                                                  image=self.__imageDict["btnDown"],
                                                  frameColor=(0, 0, 0, 0))
            self.__gun1DownBtn.setTransparency(TransparencyAttrib.MAlpha)

            #交易枪支2输入框
            self.__tradeGun2 = DirectEntry(text="12", scale=.042, width=2.0, pos=(0.38, 0.0, -0.005), text_scale=1.2,
                                           numLines=1, focus=0, text_fg=(0.5, 0.5, 0.5, 1), frameColor=(0, 0, 0, 0),initialText="0",
                                           command=self.set_gun2_total_price)
            #增加枪支2按钮
            self.__gun2UpBtn = DirectButton(pos=(0.46, 0, 0.03), text="", scale=(0.035, 0, 0.035),
                                            command=self.__add_gun2,
                                            image=self.__imageDict["btnUp"],
                                            frameColor=(0, 0, 0, 0))
            self.__gun2UpBtn.setTransparency(TransparencyAttrib.MAlpha)
            #减少枪支2按钮
            self.__gun2DownBtn = DirectButton(pos=(0.46, 0, -0.02), text="", scale=(0.035, 0, 0.029),
                                              command=self.__minus_gun2,
                                              image=self.__imageDict["btnDown"],
                                              frameColor=(0, 0, 0, 0))

            self.__gun2DownBtn.setTransparency(TransparencyAttrib.MAlpha)

            #药品单价显示框
            self.__medicineCoin = OnscreenText(str(self.__medicineUnitPrice), pos=(-0.45,-0.005), scale=0.06, fg=(0.5, 0.5, 0.5, 1), shadow=(0, 0, 0, 1),
                                                 mayChange=True)
            # 枪支1单价显示框
            self.__gun1Coin = OnscreenText(str(self.__gun1UnitPrice), pos=(0.09, -0.005), scale=0.06, fg=(0.5, 0.5, 0.5, 1), shadow=(0, 0, 0, 1),
                                               mayChange=True)
            # 枪支2单价显示框
            self.__gun2Coin = OnscreenText(str(self.__gun2UnitPrice), pos=(0.63, -0.005), scale=0.06, fg=(0.5, 0.5, 0.5, 1), shadow=(0, 0, 0, 1),
                                               mayChange=True)
            #购买物品总价
            self.__totalCoin = OnscreenText(str(self.__totalPrice), pos=(-0.01, -0.21), scale=0.06, fg=(0.5, 0.5, 0.5, 1), shadow=(0, 0, 0, 1),
                                           mayChange=True)
            #交易按钮
            self.__tradeBtn =  DirectButton(pos=(0.0, 0, -0.32), text="", scale=(0.15, 0, 0.07),
                                                     command=self.purchase,
                                                     image=(self.__imageDict["purchase1"],
                                                            self.__imageDict["purchase1"],
                                                            self.__imageDict["purchase2"]),
                                                     frameColor=(0, 0, 0, 0))
            self.__tradeBtn.setTransparency(TransparencyAttrib.MAlpha)

            self.__closeBtn = DirectButton(pos=(0.88, 0, 0.33), text="", scale=(0.035, 0, 0.035),
                                                command=self.destroy_trade,
                                                image=self.__imageDict["close"],
                                                frameColor=(0, 0, 0, 0))
            self.__closeBtn.setTransparency(TransparencyAttrib.MAlpha)

            self.__destroyTrade = True

    def destroy_trade(self):
        if self.__destroyTrade==True:
            self.__tradeFrame.destroy()
            self.__tradeMedicine.destroy()
            self.__medicineUpBtn.destroy()
            self.__medicineDownBtn.destroy()
            self.__tradeGun1.destroy()
            self.__gun1UpBtn.destroy()
            self.__gun1DownBtn.destroy()
            self.__tradeGun2.destroy()
            self.__gun2UpBtn.destroy()
            self.__gun2DownBtn.destroy()
            self.__medicineCoin.destroy()
            self.__gun1Coin.destroy()
            self.__gun2Coin.destroy()
            self.__totalCoin.destroy()
            self.__tradeBtn.destroy()
            self.__closeBtn.destroy()
            self.__destroyTrade=False


    #更新购买药品总价
    def set_medicine_total_price(self,textEntered):
        if (int(textEntered) <= 99 and int(textEntered)>=0):
            self.__tradeMedicineNumber=int(textEntered)
        else:
            self.__tradeMedicineNumber = 0
            self.__tradeMedicine.set(str(self.__tradeMedicineNumber))
        self.__medicineTotalPrice = self.__medicineUnitPrice * int(self.__tradeMedicineNumber)
        # self.__medicineCoin.setText(str(self.__medicineTotalPrice))
        self.__totalPrice = self.__medicineTotalPrice + self.__gun1TotalPrice + self.__gun2TotalPrice
        self.__totalCoin.setText(str(self.__totalPrice))

    # 更新购买枪支1总价
    def set_gun1_total_price(self, textEntered):
        if (int(textEntered) <= 1 and int(textEntered) >= 0):
            self.__tradeGun1Number = int(textEntered)
        else:
            self.__tradeGun1Number = 0
            self.__tradeGun1.set(str(self.__tradeGun1Number))
        self.__gun1TotalPrice = self.__gun1UnitPrice * int(self.__tradeGun1Number)
        # self.__gun1Coin.setText(str(self.__gun1TotalPrice))
        self.__totalPrice = self.__medicineTotalPrice + self.__gun1TotalPrice + self.__gun2TotalPrice
        self.__totalCoin.setText(str(self.__totalPrice))

    # 更新购买枪支2总价
    def set_gun2_total_price(self, textEntered):
        if (int(textEntered) <= 1 and int(textEntered) >= 0):
            self.__tradeGun2Number = int(textEntered)
        else:
            self.__tradeGun2Number = 0
            self.__tradeGun2.set(str(self.__tradeGun2Number))
        self.__gun2TotalPrice = self.__gun2UnitPrice * int(self.__tradeGun2Number)
        # self.__gun2Coin.setText(str(self.__gun2TotalPrice))
        self.__totalPrice = self.__medicineTotalPrice + self.__gun1TotalPrice + self.__gun2TotalPrice
        self.__totalCoin.setText(str(self.__totalPrice))

    # 增加药品数量
    def __add_medicine(self):
        if(self.__tradeMedicineNumber<=99):
            self.__tradeMedicineNumber += 1
            self.__tradeMedicine.set(str(self.__tradeMedicineNumber))
            self.set_medicine_total_price(str(self.__tradeMedicineNumber))

    # 减少药品数量
    def __minus_medicine(self):
        if(self.__tradeMedicineNumber>0):
            self.__tradeMedicineNumber -= 1
            self.__tradeMedicine.set(str(self.__tradeMedicineNumber))
            self.set_medicine_total_price(str(self.__tradeMedicineNumber))

    #增加枪支1数量
    def __add_gun1(self):
        if(self.__tradeGun1Number==0):
            self.__tradeGun1Number+=1
            self.__tradeGun1.set(str(self.__tradeGun1Number))
            self.set_gun1_total_price(str(self.__tradeGun1Number))

    #减少枪支1数量
    def __minus_gun1(self):
        if (self.__tradeGun1Number ==1):
            self.__tradeGun1Number -= 1
            self.__tradeGun1.set(str(self.__tradeGun1Number))
            self.set_gun1_total_price(str(self.__tradeGun1Number))

    # 增加枪支2数量
    def __add_gun2(self):
        if (self.__tradeGun2Number == 0):
            self.__tradeGun2Number += 1
            self.__tradeGun2.set(str(self.__tradeGun2Number))
            self.set_gun2_total_price(str(self.__tradeGun2Number))

    # 减少枪支2数量
    def __minus_gun2(self):
        if (self.__tradeGun2Number == 1):
            self.__tradeGun2Number -= 1
            self.__tradeGun2.set(str(self.__tradeGun2Number))
            self.set_gun2_total_price(str(self.__tradeGun2Number))

    def purchase(self):
        self.__purchaseMedicineNumber = self.__tradeMedicineNumber
        self.__purchaseMoney = self.__totalPrice
        self.destroy_trade()

    def get_purchase(self):
        medicineNumber = self.__purchaseMedicineNumber
        money = self.__purchaseMoney
        return [money , medicineNumber]

    def get_destroy_trade(self):
        return self.__destroyTrade

    def set_purchase_medicine_number(self):
        self.__purchaseMedicineNumber=0

    def set_purchase_money(self):
        self.__purchaseMoney=0
