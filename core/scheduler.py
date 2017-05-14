# _*_ coding: utf-8 _*_

"""
@file: scheduler.py
@time: 2017/5/1 下午11:51
@author: pigbreeder
"""
import logging

import core.spiderQueue
import core.constant
from core.baseCoroutine import BaseCoroutine
import core.bloomFilter
from core.constant import get_core_name_with_prefix
from core.entity import Request


class Scheduler(BaseCoroutine):
    def finish_work(self, task, success=True):
        pass

    async def do_work(self):
        pass

    def __init__(self, spider, worker=1):
        super().__init__(worker=worker)
        self.__spider = spider
        self.__queue = core.spiderQueue.queueContext.get_queue(get_core_name_with_prefix(core.constant.SCHEDULER))
        self.__bf = spider.filter
        self.__log = logging.getLogger(core.constant.SCHEDULER)

    def get_task(self):
        return self.__queue.get_task()

    def put_task(self, request):
        assert isinstance(request,list) or isinstance(request,Request),'request must be list or Request'
        if isinstance(request,Request):
            request = [request]
        for req in request:
            if self.__bf.isContaions(req.url):
                self.__log.warning('the url=%s has been gotten' % req.url)
                return
            self.__spider.update_number(core.constant.TOTAL_TASK, +1)
            self.__queue.put_task(req)
