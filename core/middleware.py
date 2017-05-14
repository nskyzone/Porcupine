# _*_ coding: utf-8 _*_

"""
@file: middleware.py
@time: 2017/5/5 下午4:09
@author: pigbreeder
"""
import importlib
import logging

import settings
from core.pipeline import Pipeline


class MiddleWareContext():
    pass

    def __init__(self):
        self.__saveMiddleware = []
        self.__downloaderMiddleware = []
        self.register_middleware()

    # TODO scan settings
    def register_middleware(self):
        downloadMW = settings.DOWNLOADER_MIDDLEWARES
        saveMW = settings.SAVE_MIDDLEWARES
        self.register_(downloadMW, self.__downloaderMiddleware)
        self.register_(saveMW, self.__saveMiddleware)

    def register_(self, mw_lst, d):
        for mw in mw_lst:
            try:
                pass
                if isinstance(mw, str):
                    m1 = importlib.import_module(mw)
                    d.append(m1())
                elif issubclass(mw, Pipeline):
                    d.append(mw())
                else:
                    raise Exception('wrong config')
            except ImportError as e:
                logging.error('the module %s is not exist.' % mw)
            except Exception:
                logging.error('wrong config')

    def call_downloaderMiddleware(self, request):
        for mw in self.__downloaderMiddleware:
            if not mw.do_next(request):
                return False
        return True

    def call_saveMiddleware(self, response):
        for mw in self.__saveMiddleware:
            if not mw.do_next(response):
                return False
        return True


middlewareContext = None


def init_middleware():
    global middlewareContext
    middlewareContext = MiddleWareContext()
    print('init MiddleWare')
