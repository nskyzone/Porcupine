# _*_ coding: utf-8 _*_

"""
@file: asyncInstance.py
@time: 2017/5/4 下午9:31
@author: pigbreeder
"""
import abc

import asyncio
import logging

from multiprocessing.dummy import Process


class BaseCoroutine():
    __metaclass__ = abc.ABCMeta

    def __init__(self, worker=1):
        super().__init__()
        self.worker = worker

    @abc.abstractmethod
    async def do_work(self):
        pass

    @abc.abstractmethod
    async def finish_work(self, task,success=True):
        pass

    @staticmethod
    def new_process(cls,*args,**kwargs):
        process = Process(target=BaseCoroutine.start_coroutine,args=(cls,)+args,kwargs=kwargs)
        process.daemon = True
        process.start()
        return process

    @staticmethod
    def start_coroutine(*args,**kwargs):
        # print("args=",args)
        if len(args) == 1:
            b = args[0]()
        else:
            b = args[0](*args[1:])
        # print(b)
        b.start_work()

    def run(self):
        logging.warning('start process,%s' % self.__class__.__name__)
        self.start_work()

    def start_work(self):
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(asyncio.wait([self.do_work() for i in range(self.worker)]))
        except Exception as excep:
            logging.error(("%s start_work error: " % self.__class__.__name__))
        finally:
            self.loop.stop()
            self.loop.run_forever()
            self.loop.close()


