# _*_ coding: utf-8 _*_

"""
@file: http.py
@time: 2017/5/3 上午8:28
@author: pigbreeder
"""
import random
import aiohttp
import asyncio
import logging

from core.defaultConfig import CONFIG_USERAGENT_PC, CONFIG_USERAGENT_PHONE, CONFIG_USERAGENT_ALL
from core.entity import Request


class FetchWeb():
    async def access(self, request):
        assert isinstance(request, Request), 'input request is wrong type'
        if not self._session:
            self.init_session(cookies=request.cookies, headers=request.headers)
        try:
            await asyncio.sleep(random.randint(0, self._sleep_time))
            if request.method == Request.GET:
                return await self._get(request.url, request.body)
            elif request.method == Request.POST:
                return await self._post(request.url, request.body)

        except Exception as e:
            logging.error('access web error.' + e.args.__str__())
            return None

    async def _get(self, url, parms=None):
        response = await self._session.get(url, params=parms, timeout=self._timeout)
        return response

    async def _post(self, url, data=None):

        response = await self._session.post(url=url, data=data, timeout=self._timeout)

        return response

    def __init__(self, sleep_time=2, timeout=2, retry_time=3, cookies=None, headers=None):
        self._sleep_time = sleep_time
        self._retry_time = retry_time
        self._timeout = timeout
        self.init_session(cookies, headers)

    def init_session(self, cookies=None, headers=None):
        if hasattr(self, '_session'):
            self.close_session()
        conn = aiohttp.TCPConnector(verify_ssl=False)
        headers= FetchWeb.get_random_UA() if  not headers else headers
        self._session = aiohttp.ClientSession(connector=conn, cookies=cookies, headers=headers)

    def close_session(self):

        if not self._session.closed:
            self._session.close()
        return
    @staticmethod
    def get_random_UA(ua_type="pc"):
        ua_type = ua_type.lower()
        assert ua_type in ("pc", "phone", "all"), "make_random_useragent: parameter ua_type[%s] is invalid" % ua_type
        return {"User-Agent":random.choice(CONFIG_USERAGENT_PC if ua_type == "pc" else (CONFIG_USERAGENT_PHONE if ua_type == "phone" else CONFIG_USERAGENT_ALL))}



if __name__ == '__main__':
    async def hello():
        pass
        view = FetchWeb()
        r = Request(url='https://www.lfasdfadfagou.com/')
        x = await view.access(r)
        if x:
            print(await x.text())
        view.close_session()
        print('finish')


    loop = asyncio.get_event_loop()
    tasks = [hello()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
