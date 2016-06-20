# coding=utf-8
#
# 本文档是一个python的logging 的demo
#

import logging
import logging.handlers

class SeriousLog(object):
    # 初始化函数
    # IN: 希望日志记录的文件的文件名称
    def __init__(self,file_name):
        self.file_name = file_name

    # 日志函数
    # IN：level--显示的错误等级（分为info,warn,error三个等级,使用字符串即可） content--希望显示的日志信息内容（字符串）
    def log(self,level,content):
        LOG_FILE = self.file_name

        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

        formatter = logging.Formatter(fmt)  # 实例化formatter
        handler.setFormatter(formatter)

        logger = logging.getLogger(level)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        logger.debug(content)

