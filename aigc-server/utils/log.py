#!/usr/bin/python
# -*- coding:utf-8 -*-
# 统一日志组件

import logging
import os
import time
from logging.handlers import TimedRotatingFileHandler


class Logger(object):
    '''
    封装后的logging
    '''

    def __init__(self, logger=None, log_cate='search', log_name = "BotGateWay.log"):
        '''
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''

        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime("%Y_%m_%d")
        file_dir = os.getcwd() + '/logs'
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        self.log_path = file_dir
        self.log_name = self.log_path + '/' + log_name
        # windows
        # fh = TimedRotatingFileHandler(self.log_name, when='D', interval=24, backupCount=30)
        # linux/mac 打包时需使用when = MIDNIGHT 使用when = D没有凌晨自动创建下一天日志的功能（未解决）
        fh = TimedRotatingFileHandler(self.log_name, when='MIDNIGHT', interval=1, backupCount=30)
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.commons.removeHandler(ch)
        # self.commons.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def getlogger(self):
        return self.logger

logger = Logger(__name__).getlogger()