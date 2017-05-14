# _*_ coding: utf-8 _*_

"""
@file: testFilter.py
@time: 2017/5/14 上午8:54
@author: pigbreeder
"""
from core.bloomFilter import BloomFilter

if __name__ == '__main__':
    pass
    fd = open("urls.txt")
    bloomfilter = BloomFilter()
    while True:
        # url = raw_input()
        url = fd.readline()
        if (url== 'exit') :  # if url is equal exit break
            break
        if bloomfilter.isContaions(url) == False:
            bloomfilter.insert(url)
        else:
            print('url :%s has exist' % url)