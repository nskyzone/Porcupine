# _*_ coding: utf-8 _*_

"""
@file: redisMangment.py
@time: 2017/5/2 下午4:04
@author: pigbreeder
"""
import redis
import settings
import logging

logger = logging.getLogger()


# def redisException(func):
#     def _func(*args, **kwargs):
#         error, result = None, None
#         try:
#             result = func(*args, **kwargs)
#         except Exception as e:
#             logger.error('redis connection failed!')
#             error = str(e)
#
#         return {'result': result, 'error': error}
#     return _func


class Redis():
    def __init__(self):
        super().__init__()
        try:
            logger.info('init redis pool')
            if not settings.REDIS_HOST:
                raise Exception('not config redis!')
            self.__pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                               encoding_errors='strict', password=settings.REDIS_PASSWORD, db=0)
            self.__db = redis.Redis(connection_pool=self.__pool)
        except ConnectionError as e:
            logger.error('redis connection failed!')

    # @redisException
    def set(self, key, value):
        self.__db.set(key, value)

    def get_bit(self, name, loc):
        return self.__db.getbit(name, loc)

    def set_bit(self, name, loc, value):
        self.__db.setbit(name, loc, value)

    def get(self, key):
        return self.__db.get(key)

    def qsize(self, queue_name):
        return self.__db.llen(queue_name)

    def empty(self, queue_name):
        return self.qsize(queue_name) == 0

    def put_queue(self, queue_name, item):
        self.__db.rpush(queue_name, item)

    def get_queue(self, queue_name, block=True, timeout=None):
        if block:
            item = self.__db.blpop(queue_name, timeout=timeout)
        else:
            item = self.__db.lpop(queue_name)
        if item:
            item = item[1]
        return item

    def close(self):
        self.__pool.disconnect()


redisContext = None


def init_redis():
    global redisContext
    try:
        redisContext = Redis()
    except:
        redisContext = None
