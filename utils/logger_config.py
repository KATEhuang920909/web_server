#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'yangzl31'
__mtime__ = '2020/5/28'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import os
import time

import logging.config
from logging import LogRecord

# 路径设置
curdir = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
predir = os.path.abspath(os.path.dirname(os.getcwd()))
logging.getLogger("elasticsearch").setLevel(logging.WARNING)


# 通常用于Linux系统下，使控制台输出的日志带颜色
class ColorFormatter(logging.Formatter):
    log_colors = {
        'CRITICAL': '\033[0;31m',
        'ERROR': '\033[0;33m',
        'WARNING': '\033[0;35m',
        'INFO': '\033[0;32m',
        'DEBUG': '\033[0;00m',
    }

    def format(self, record: LogRecord) -> str:
        s = super().format(record)

        level_name = record.levelname
        if level_name in self.log_colors:
            return self.log_colors[level_name] + s + '\033[0m'
        return s


LOGGER_CONF = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        # 'colored': {
        #     'class': 'logger_config.ColorFormatter',
        #     'format': '%(asctime)s - %(filename)s - %(funcName)s [line:%(lineno)d] - %(levelname)s: %(message)s'
        # },
        'default': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s - [%(threadName)s:%(thread)d] - %(filename)s - '
                      '%(funcName)s [line:%(lineno)d] - %(levelname)s: %(message)s'
        }
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': logging.INFO,
            'class': 'logging.StreamHandler',
            # 'formatter': 'colored',
        },
        'file': {
            'level': logging.INFO,
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': predir + r'\web_server\logs\dl.log',
            "when": "midnight",
            'backupCount': 100,
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': logging.INFO,
        },
    }
}

logging.config.dictConfig(LOGGER_CONF)
base_logger = logging.getLogger(__name__)

if __name__ == '__main__':
    base_logger.info('抽检数据,this is a logger info message')
    base_logger.info('处理工作池,this is a logger info message')
    base_logger.warning('处理工作池,this is a logger warning message')
    base_logger.error('聚类工作池,this is a logger error message')
