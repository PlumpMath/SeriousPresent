# -*-coding:utf-8 -*-

#!/usr/bin/env python

# Author: Yang chenjing
# Last Updated: 2016-06-28
#
# This tutorial save or select archives

import sys
sys.path.append('../')

from SceneModule.scene_manager import SceneManager
from ArchiveModule.archive_package import ArchivePackage

import json
import time
from panda3d.core import LPoint3f
from panda3d.core import LVecBase3f
from panda3d.core import LVecBase4f

class Archives(object):
    def __init__(self):
        self.__archiveFilePath="../../resources/files/archives.txt"#存档文件路径

        self.__archives=list()#存档内容。数组多条

        self.__showArchives=list()#存档界面展示内容

        self.__loadSceneArchive=dict()#需要加载的场景存档
        self.__loadRoleArchive=dict()#需要加载的角色存档
        # self.__scene=SceneManager()
        # self.save_archive(self.__scene.export_sceneArcPkg())


    #存档界面展示存档
    def show_archives(self):
        for i in range(len(self.__archives)):
            self.__showArchives[i]=dict()
            self.__showArchives[i]["id"]=self.__archives[i]["id"]
            self.__showArchives[i]["name"] = self.__archives[i]["name"]
            self.__showArchives[i]["time"] = self.__archives[i]["time"]

        return self.__showArchives

    def click_archive(self,id):
        if id==0 :
            pass
        else :
            for i in range(len(self.__archives)):
                if (self.__archives[i]["id"] == id):
                    self.__loadSceneArchive = self.__archives[i]["content"]["scene"]
                    # self.__loadRoleArchive = self.__archives[i]["content"]["role"]

    #存档
    def save_archive(self,sceneArchive,id,archiveName):
        if id==0 :
            id = len(self.__archives)+1
            self.new_archive(sceneArchive,id,archiveName)
            self.__archives.append(self.__archive)
        else:
            for i in range(len(self.__archives)):
                if (self.__archives[i]["id"] == id):
                    self.new_archive(sceneArchive,id,archiveName)
                    self.__archives[i]=self.__archive

        self.write_to_file()

    #新建存档
    def new_archive(self,sceneArchive,id,archiveName):
        #场景类存档
        self.__sceneArchive=dict()

        index = 0
        indexChar=0
        for lists in sceneArchive:
            name=lists.get_metaData()["ArchivePackageName"]
            self.__sceneArchive[name] = dict()
            self.__sceneArchive[name]["metaData"] = lists.get_metaData()
            self.__sceneArchive[name]["items"]= list()

            for i in range(len(lists.get_itemsData())):
                self.__sceneArchive[name]["items"].append(dict())
                for j in range(len(lists.get_itemsName())):
                    #去掉LPoint3f(0, 50, 5)前缀
                    indexChar = str((lists.get_itemsData())[i][j]).find("(")
                    #判断是否有前缀
                    if indexChar == -1:
                        itemData = (lists.get_itemsData())[i][j]
                    else:
                        data = str((lists.get_itemsData())[i][j])[indexChar+1 : -1]
                        itemData=list()
                        for item in data.split(','):
                            itemData.append(float(item))

                    self.__sceneArchive[name]["items"][i][(lists.get_itemsName())[j]] = itemData

            index = index+1

        #一条存档
        self.__archive=dict()
        self.__archive["id"] = id
        self.__archive["time"]=time.strftime('%Y/%m/%d %H:%M',time.localtime(time.time()))
        self.__archive["name"]=archiveName
        self.__archive["content"]=dict()
        self.__archive["content"]["scene"]=self.__sceneArchive
        # self.__archive["content"]["role"] = self.__role

        # self.select_archive(1)

        # print self.__archive["content"]["scene"]["camera"]

    #选择存档
    def select_archive(self,id):
        for i in range(len(self.__archives)):
            if(self.__archives[i]["id"]==id):
                self.__loadSceneArchive=self.__archives[i]["content"]["scene"]
                # self.__loadRoleArchive = self.__archives[i]["content"]["role"]
        self.read_archive()

    #读取档案，加载游戏
    def read_archive(self):
        self.__selectedSceneArchive=list()
        for name in self.__loadSceneArchive:
            arc=ArchivePackage(name,self.__loadSceneArchive[name]["items"][0].keys())
            for key in self.__loadSceneArchive[name]["metaData"]:
                arc.append_metaData(key,self.__loadSceneArchive[name]["metaData"][key])
            arc.__metaData=self.__loadSceneArchive[name]["metaData"]
            for index in range(len(self.__loadSceneArchive[name]["items"])):
                addItem=list()
                for key ,item in self.__loadSceneArchive[name]["items"][index].items():
                    if key == "pos":
                        item= LPoint3f(self.__loadSceneArchive[name]["items"][index][key][0],
                                       self.__loadSceneArchive[name]["items"][index][key][1],
                                       self.__loadSceneArchive[name]["items"][index][key][2])
                    elif key == "hpr":
                        item = LVecBase3f(self.__loadSceneArchive[name]["items"][index][key][0],
                                          self.__loadSceneArchive[name]["items"][index][key][1],
                                          self.__loadSceneArchive[name]["items"][index][key][2])
                    elif key == "scale":
                        item = LVecBase3f(self.__loadSceneArchive[name]["items"][index][key][0],
                                          self.__loadSceneArchive[name]["items"][index][key][1],
                                          self.__loadSceneArchive[name]["items"][index][key][2])
                    elif key == "color":
                        item = LVecBase4f(self.__loadSceneArchive[name]["items"][index][key][0],
                                          self.__loadSceneArchive[name]["items"][index][key][1],
                                          self.__loadSceneArchive[name]["items"][index][key][2],
                                          self.__loadSceneArchive[name]["items"][index][key][3])
                    addItem.append(item)
                    arc.add_item(addItem)
            self.__selectedSceneArchive.append(arc)

        # print self.__selectedSceneArchive[2].get_metaData()
        # print self.__selectedSceneArchive[2].get_itemsName()
        # print self.__selectedSceneArchive[2].get_itemsData()

    #将存档记录写入文件
    def write_to_file(self):
        encodedjson = json.dumps(self.__archives, indent=4)

        f = open("../../Resources/files/archives.txt", "w")
        f.write(encodedjson)
        f.close()

    #从文件中读取存档记录
    def read_from_file(self):
        with open(self.__archiveFilePath , 'r') as f:
            self.__archives=json.loads(f.read())

    def get_id(self):
        pass