#!/usr/bin/python3
# -*- coding:utf-8 -*-

import logging.handlers

from concurrent_log import ConcurrentTimedRotatingFileHandler

import exportInfluxdbEMS
from utils import *

def config_log():
    # Only works on POSIX systems and only Linux is supported. It does not work on Windows.
    from multiprocessing_logging import install_mp_handler, MultiProcessingHandler

    log_level = int(config.get('log', 'level'))

    timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(filename=config.get("log", "path"), when='H',
                                                                       interval=24,
                                                                       backupCount=20, encoding='utf8')

    log_handler = MultiProcessingHandler(
        "mp-handler",
        timed_rotating_handler,
    )
    log_handler.setLevel(log_level)
    log_handler.setFormatter(
        logging.Formatter('%(levelname)s:%(asctime)s:%(process)s:%(module)s:%(lineno)s:%(message)s'))
    logging.basicConfig(**{'handlers': [log_handler], 'level': log_level})


def config_log_win():
    from concurrent_log import ConcurrentTimedRotatingFileHandler

    log_level = int(config.get('log', 'level'))

    log_handler = ConcurrentTimedRotatingFileHandler(filename=config.get("log", "path"), when='H', interval=24,
                                                     backupCount=20, encoding='utf8')
    log_handler.setLevel(log_level)
    log_handler.setFormatter(logging.Formatter('%(levelname)s:%(asctime)s:%(module)s:%(lineno)s:%(message)s'))
    logging.basicConfig(**{'handlers': [log_handler], 'level': log_level})

    # logging.basicConfig(level=log_level)
    # logging.getLogger().addHandler(log_handler)


def my_config_log():
    logger = logging.getLogger()
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            console_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(console_formatter)
    logger.setLevel(logging.INFO)

    # 创建一个文件处理器
    file_handler = ConcurrentTimedRotatingFileHandler(filename=config.get("log", "path"), when='H', interval=24,
                                                      backupCount=20, encoding='utf8')
    file_handler.setLevel(logging.INFO)
    # 创建一个格式化器
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # 将格式化器添加到处理器
    file_handler.setFormatter(file_formatter)
    # 将处理器添加到logger对象
    logger.addHandler(file_handler)
def my_config_log_win():
    import colorlog
    logger = logging.getLogger()
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(colorlog.ColoredFormatter(
                '%(log_color)s %(asctime)s %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'green',
                    'INFO': 'bold_white',
                }
            ))
            # console_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')
            # handler.setFormatter(console_formatter)
    logger.setLevel(logging.INFO)
    # 创建一个控制台处理器
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.DEBUG)

    # 创建一个文件处理器
    file_handler = ConcurrentTimedRotatingFileHandler(filename=config.get("log", "path"), when='H', interval=24,
                                                     backupCount=20, encoding='utf8')
    file_handler.setLevel(logging.INFO)
    # 创建一个格式化器
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # 将格式化器添加到处理器
    file_handler.setFormatter(file_formatter)

    # 将处理器添加到logger对象
    logger.addHandler(file_handler)



if __name__ == '__main__':
    if sys.platform == "win32":
        my_config_log_win()
    else:
        my_config_log()
    start_time = exportInfluxdbEMS.get_influxdb_lasttime()
    exportInfluxdbEMS.manual_save_emsInfluxdb_tillnow(start_time)
