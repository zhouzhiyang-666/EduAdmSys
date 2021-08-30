from public.models import Logging
import logging
import os
from datetime import datetime

'''
日志类，将系统登录写入日志，
参数：请求+信息
'''
class LoggerTool:
    def __init__(self):
        pass

    def debug(self, request, message):
        current_time = datetime.now()
        print(current_time, request.path, request.method, message)
        Logging.objects.create(message=message,
                               level_string='DEBUG',
                               created_time=current_time,
                               logger_name=request.path)

        # Logging.objects.create(mess)

    def info(self, request, message):
        current_time = datetime.now()
        print(current_time, request.path, request.method, message)
        Logging.objects.create(message=message,
                               level_string='INFO',
                               created_time=current_time,
                               logger_name=request.path)

    def warning(self, request, message):
        current_time = datetime.now()
        print(current_time, request.path, request.method, message)
        Logging.objects.create(message=message,
                               level_string='WARNING',
                               created_time=current_time,
                               logger_name=request.path)

    def error(self, request, message):
        current_time = datetime.now()
        print(current_time, request.path, request.method, message)
        Logging.objects.create(message=message,
                               level_string='ERROR',
                               created_time=current_time,
                               logger_name=request.path)


def test_log():
    logger = LoggerTool()
    # output the log msg
    logger.debug("this is the debug message")
    logger.info("this is the info message")
    logger.warning("this is the warning message")
    logger.error("this is the error message")
