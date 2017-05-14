# _*_ coding: utf-8 _*_

"""
@file: spider.py
@time: 2017/5/5 下午4:29
@author: pigbreeder
"""
import abc
import json

import logging

import asyncio
from functools import reduce
from multiprocessing.dummy import Process

import settings
from core.bloomFilter import init_bloomFilter
import core.bloomFilter
from core.downloader import Downloader
from core.entity import Request
from core.log import init_log
from core.middleware import init_middleware
from core.monitor import Monitor
from core.save import Save
from core.scheduler import Scheduler
from core.spiderQueue import init_queue
import core.constant


class Spider():
    __metaclass__ = abc.ABCMeta

    start_request=[]
    def __init__(self, start_monitor=True):
        self.init()
        self.number_dict = {core.constant.TOTAL_TASK: 0, core.constant.TOTAL_REQUEST: 0,
                            core.constant.TOTAL_RESPONSE: 0}
        self.color = core.constant.COLOR
        self.close = False
        self.loop = asyncio.get_event_loop()
        self.filter = core.bloomFilter.bloomFilterContext.get_filter(settings.PROJECT_NAME)
        self.scheduler = Scheduler(self)
        self.downloader = Downloader(self, settings.DOWNLOADER_WORKER)
        self.save = Save(self, settings.SAVE_WORKER)
        self.monitor = Monitor(self)
        self.start_monitor = start_monitor

    def start_work(self):
        logging.warning(settings.PROJECT_NAME + ' start work')
        self.scheduler.put_task(self.__class__.start_request)
        if self.start_monitor:
            self.monitor_porcess = Process(target=self.monitor.start_work, name="monitor")
            self.monitor_porcess.daemon = True
            self.monitor_porcess.start()

        self.__start_process()

    def update_number(self, key, value):
        self.number_dict[key] += value

    async def check_finish(self):
        while not self.close:
            await asyncio.sleep(5)
            self.close = reduce(lambda x, y: x == y, self.number_dict.values())


    def __start_process(self):
        pass

        try:
            self.loop.run_until_complete(
                asyncio.wait([self.downloader.do_work(), self.scheduler.do_work(), self.save.do_work(),self.check_finish(),]))
        except Exception as excep:
            logging.error(("%s start_work error: " % self.__class__.__name__), excep.args)
        finally:
            self.loop.stop()
            self.loop.run_forever()
            self.loop.close()
            logging.info(settings.PROJECT_NAME + "finish.")
            # monitor

            # self.downloader.process = multiprocessing.Process(target=self.downloader.run)
            # self.downloader.process.start()
            # self.save.process = multiprocessing.Process(target=self.save.run)
            # self.save.process.start()
            # self.scheduler.process = Process(target=self.scheduler.run)
            # self.scheduler.process.start()
            #
            # self.scheduler.process.join()
            # self.downloader.process.join()
            # self.save.process.join()

    def init(self):
        init_log()
        init_queue()
        init_middleware()
        init_bloomFilter()

    # @abc.abstractmethod
    def add_start_url(self) -> Request:
        pass

    def to_save(self, response):
        with open(settings.STORAGE_PATH + '/save_data.log', 'w') as f:
            f.write("\t".join([response.url,str(response.status),json.dumps(response.meta)]) + "\n")
            f.flush()
            logging.info(("save data success.data=%r" % response.meta))

    def parse(self, response):
        pass
