# # _*_ coding: utf-8 _*_
#
# """
# @file: factory.py
# @time: 2017/5/2 下午6:58
# @author: pigbreeder
# """
#
# class Factory(object):
#
#     instances = {}
#     SINGLETON = 'singleton'
#     PROTOTYPE = 'prototype'
#     @classmethod
#     def getInstance(cls,aClass,type, *args):
#         if aClass not in Factory.instances:
#             Factory.instances[aClass] = aClass(*args)
#         if type == Factory.SINGLETON:
#             return Factory.instances[aClass]  # 每一个类只能存在一个实例
#         elif type == Factory.PROTOTYPE:
#             return aClass(*args)
#
#     @classmethod
#     def registerClass(cls,aClass,name):
#         pass
#
#
# def singleton(aClass):
#     print(aClass)
#     def onCall(*args):
#         return Factory.getInstance(aClass,type, *args)
#     return onCall
#
# def prototype(aClass):
#     print(aClass)
#     def onCall(*args):
#         return Factory.getInstance(aClass,type, *args)
#     return onCall
#
# @singleton
# def fuck(f):
#     print(f)
# @singleton
# class asdf():
#     def __init__(self,name):
#         self.__name = name
#     def __str__(self, *args, **kwargs):
#         return 'in test %s'%self.__name
# fuck('a')
# test = asdf('f')
# print(test)
# test = asdf('ff')
# print(test)