# coding=utf-8
from direct.fsm.FSM import FSM

class SeriousFSM(FSM):
    def __init__(self,window):
        FSM.__init__(self,'SeriousFSM')
        ### todo init
        self.__window = window

    def enterMenu(self):
        print '现在是菜单状态'
        self.__window.menu()
        
    def exitMenu(self):
        print '退出菜单状态'

    def enterGame(self):
        print '进入游戏状态'

    def exitGame(self):
        print '退出游戏状态'

    def enterSetting(self):
        print '进入设置界面'

    def exitSetting(self):
        print '退出设置界面'

# myFSM = SeriousFSM()
# myFSM.request('Walk')
# currentFSM = myFSM.state
# print '确定当前状态是:',currentFSM

# myFSM.request('Swim')
# currentFSM = myFSM.state
# print "确定当前状态是",currentFSM