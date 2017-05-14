# _*_ coding: utf-8 _*_

"""
@file: constant.py
@time: 2017/5/4 下午11:14
@author: pigbreeder
"""
import platform

import settings

if 'Windows' in platform.system():
    from core.color import WindowsColor

    COLOR = WindowsColor
else:
    from core.color import LinuxColor

    COLOR = LinuxColor


def get_core_name_with_prefix(name='', prefix=settings.PROJECT_NAME):
    return prefix + name


# core module
DOWNLOADER = '__DOWNLOADER__'
SCHEDULER = '__SCHEDULER__'
MONITOR = '__MONITOR__'
SAVE = '__SAVE__'

MIDDLEWARE = '__MIDDLEWARE__'

# record number
SUCCESS = '__SUCCESS__'
FAILED = '__FAILED__'
NOT_HANDLER = '__NOT_HANDLER__'
TOTAL_TASK = '__TOTAL_TASK__'
TOTAL_REQUEST = '__TOTAL_REQUEST__'
TOTAL_RESPONSE = '__TOTAL_RESPONSE__'

# SAVE_FILE
DOWNLOADED_URL = '__DOWNLOADED_URL__'
SCHEDULER_QUEUE = '__SCHEDULER_QUEUE__'

QUEUE_WAIT_TIME = 1
#
# class A():
#     def __init__(self,a):
#         self.aa=a
#         self.__s=4
# class B(A):
#     def __init__(self,a):
#         super().__init__(a)
#         # self.aa=4
# a=A(1)
# print(a._s)
# print(a.__dict__)
