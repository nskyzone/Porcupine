# _*_ coding: utf-8 _*_

"""
@file: testFetchWeb.py
@time: 2017/5/6 下午7:49
@author: pigbreeder
"""
import asyncio

from core.entity import Request
from core.fetchWeb import FetchWeb

headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
def test_access():
    async def get_access():
        pass
        view = FetchWeb(headers=headers)
        r = Request(url='http://www.yunpian.com/')
        x = await view.access(r)
        if x:
            print(await x.text())
        view.close_session()
        print('finish')

    loop = asyncio.get_event_loop()
    tasks = [get_access()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

test_access()