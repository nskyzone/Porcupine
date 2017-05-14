# _*_ coding: utf-8 _*_

"""
@file: testBaseCoroutine.py
@time: 2017/5/6 上午8:06
@author: pigbreeder
"""
import asyncio
import random

from core.baseCoroutine import BaseCoroutine
import multiprocessing
from multiprocessing import Process


def testBaseCoroutine():
    class TB(BaseCoroutine):
        async def do_work(self):
            pass
            print('in ' + multiprocessing.current_process().name)
            await asyncio.sleep(random.randint(1, 3))

    p = []
    for i in range(10):
        print('start process,%d' % i)
        p.append(TB.new_process(TB))
    for i in p:
        i.join()


# testBaseCoroutine()


import asyncio
from collections import deque


def done_callback(fut):
    fut._loop.stop()


class Loop:
    def __init__(self):
        self._ready = deque()
        self._stopping = False

    def create_task(self, coro):
        Task = asyncio.tasks.Task
        task = Task(coro, loop=self)
        return task

    def run_until_complete(self, fut):
        tasks = asyncio.tasks
        # 获取任务
        fut = tasks.ensure_future(
            fut, loop=self)
        # 增加任务到self._ready
        fut.add_done_callback(done_callback)
        # 跑全部任务
        self.run_forever()
        # 从self._ready中移除
        fut.remove_done_callback(done_callback)

    def run_forever(self):
        try:
            while 1:
                self._run_once()
                if self._stopping:
                    break
        finally:
            self._stopping = False

    def call_soon(self, cb, *args):
        self._ready.append((cb, args))

    def _run_once(self):
        ntodo = len(self._ready)
        for i in range(ntodo):
            t, a = self._ready.popleft()
            t(*a)

    def stop(self):
        self._stopping = True

    def close(self):
        self._ready.clear()

    def call_exception_handler(self, c):
        pass

    def get_debug(self):
        return False


class Task(asyncio.futures.Future):
    def __init__(self, gen, *, loop):
        super().__init__(loop=loop)
        self._gen = gen
        self._loop.call_soon(self._step)

    def _step(self, val=None, exc=None):
        try:
            if exc:
                f = self._gen.throw(exc)
            else:
                f = self._gen.send(val)
        except StopIteration as e:
            self.set_result(e.value)
        except Exception as e:
            self.set_exception(e)
        else:
            f.add_done_callback(
                self._wakeup)

    def _wakeup(self, fut):
        try:
            res = fut.result()
        except Exception as e:
            self._step(None, e)
        else:
            self._step(res, None)


async def foo():
    await asyncio.sleep(2)
    print('Hello Foo')


async def bar():
    await asyncio.sleep(1)
    print('Hello Bar')


loop = Loop()
tasks = [loop.create_task(foo()),
         loop.create_task(bar())]
loop.run_until_complete(
    asyncio.wait(tasks))
loop.close()
