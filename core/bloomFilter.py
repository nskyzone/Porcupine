# _*_ coding: utf-8 _*_

"""
@file: filterModule.py
@time: 2017/5/5 下午7:29
@author: pigbreeder
"""
from hashlib import md5

import BitVector

import core.redisModule


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, name=None, BIT_SIZE=1 << 25):
        self.BIT_SIZE = BIT_SIZE
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.bitset = BitVector.BitVector(size=self.BIT_SIZE)
        self.hashFunc = []
        self.name = name

        for i in range(len(self.seeds)):
            self.hashFunc.append(SimpleHash(self.BIT_SIZE, self.seeds[i]))

    def insert(self, value):
        m5 = md5()
        m5.update(value.encode('utf8'))
        value = m5.hexdigest()
        for f in self.hashFunc:
            loc = f.hash(value)
            self.bitset[loc] = 1

    def isContaions(self, value):
        if value == None:
            return False
        m5 = md5()
        m5.update(value.encode('utf8'))
        value = m5.hexdigest()
        ret = True
        for f in self.hashFunc:
            loc = f.hash(value)
            ret = ret & self.bitset[loc]
        return ret


class BloomFilterContext():
    def __init__(self):
        super().__init__()
        self.filter = {}

    def get_filter(self, key):
        val = self.filter.get(key)
        if not val:
            val = BloomFilter(key)
            self.filter[key] = val
        return val


bloomFilterContext = None


def init_bloomFilter():
    print('init BloomFilter')
    global bloomFilterContext
    bloomFilterContext = BloomFilterContext()


if __name__ == '__main__': pass
# fd = open("urls.txt")
# bloomfilter = BloomFilter()
# while True:
#     # url = raw_input()
#     url = fd.readline()
#     if (url== 'exit') :  # if url is equal exit break
#         break
#     if bloomfilter.isContaions(url) == False:
#         bloomfilter.insert(url)
#     else:
#         print('url :%s has exist' % url)
