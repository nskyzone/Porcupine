# _*_ coding: utf-8 _*_

"""
@file: testDownloader.py
@time: 2017/5/8 下午10:23
@author: pigbreeder
"""
import random
import unittest

import multiprocessing

import asyncio

from core.baseCoroutine import BaseCoroutine
from core.bloomFilter import init_bloomFilter
from core.entity import Request
from core.scheduler import Scheduler
from core.spider import Spider
from core.spiderQueue import init_queue


class justSpider(Spider):

    def add_start_url(self) -> Request:
        pass
        return Request('http://www.yunpian.com')

    def save(self,response):
        super().save(response)
        print(response.headers+response.status)
class TBB(BaseCoroutine):
    async def do_work(self):
        pass
        print('in TBB ' + multiprocessing.current_process().name)
        await asyncio.sleep(random.randint(1, 3))

class TestSpider(unittest.TestCase):
    def test(self):

        p = []
        pp=[]
        init_queue()
        init_bloomFilter()
        for i in range(10):
            print('start TB process,%d' % i)
            # p.append(TB.new_process(TB,))
            # pp.start()
            p.append(Scheduler(None))
            p.append(TBB(None))
        for i in p:
            x=multiprocessing.Process(target=i.run)
            pp.append(x)
        for i in pp:
            i.start()
        for i in pp:
            i.join()
    # def testSpider(self):
    #     spider = justSpider()
    #     spider.start_work()