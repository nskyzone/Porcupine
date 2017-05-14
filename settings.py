# _*_ coding: utf-8 _*_

"""
@file: settings.py
@time: 2017/5/1 下午8:46
@author: pigbreeder
"""
import os
import logging

# Basic configure
PROJECT_NAME = 'Porcupine'
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DEBUG = True
PROJECT_LOG_LEVEL = logging.DEBUG
STORAGE_PATH = PROJECT_DIR + '/' + 'storage'
# Unit is seconds
MONITOR_TIME = 5

RETRY_TIME = 3
SLEEP_TIME = 2
WAITTING_TIMEOUT = 3

SAVE_WORKER=5
DOWNLOADER_WORKER=10
# mongo or mysql
DB_CONNECTION = ''
DB_HOST = 'localhost'
DB_PORT = ''
DB_DATABASE = 'Porcupine'
DB_USERNAME = "root"
DB_PASSWORD = ""

# default local, you can replace to redis
REDIS_HOST = ''
REDIS_PASSWORD = ''
REDIS_PORT = 6379

# MIDDLEWARE
DOWNLOADER_MIDDLEWARES = [
    # put subclass of core.pipeline.Pipeline
]
SAVE_MIDDLEWARES = [
    # put subclass of core.pipeline.Pipeline

]
