# _*_ coding: utf-8 _*_

"""
@file: testLock.py
@time: 2017/5/2 下午10:50
@author: pigbreeder
"""
from test.mylocker import *


class example:
    @lockhelper(mylocker)
    def myfunc(self):
        print(" myfunc() called.")

    @lockhelper(mylocker)
    @lockhelper(lockerex)
    def myfunc2(self, a, b):
        print(" myfunc2() called.")
        return a + b


if __name__ == "__main__":
    a = example()
    a.myfunc()
    print(a.myfunc())
    print(a.myfunc2(1, 2))
    print(a.myfunc2(3, 4))