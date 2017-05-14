# _*_ coding: utf-8 _*_

"""
@file: save.py
@time: 2017/5/5 上午12:12
@author: pigbreeder
"""
import logging
import queue

import asyncio

import core.spiderQueue
import core.constant
from core.baseCoroutine import BaseCoroutine
from core.entity import Response, Request
import core.middleware


class Save(BaseCoroutine):
    def __init__(self, spider, worker=10):
        super().__init__(worker=worker)
        self.number_dict = {core.constant.SUCCESS: 0, core.constant.FAILED: 0, core.constant.NOT_HANDLER: 0}
        self.__spider = spider
        # self.__queue = core.spiderQueue.queueContext.get_queue(core.constant.DOWNLOADER)
        self.__log = logging.getLogger(core.constant.SAVE)

    async def do_work(self):
        pass
        while not self.__spider.close or not self.__spider.downloader.queue.is_empty():
            success = True

            try:
                response = self.get_task()
                assert isinstance(response, Response), "response is not a right type"
                self.number_dict[core.constant.NOT_HANDLER] += 1

                if not core.middleware.middlewareContext.call_saveMiddleware(response):
                    self.__log.warning('middleware execute failed! %s= ' % response.url)
                    success = False
                    continue
                self.__spider.parse(response)
                self.__spider.to_save(response)
                if response.meta and response.meta.get('append_url'):
                    self.append_task(response, response.meta.get('append_url'))
                self.__log.info(('success deal with url=%s,then put into DOWNLOADER queue') % response.url)
            except queue.Empty as e:
                self.__log.error('save queue is empty')
                await asyncio.sleep(3)
                response = None
                continue
            except Exception as e:
                success = False
                self.__log.error(('save url=%s,access failed!' % response.url))
            finally:
                if response != None:
                    self.finish_work(response, success)
                    self.number_dict[core.constant.NOT_HANDLER] -= 1

    def append_task(self, response, lst):
        assert isinstance(lst, list), "append_url is not a list type"
        for l in lst:
            request = response.request.replace(url=l)
            self.put_task(request)

    def get_task(self):
       return self.__spider.downloader.get_task()

    def put_task(self, request):
        self.__spider.scheduler.put_task(request)

    def finish_work(self, task, success=True):
        if not success:
            self.number_dict[core.constant.FAILED] += 1
        else:
            self.number_dict[core.constant.SUCCESS] += 1
        self.__spider.update_number(core.constant.TOTAL_RESPONSE, +1)
