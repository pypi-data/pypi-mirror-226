#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import os

class DataBase:
    DB_NAME = "pitrix.db"

    CONFIG_TABLE = 'config'
    CACHE_TABLE = 'cache'
    SCHEMA_TABLE = 'schema'

    CACHE_VAR_NAME = 'var_name'
    CACHE_RESPONSE = 'response'
    CACHE_WORKER = 'worker'
    CACHE_API_INFO = 'api_info'

    CONFIG_KEY = 'key'
    CONFIG_VALUE = 'value'

    SCHEMA_API_NAME = 'api_name'
    SCHEMA_SCHEMA = 'schema'

class PitrixConf:
    PITRIX_BASE = os.path.dirname(os.path.dirname(__file__))
    PITRIX_TEMPLATE_SUFFIX = '.temp'
    PITRIX_TEMPLATE_DIR = os.path.join(PITRIX_BASE, "templates")

class TargetConf:
    PROJECT_DIR = ""
    FIXTURES = ""
    CONF_DIR = ""
    DATA_DIR = ""
    LOG_DIR = ""
    REPORT_DIR = ""
    CASE_DIR = ""
    DB_DIR = ""
    PYTEST_INI = ""
    DB_PATH = ""
    CONF_YAML = ""
    LOG_FILE = ""
    NOTIFICATION_YAML = ""

    ALLURE_RESULTS = ""
    ALLURE_REPORT = ""
    ALLURE_SUMMARY_FILE = ""
    ALLURE_ENV_FILE = ""
    ALLURE_TYPE_FILE = ""
    ALLURE_SERVER_IP = "127.0.0.1"
    ALLURE_SERVER_PORT = '8086'
    ALLURE_SERVER = f"http://{ALLURE_SERVER_IP}:{ALLURE_SERVER_PORT}"

    LOG_FILE_NAME = "pitrix.log"
    CONF_NAME = "config.yaml"
    UTILS_CONF_NAME = "utils.yaml"
    CURRENT_ENV_KEY = 'env'

    CONF_NAME_FILE = os.path.join(CONF_DIR, CONF_NAME)

class MysqlConfig:
    MYSQL_CONF = {
        "user": "root",
        "password": "12345678",
        "host": "localhost",
        "port": 3306,
    }

class LogConfig:
    """
    +----------------------+------------------------+------------------------+
    | Level name           | Severity value         | Logger method          |
    +======================+========================+========================+
    | ``TRACE``            | 5                      | |logger.trace|         |
    +----------------------+------------------------+------------------------+
    | ``DEBUG``            | 10                     | |logger.debug|         |
    +----------------------+------------------------+------------------------+
    | ``INFO``             | 20                     | |logger.info|          |
    +----------------------+------------------------+------------------------+
    | ``SUCCESS``          | 25                     | |logger.success|       |
    +----------------------+------------------------+------------------------+
    | ``WARNING``          | 30                     | |logger.warning|       |
    +----------------------+------------------------+------------------------+
    | ``ERROR``            | 40                     | |logger.error|         |
    +----------------------+------------------------+------------------------+
    | ``CRITICAL``         | 50                     | |logger.critical|      |
    +----------------------+------------------------+------------------------+
    """
    TRACE = 'TRACE'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    SUCCESS = 'SUCCESS'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICA = 'CRITICAL'

    RETENTION = "10 days"
    ROTATION = "10MB"
    COMPRESSION = 'zip'
    BACKTRACE = False
    ENQUEUE = True # 具有使日志记录调用非阻塞的优点(适用于多线程)

    FILE_HANDLER_DEFAULT_LEVEL = INFO
    CONSOLE_HANDLER_DEFAULT_LEVEL = DEBUG

    FILE_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {process.name} | {thread.name} | {module}.{function}:{line} | {level}:{message}"# 时间|进程名|线程名|模块|方法|行号|日志等级|日志信息
    CONSOLE_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | " \
                     "{process.name} | " \
                     "{thread.name} | " \
                     "<cyan>{module}</cyan>.<cyan>{function}</cyan>" \
                     ":<cyan>{line}</cyan> | " \
                     "<level>{level}</level>: " \
                     "<level>{message}</level>"