# _*_ coding: utf-8 _*_

"""
@file: testLog.py
@time: 2017/5/1 下午9:49
@author: pigbreeder
"""
import core.log
import logging

core.log.init_log()

logger=logging.getLogger()
logger.debug('root hello world')
logger=logging.getLogger('DOWNLOADER')
logger.debug('hello DOWNLOADER')
logger.info('hello DOWNLOADER')

import core.constant
core.constant.COLOR.print_yellow_text('asdf')
core.constant.COLOR.print_pink_text('asdf')
core.constant.COLOR.print_blue_text('asdf')