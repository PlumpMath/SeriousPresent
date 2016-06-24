# -*- coding:utf-8 -*-

# Author : 戴熹
#
# Last Updated : 2016-06-20
#
# Description : 相机控制器，为相机添加各种操作

# 定义常量
CAM_MOVE_FORWARD  = "move_forward"
CAM_MOVE_BACKWARD = "move_backward"
CAM_MOVE_LEFT     = "move_left"
CAM_MOVE_RIGHT    = "move_right"
CAM_MOVE_UP       = "move_up"
CAM_MOVE_DOWN     = "move_down"
CAM_ROTATE_H_CW   = "rotate_h_cw"
CAM_ROTATE_H_CCW  = "rotate_h_ccw"
CAM_ROTATE_P_CW   = "rotate_p_cw"
CAM_ROTATE_P_CCW  = "rotate_p_ccw"
CAM_ROTATE_R_CW   = "rotate_r_cw"
CAM_ROTATE_R_CCW  = "rotate_r_ccw"

class CameraController(object):

    def __init__(self, camera, clock):

        self.__camToCtrl = camera  # 所要进行控制的相机
        self.__clock = clock       # 全局时钟，偏移量的计算依赖于时钟
        self.__moveSpeed = 10      # 相机移动速度
        self.__rotateSpeed = 60    # 相机旋转速度

        self.__camCurrX = self.__camToCtrl.getX()
        self.__camCurrY = self.__camToCtrl.getY()
        self.__camCurrZ = self.__camToCtrl.getZ()
        self.__camCurrH = self.__camToCtrl.getH()
        self.__camCurrP = self.__camToCtrl.getP()
        self.__camCurrR = self.__camToCtrl.getR()

        self.__camMoveOffset = 0   # 相机单位时间的偏移量
        self.__camRotateOffset = 0 # 相机单位事件的旋转量

        # 每个控制选项所对应的函数
        self.__optsFunc = {
            CAM_MOVE_FORWARD  : self.__move_forward,
            CAM_MOVE_BACKWARD : self.__move_backward,
            CAM_MOVE_LEFT     : self.__move_left,
            CAM_MOVE_RIGHT    : self.__move_right,
            CAM_MOVE_UP       : self.__move_up,
            CAM_MOVE_DOWN     : self.__move_down,
            CAM_ROTATE_H_CW   : self.__rotate_h_cw,
            CAM_ROTATE_H_CCW  : self.__rotate_h_ccw,
            CAM_ROTATE_P_CW   : self.__rotate_p_cw,
            CAM_ROTATE_P_CCW  : self.__rotate_p_ccw,
            CAM_ROTATE_R_CW   : self.__rotate_r_cw,
            CAM_ROTATE_R_CCW  : self.__rotate_r_ccw
        }

        # 每个控制选项有两个开关，第一个是触发事件，第二个是开关函数
        self.__optsSwitch = {
            CAM_MOVE_FORWARD  : [False, True],
            CAM_MOVE_BACKWARD : [False, True],
            CAM_MOVE_LEFT     : [False, True],
            CAM_MOVE_RIGHT    : [False, True],
            CAM_MOVE_UP       : [False, True],
            CAM_MOVE_DOWN     : [False, True],
            CAM_ROTATE_H_CW   : [False, True],
            CAM_ROTATE_H_CCW  : [False, True],
            CAM_ROTATE_P_CW   : [False, True],
            CAM_ROTATE_P_CCW  : [False, True],
            CAM_ROTATE_R_CW   : [False, True],
            CAM_ROTATE_R_CCW  : [False, True]
        }

    def accept_event(self, key, value):
        self.__optsSwitch[key][0] = value

    #########################################

    # 相机总控制
    def camera_control(self, task):

        dt = self.__clock.getDt()

        self.__camMoveOffset = dt * self.__moveSpeed
        self.__camRotateOffset = dt * self.__rotateSpeed

        # 移动相机位置
        if self.__optsSwitch[CAM_MOVE_FORWARD][0] and \
                self.__optsSwitch[CAM_MOVE_FORWARD][1]:

            self.__move_forward()

        if self.__optsSwitch[CAM_MOVE_BACKWARD][0] and \
                self.__optsSwitch[CAM_MOVE_BACKWARD][1]:

            self.__move_backward()

        if self.__optsSwitch[CAM_MOVE_LEFT][0] and \
                self.__optsSwitch[CAM_MOVE_LEFT][1]:

            self.__move_left()

        if self.__optsSwitch[CAM_MOVE_RIGHT][0] and \
                self.__optsSwitch[CAM_MOVE_RIGHT][1]:

            self.__move_right()

        if self.__optsSwitch[CAM_MOVE_UP][0] and \
                self.__optsSwitch[CAM_MOVE_UP][1]:

            self.__move_up()

        if self.__optsSwitch[CAM_MOVE_DOWN][0] and \
                self.__optsSwitch[CAM_MOVE_DOWN][1]:

            self.__move_down()

        # 移动相机镜头方向
        if self.__optsSwitch[CAM_ROTATE_H_CW][0] and \
                self.__optsSwitch[CAM_ROTATE_H_CW][1]:

            self.__rotate_h_cw()

        if self.__optsSwitch[CAM_ROTATE_H_CCW][0] and \
                self.__optsSwitch[CAM_ROTATE_H_CCW][1]:

            self.__rotate_h_ccw()

        if self.__optsSwitch[CAM_ROTATE_P_CW][0] and \
                self.__optsSwitch[CAM_ROTATE_P_CW][1]:

            self.__rotate_p_cw()

        if self.__optsSwitch[CAM_ROTATE_P_CCW][0] and \
                self.__optsSwitch[CAM_ROTATE_P_CCW][1]:

            self.__rotate_p_ccw()

        if self.__optsSwitch[CAM_ROTATE_R_CW][0] and \
                self.__optsSwitch[CAM_ROTATE_R_CW][1]:

            self.__rotate_r_cw()

        if self.__optsSwitch[CAM_ROTATE_R_CCW][0] and \
                self.__optsSwitch[CAM_ROTATE_R_CCW][1]:

            self.__rotate_r_ccw()

        self.__update_camera()

        #print "pos : %s, hpr : %s" % (self.__camToCtrl.getPos(), self.__camToCtrl.getHpr())

        return task.cont

    # 相机跟踪物体
    def follow_object(self, target):
        pass

    """""""""""""""""
    相机控制选项开关函数
    """""""""""""""""

    # 开启控制选项
    def turn_on_ctrl_options(self, options=None):

        if options == None:

            for opt in self.__optsSwitch.keys():
                self.__optsSwitch[opt][1] = True

        else:

            for opt in options:
                if opt in self.__optsSwitch.keys():
                    self.__optsSwitch[opt][1] = True

    #########################################

    # 关闭控制选项
    def turn_off_ctrl_options(self, options=None):

        if options == None:

            for opt in self.__optsSwitch.keys():
                self.__optsSwitch[opt][1] = False

        else:

            for opt in options:
                if opt in self.__optsSwitch.keys():
                    self.__optsSwitch[opt][1] = False

    # 绑定设备输入
    def bind_input_to_(self, opt, inputEvent):

        if self.__optsFunc[opt] is not None:
            self.__optsFunc[opt][0] = inputEvent

    """""""""""""""""
    相机单个控制操作函数
    """""""""""""""""

    # 向前移动相机
    def __move_forward(self):

        self.__camCurrY -= self.__camMoveOffset

    # 向后移动相机
    def __move_backward(self):

        self.__camCurrY += self.__camMoveOffset

    # 向左移动相机
    def __move_left(self):

        self.__camCurrX += self.__camMoveOffset

    # 向右移动相机
    def __move_right(self):

        self.__camCurrX -= self.__camMoveOffset

    # 向上移动相机
    def __move_up(self):

        self.__camCurrZ += self.__camMoveOffset

    # 向下移动相机
    def __move_down(self):

        self.__camCurrZ -= self.__camMoveOffset

    # 绕Z轴顺时针旋转镜头
    def __rotate_h_cw(self):

        self.__camCurrH += self.__camRotateOffset

    # 绕Z轴逆时针旋转镜头
    def __rotate_h_ccw(self):

        self.__camCurrH -= self.__camRotateOffset

    # 绕X轴顺时针旋转镜头
    def __rotate_p_cw(self):

        self.__camCurrP += self.__camRotateOffset

    # 绕X轴逆时针旋转镜头
    def __rotate_p_ccw(self):

        self.__camCurrP -= self.__camRotateOffset

    # 绕Y轴顺时针旋转镜头
    def __rotate_r_cw(self):

        self.__camCurrR += self.__camRotateOffset

    # 绕Y轴逆时针旋转镜头
    def __rotate_r_ccw(self):

        self.__camCurrR -= self.__camRotateOffset

    # 移动至指定点
    def move_to(self, pos):

        self.__camCurrX = pos[0]
        self.__camCurrY = pos[1]
        self.__camCurrZ = pos[2]

    """""""""""""""
    相机状态更新函数
    """""""""""""""

    # 只有执行更新函数后相机的状态才会发生改变
    def __update_camera(self):

        self.__camToCtrl.setPos(self.__camCurrX,
                                self.__camCurrY,
                                self.__camCurrZ)

        self.__camToCtrl.setHpr(self.__camCurrH,
                                self.__camCurrP,
                                self.__camCurrR)

    """""""""""""""""""""
    成员变量的get和set函数
    """""""""""""""""""""

    # 相机的移动速度
    def set_moveSpeed(self, speed):

        self.__moveSpeed = max(speed, 0.0)

    def get_moveSpeed(self):

        return self.__moveSpeed

    # 相机的旋转速度
    def set_rotateSpeed(self, speed):

        self.__rotateSpeed = max(speed, 0.0)

    def get_rotateSpeed(self):

        return self.__rotateSpeed

    """""""""""""""""""""""""""""
    一些数据的打印函数，只要用于调试
    """""""""""""""""""""""""""""

    def print_optsFunc(self):

        print "-- Options Map Functions --"

        for k, v in self.__optsFunc.iteritems():

            print "%s : %s" % (k, v)

        print "--------------------"

    def print_optsSwitch(self):

        print "-- Options Switch --"

        for k, v in self.__optsSwitch.iteritems():

            print "%s : %s" % (k, v)

        print "--------------------"