# _*_ coding: utf-8 _*_

"""
@file: downloader.py
@time: 2017/5/4 下午11:50
@author: pigbreeder
"""
import logging
import queue

import asyncio

import core.spiderQueue
import core.constant
import settings
from core.baseCoroutine import BaseCoroutine
from core.entity import Request, Response
from core.fetchWeb import FetchWeb
import core.middleware
from core.constant import get_core_name_with_prefix


class Downloader(BaseCoroutine):
    def __init__(self, spider, worker=10, cookies=None, headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
):
        super().__init__(worker=worker)
        self.number_dict = {core.constant.SUCCESS: 0, core.constant.FAILED: 0, core.constant.NOT_HANDLER: 0}
        self.__spider = spider
        self.__queue = core.spiderQueue.queueContext.get_queue(get_core_name_with_prefix(core.constant.DOWNLOADER))
        self.__log = logging.getLogger(core.constant.DOWNLOADER)
        self.__http = FetchWeb(settings.SLEEP_TIME, settings.WAITTING_TIMEOUT, settings.RETRY_TIME, cookies, headers)
        self.__bf = spider.filter

    @property
    def queue(self):
        return self.__queue

    # 抓取、入队
    async def do_work(self):
        pass
        while not self.__spider.close:
            success = True

            try:
                request = self._get_task()
                assert isinstance(request, Request), "request is not a right type"
                self.number_dict[core.constant.NOT_HANDLER] += 1
                if request.retry >= settings.RETRY_TIME:
                    self.__log.warning('the url=%s retry many times,we discard it.' % request.url)

                if not core.middleware.middlewareContext.call_downloaderMiddleware(request):
                    self.__log.warning('middleware execute failed! %s= ' % request.url)
                    success = False
                    continue
                resp = await self.__http.access(request)
                if not resp:
                    success = False
                    continue
                self.__bf.insert(request.url)
                # new Response
                body = await resp.text()
                response = Response(url=request.url, status=resp.status, headers=resp.headers, body=body,
                                    request=request)
                self.__log.info(('success download url=%s,then put into DOWNLOADER queue') % response.url)
            except queue.Empty as e:
                self.__log.error('scheduler queue is empty')
                request = None
                await asyncio.sleep(3)
            except Exception as e:
                self.__log.error(('download url=%s,access failed!' % request.url))
                success = False
            finally:
                if request:# request maybe none
                    if not success:
                        self.finish_work(request, success)
                    else:
                        self.finish_work(response, success)
                    self.number_dict[core.constant.NOT_HANDLER] -= 1

        self.__http.close_session()
        self.__spider.color.print_red_text('closed downloader')

    def _get_task(self):
        return self.__spider.scheduler.get_task()

    def _put_task(self, request):
        self.__spider.scheduler.put_task(request)

    def get_task(self):
        return self.__queue.get_task()

    def put_task(self, response):
        self.__queue.put_task(response)

    def finish_work(self, task, success=True):

        if not success:
            self.number_dict[core.constant.FAILED] += 1
            if task.retry < settings.RETRY_TIME:
                task.retry += 1
                self._put_task(task)
            else:
                self.__log.warning('the url=%s retry many times,we discard it.' % task.url)
                if task.errback and callable(task.errback):
                    r = task.errback(task)
                    if isinstance(r, Request):  # you can modify this entity,if you faith to do it.
                        self._put_task(task)

        else:
            self.number_dict[core.constant.SUCCESS] += 1
            try:
                self.put_task(task)
            except Exception as e:
                print('in e')
            if task.request.callback and callable(task.request.callback):
                r = task.callback(task)
                if isinstance(r, Request):  # you can modify this entity,if you faith to do it.
                    self._put_task(task)
            pass
        self.__spider.update_number(core.constant.TOTAL_REQUEST, +1)
