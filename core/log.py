# _*_ coding: utf-8 _*_

"""
@file: log.py
@time: 2017/5/1 下午9:39
@author: pigbreeder
"""
import logging
import logging.handlers

import core.constant
import settings

# logging.basicConfig(level=settings.PROJECT_LOG_LEVEL,
#                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='root.log',
#                     filemode='w')

#################################################################################################
# console = logging.StreamHandler()
# console.setLevel(settings.PROJECT_LOG_LEVEL)
# formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
# console.setFormatter(formatter)
# logging.getLogger().addHandler(console)
#################################################################################################

def init_log():
    print('init Log')
    logging.basicConfig(level=settings.PROJECT_LOG_LEVEL,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


    downloaderHandler = logging.handlers.TimedRotatingFileHandler(settings.STORAGE_PATH + '/logs/downloader.log',
                                                                  when='midnight', encoding='utf8',
                                                                  backupCount=10)
    downloaderHandler.setFormatter(formatter)
    downloaderLogger = logging.getLogger(core.constant.DOWNLOADER)
    downloaderLogger.propagate = False
    downloaderLogger.setLevel(logging.INFO)
    downloaderLogger.addHandler(downloaderHandler)

    #
    saveHandler = logging.handlers.TimedRotatingFileHandler(settings.STORAGE_PATH + '/logs/save.log', when='midnight',
                                                            encoding='utf8',
                                                            backupCount=10)
    saveHandler.setFormatter(formatter)
    saveLogger = logging.getLogger(core.constant.SAVE)
    saveLogger.propagate = False
    saveLogger.setLevel(logging.INFO)
    saveLogger.addHandler(saveHandler)

    #
    handler = logging.handlers.TimedRotatingFileHandler(settings.STORAGE_PATH + '/logs/middleware.log', when='midnight',
                                                        encoding='utf8',
                                                        backupCount=10)
    handler.setFormatter(formatter)
    handlerLogger = logging.getLogger(core.constant.MIDDLEWARE)
    handlerLogger.propagate = False
    handlerLogger.setLevel(logging.INFO)
    handlerLogger.addHandler(handler)
