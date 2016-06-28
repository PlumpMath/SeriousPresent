# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-26
#
# This tutorial shows load plot and display

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import TransparencyAttrib
import codecs

#读取对话文件
class LoadPlot(DirectObject):
    def __init__(self):

        #打开对话文件
        self.__file = open("../../resources/files/dialogue.txt", 'r')

        self.__content = self.__file.readlines()
        self.__dialogueList = []  # 对话数组,id唯一标识

        self.__part = 0
        self.__index = 0

        self.dialogue_list()

        self.selectPart(1)

        self.accept("a",self.dialogue_next)

        self.init_tree()


    #初始化对话与人物头像
    def init_interface(self):
        # 显示对话内容
        self.__dialogue = OnscreenText("", pos=(0, -0.9), scale=0.07, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
                                       mayChange=True)
        # 人物头像
        self.__image = OnscreenImage(image='../../resources/images/1.jpg', pos=(0, 0, 0), scale=0.5)
        self.__image.setTransparency(TransparencyAttrib.MAlpha)

    #移除控件
    def destroy(self):
        self.__dialogue.destroy()
        self.__image.destroy()

    def dialogue_list(self):

        # 按行读取文件
        part = -1
        index = 0
        for line in self.__content:
            # 去掉首三个字符
            if line[:3] == codecs.BOM_UTF8:
                line = line[3:]

            # for f in line:
            if (line[4] == "1" or line[4] == "2" or line[4] == "3" or line[4] == "4" or line[4] == "5"
                or line[4] == "6" or line[4] == "7" or line[4] == "8" or line[4] == "9"):
                part=part+1
                self.__dialogueList.append({"id":part+1,"dialogue":[]})
                index = 0
                continue

            line = line.strip('\n')

            self.__dialogueList[part]["dialogue"].append(line)
            index=index+1

    #选择第几部分对话
    def selectPart(self,id):
        self.__part=id
        self.__index=1

    #读取下一句对话
    def dialogue_next(self):
        length=len(self.__dialogueList[self.__part-1]["dialogue"])
        if self.__index-1>=length:
            return
        line=self.__dialogueList[self.__part-1]["dialogue"][self.__index-1]
        char=0
        for f in line:
            char = char + 1
            if (f == ":"):
                break
        role = line[:char - 1]
        dia = line[char:]
        # 判断角色
        if role.decode('gb2312').encode('utf-8') == "猎人":
            self.__image.setImage("../../resources/images/1.jpg")
        elif role.decode('gb2312').encode('utf-8') == "修女":
            self.__image.setImage("../../resources/images/2.jpg")
        else:
            self.__image.setImage("../../resources/images/3.jpg")

        self.__dialogue.setText(dia.decode('gb2312'))

        self.__index = self.__index+1


    def init_tree(self):

        dialoguePart=[]
        for part in self.__dialogueList:
            dialoguePart.append(Node(part["id"]))

        print dialoguePart[1].get_data()

        index = 0
        # for node in dialoguePart:
        #     if(index<len(dialoguePart)-2):
        #         node.add(dialoguePart[index+1])
        dialoguePart[0].add(dialoguePart[1])
        dialoguePart[1].add(dialoguePart[2])
        dialoguePart[2].add(dialoguePart[3])
        dialoguePart[3].add(dialoguePart[4])
        dialoguePart[4].add(dialoguePart[5])
        dialoguePart[5].add(dialoguePart[6])
        dialoguePart[6].add(dialoguePart[7])
        dialoguePart[0].add(dialoguePart[8])

        dialogueTree = Tree()
        dialogueTree.link_to_head(dialoguePart[0])

        print 'Node', dialogueTree.search("123").get_data()
        print 'Node', dialogueTree.search("1234").get_data()
        print 'Node', dialogueTree.search("19").get_data()

class Node(object):
    def __init__(self,data):
        self.__data=data
        self.__children=[]

    def get_data(self):
        return self.__data

    def get_children(self):
        return self.__children

    def add(self,node):
        if len(self.__children)==4:
            return False
        else:
            self.__children.append(node)

    def go(self,data):
        for child in self.__children:
            if child.get_data()==int(data):
                return child
        return None

class Tree:
    def __init__(self):
        self.__head=Node('header')

    def link_to_head(self,node):
        self.__head.add(node)

    def insert(self,path,data):
        cur=self.__head
        for step in path:
            if cur.go(step)==None:
                return False
            else:
                cur=cur.go(step)
        cur.add(Node(data))
        return True

    def search(self,path):
        cur = self.__head
        for step in path:
            if cur.go(step) == None:
                return None
            else:
                cur = cur.go(step)
        return cur





