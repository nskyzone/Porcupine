# _*_ coding: utf-8 _*_

"""
@file: testSpider.py
@time: 2017/5/14 上午9:00
@author: pigbreeder
"""
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
    start_request = Request('http://www.yunpian.com')

    def save(self, response):
        super().save(response)
        print(response.headers + response.status)


class TestSpider(unittest.TestCase):
    def test(self):
        s = justSpider()
        s.start_work()
