# -*- coding:utf-8 -*-

from panda3d.core import *

#####################

# 获取文件名后缀，如"models/demo.egg"的后缀为"egg"
def get_filepath_suffix(filepath):

    if isinstance(filepath, str):

        dotIdx = filepath.rfind('.')

        if dotIdx <= 1:
            return "egg"

        return filepath[(dotIdx + 1):]

    return None

#####################

# 根据key查找字典中的value
def find_value_in_dict(key, _dict):

    if isinstance(_dict, dict):

        if key in _dict.keys():

            return _dict[key]

    return None

#####################

# 根据value查找其所对应的key
def find_key_in_dict(value, _dict):

    if isinstance(_dict, dict):

        for k, v in _dict.iteritems():

            if v == value:

                return k

    return None

#####################

# 创建一个空的NodePath
def empty_NP():

    return NodePath()

#####################