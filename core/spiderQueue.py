# _*_ coding: utf-8 _*_

"""
@file: cache.py
@time: 2017/5/2 下午2:40
@author: pigbreeder
"""
import functools
import logging
#from multiprocessing.dummy import Queue,Lock
from queue import Queue
# from asyncio import Queue
import abc
import settings
import core.redisModule
import core.constant
from core.constant import get_core_name_with_prefix
logger = logging.getLogger()


class BasicQueue():
    __metaclass__ = abc.ABCMeta

    def __init__(self, name=None):
        super().__init__()
        if not name:
            self._name = self.__class__.__name__
        else:
            self._name = name

    @abc.abstractmethod
    def put_task(self, task, block=False, timeout=None):
        raise NotImplementedError

    @abc.abstractmethod
    def get_task(self, block=True, timeout=None):
        raise NotImplementedError

    @abc.abstractmethod
    def get_size(self):
        pass

    @abc.abstractmethod
    def is_empty(self) -> bool:
        pass


class DefaultQueue(BasicQueue):
    def __init__(self, name=None):
        super().__init__()
        self._queue = Queue()
        self._key = name

    def get_task(self, block=True, timeout=None):
        pass
        return self._queue.get(False,core.constant.QUEUE_WAIT_TIME)

    def put_task(self, task, block=False, timeout=None):
        pass
        self._queue.put_nowait(task)

    def get_size(self):
        return self._queue.qsize()

    def is_empty(self) -> bool:
        return self._queue.empty()
    def task_done(self):
        self._queue.task_done()

class RedisQueue(BasicQueue):
    def is_empty(self) -> bool:
        return self._queue.empty(self._key)

    def get_size(self):
        return self._queue.qsize(self._key)

    def __init__(self, name=None):
        super().__init__()
        self._queue = core.redisModule.Redis()
        self._key = name

    def get_task(self, block=True, timeout=None):
        return self._queue.get_queue(self._key, block, timeout)

    def put_task(self, task, block=False, timeout=None):
        pass
        self._queue.put_queue(self._key, task)
    def task_done(self):
        pass


def queueException(func):
    def _func(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
            return r
        except Exception as e:
            logger.error('redis failed!')
            logger.error('change to defaultQueue')
            args[0].change_to_default(args[1])
        return func(*args, **kwargs)

    return _func


def sync(lock):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            lock.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                lock.release()

        return wrapper

    return decorator


# lock = Lock()

class QueueContext():
    def __init__(self):
        self._queue = {}

    def change_to_default(self, name):
        self._queue[name] = DefaultQueue(name)

    def new_queue(self, name):
        assert name, 'Cannot use queue without name'
        if settings.REDIS_HOST:
            self._queue[name] = RedisQueue(name)
        else:
            self._queue[name] = DefaultQueue(name)

    def get_queue(self, queue_name):
        try:
            return self._queue[queue_name]
        except KeyError as e:
            logger.error('KeyError,no key')
            self._queue[queue_name] = DefaultQueue(queue_name)
            return self._queue[queue_name]

    @queueException
    def put_task(self, queue_name, task, block=False, timeout=None):
        self.get_queue(queue_name).put_task(task, block, timeout)

    @queueException
    def get_task(self, queue_name, block=False, timeout=None):
        return self.get_queue(queue_name).get_task(block, timeout)


queueContext = None


def init_queue():
    print('init Queue')
    global queueContext
    queueContext = QueueContext()
    queueContext.new_queue(get_core_name_with_prefix(core.constant.DOWNLOADER))
    queueContext.new_queue(get_core_name_with_prefix(core.constant.SCHEDULER))


if __name__ == '__main__':
    queueContext.new_queue('asdf')
    queueContext.put_task('asdf', '4')
