# -*-coding:utf-8 -*-
import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from pandac.PandaModules import *

# add some text
# 添加一些文本
bk_text = "This is my Demo"
textObject = OnscreenText(text=bk_text, pos=(0.95, -0.95),
                          scale=0.07, fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter, mayChange=1)


# callback function to set  text
# 设置文本的回调函数
def setText(textEntered):
    textObject.setText(textEntered)


# clear the text
# 清除文本
def clearText():
    b.enterText('')


# add button
# 添加按钮
b = DirectEntry(text="", scale=.05, command=setText,
                initialText="Type Something", numLines=2, focus=0, focusInCommand=clearText)

# run the tutorial
# 运行教程
run()