#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import sys
from loguru import logger
from pitrix.constants.constants import LogConfig,TargetConf

class Log:

    def __init__(self,log_file=None,is_stdout=True,write_log=True):
        self.logger = logger
        self.log_file = log_file

        if is_stdout:
            self.logger.remove()
            self.logger.add(
                sink=sys.stdout,
                format=LogConfig.CONSOLE_FORMAT,
                level=LogConfig.CONSOLE_HANDLER_DEFAULT_LEVEL,
            )
        if write_log:
            if self.log_file:
                self.logger.add(
                    sink=self.log_file,
                    retention=LogConfig.RETENTION,
                    rotation=LogConfig.ROTATION,
                    compression=LogConfig.COMPRESSION,
                    encoding="utf-8",
                    enqueue=LogConfig.ENQUEUE,
                    backtrace=LogConfig.BACKTRACE,
                    level=LogConfig.FILE_HANDLER_DEFAULT_LEVEL,
                    format=LogConfig.FILE_FORMAT
                )

pitrix_logger = Log().logger
logger = Log(TargetConf.LOG_FILE).logger