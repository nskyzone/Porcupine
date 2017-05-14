# _*_ coding: utf-8 _*_

"""
@file: monitor.py
@time: 2017/5/1 下午11:56
@author: pigbreeder
"""
import core.constant
import logging

import settings
import time
import json


class Monitor():
    pass

    def __init__(self, spider):
        super().__init__()
        self.number_dict = {core.constant.SUCCESS: 0, core.constant.FAILED: 0, core.constant.NOT_HANDLER: 0}
        try:
            with open(settings.STORAGE_PATH + '/monitor_data', 'r') as f:
                line = f.readline()
                self.record_dict = json.loads(line)

        except Exception as e:
            logging.warning('monitor_data is not exist')
            self.record_dict = {core.constant.SCHEDULER: self.number_dict.copy(),
                                core.constant.DOWNLOADER: self.number_dict.copy(),
                                core.constant.SAVE: self.number_dict.copy()}

        self.monitor_time = settings.MONITOR_TIME
        self._spider = spider
        self._log = logging.getLogger(core.constant.MONITOR)
        self._color = self._spider.color

    def start_work(self):
        pass
        try:
            while not self._spider.close:
                self._color.print_red_text('monitor data')
                # for kk in self.number_dict.keys():
                #     self.record_dict[core.constant.DOWNLOADER][kk] = self._spider.downloader.number_dict[kk]
                #     self.record_dict[core.constant.SAVE][kk] = self._spider.save.number_dict[kk]
                #     self._color.print_green_text(kk + ' data:'+json.dumps(self.record_dict))
                self._color.print_green_text(
                    core.constant.DOWNLOADER + ' data:' + json.dumps(self._spider.downloader.number_dict))
                self._color.print_green_text(core.constant.SAVE + ' data:' + json.dumps(self._spider.save.number_dict))
                self._color.print_green_text('spider data: ' + json.dumps(self._spider.number_dict))
                time.sleep(3)
        except KeyboardInterrupt as e:
            logging.error('keyboard interrupt occur,and ready to kill procedure')
            self._spider.close = True
        except Exception as e:
            self._color.print_red_text('unknown exception occur,and ready to kill procedure')
            logging.error('unknown exception occur,and ready to kill procedure' + e.args)
            self._spider.close = True
        finally:
            pass
            self._color.print_pink_text("all tasks have been finished,please check in storage folder")
            self.save_data()

    def save_data(self):
        with open(settings.STORAGE_PATH + '/monitor_data.log', 'w') as f:
            f.write(json.dumps(self._spider.downloader.number_dict) + '\n')
            f.write(json.dumps(self._spider.save.number_dict) + '\n')
            f.write(json.dumps(self._spider.number_dict) + '\n')
            # save downloaded url,scheduler queue tasks
            # with open(settings.STORAGE_PATH + core.constant.DOWNLOADED_URL,'w') as f:
