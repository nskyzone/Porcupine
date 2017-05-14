# _*_ coding: utf-8 _*_

"""
@file: pipeline.py
@time: 2017/5/1 下午11:45
@author: pigbreeder
"""
import abc


class Pipeline():
    __metaclass__ = abc.ABCMeta
    pass

    @abc.abstractmethod
    def do_next(self, task):
        pass

    def register(self):
        pass

# class DownloaderPipeline(Pipeline):
#     __metaclass__ = abc.ABCMeta
#
#     @abc.abstractmethod
#     def do_next(self,request):
#         pass
#
#     def register(self):
#         pass
#
#
# class SavePipeline(Pipeline):
#     __metaclass__ = abc.ABCMeta
#
#     @abc.abstractmethod
#     def do_next(self,response):
#         pass
#
#     def register(self):
#         pass
