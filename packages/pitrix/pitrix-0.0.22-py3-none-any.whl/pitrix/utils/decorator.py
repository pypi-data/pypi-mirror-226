#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import json
import time
import inspect
import datetime
from functools import wraps
from pitrix.utils.log import logger
from json.decoder import JSONDecodeError
from pitrix.utils.allure_attach import allure_attach

def single(cls):
    """
    类装饰器,对类实现单例模式
    """
    def inner(*args, **kwargs):
        if not hasattr(cls, "ins"):
            instance = cls(*args, **kwargs)
            setattr(cls, "ins", instance)
        return getattr(cls, "ins")
    return inner


def retry(max_retry: int = 0):
    """
    重试装饰器,调用成功返回原函数的返回值,调用失败或超过重试次数则返回False
    :param max_retry: 重试次数,默认为0
    :return:
    """
    def warpp(func):
        @wraps(func)
        def inner(*args, **kwargs):
            ret = func(*args, **kwargs)
            number = 0
            if not ret:
                while number < max_retry:
                    number += 1
                    logger.info(f"共计进行{max_retry}次重试,现在开始进行第:{number}次重试")
                    result = func(*args, **kwargs)
                    if result:
                        return result
                return False
            else:
                return ret
        return inner
    return warpp


def timer(func, unit="s"):
    """
    计算函数的运行时间—单位s,传递ms，则打印毫秒
    :param func: 被装饰的函数
    :return:None
    """
    def call_fun(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        end_time = time.time()
        if unit == "s":
            logger.info('%s() run time：%s s' %
                  (func.__name__, int(end_time - start_time)))
        else:
            logger.info('%s() run time：%s ms' %
                  (func.__name__, int(1000 * (end_time - start_time))))
        return f
    return call_fun


def func_log(func):
    """
    打印函数执行情况
    @param func:
    @return:
    """
    def inner(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res = func(*args, **kwargs)
        logger.info(f"func: {func.__name__} {args} -> {res}")
        return res
    return inner


def check_params(fn):
    """
    检查函数参数及类型
    @param fn:
    @return:
    """
    def wrapper(*args, **kwargs):
        logger.debug(f"传入参数:{*args,kwargs}")
        sig = inspect.signature(fn)
        logger.debug(f"参数及返回值:{sig}")
        # print('params : ', sig.parameters)
        logger.debug('返回值类型:', sig.return_annotation)
        for i, item in enumerate(sig.parameters.items()):
            name, param = item
            logger.debug(f"{name} 参数详细信息:{param.annotation, param.kind, param.default}")
        ret = fn(*args, **kwargs)
        return ret
    return wrapper


def request_wrapper(func):
    def wrapper(*args, **kwargs):
        logger.info('-------------- Request -----------------')
        # print(args, kwargs)
        payload = args[1]
        from pitrix.plugin import db_config, db_cache
        url = payload.get('url')
        method = payload.get('method')
        host = db_config.get("host")
        api_path = payload.get('api_path', '')
        headers = db_cache.get("headers")
        params = payload.get("params")
        data = payload.get("data")
        _json = payload.get("json")

        logger.info(f"请求地址 =====> {host + api_path}")
        logger.info(f"请求方法 =====> {method}")
        if headers:
            logger.debug(f"请求头 =====> {headers}")
        if params:
            logger.info(f"请求参数 =====> {params}")
        if data:
            logger.info(f"请求体[data] =====> {data}")
        if _json:
            logger.info(f"请求体[json] =====> {_json}")

        response = func(*args, **kwargs)

        if response.status_code <= 400:
            logger.info(f"请求成功,状态码：{str(response.status_code)}")
        else:
            logger.warning(f"请求失败,状态码：{str(response.status_code)}")

        elapsed = response.elapsed.total_seconds()

        api_name = inspect.stack()[1][3]
        try:
            resp = response.json()
            logger.info(f"请求响应 =====> {resp}")
        except JSONDecodeError as msg:
            logger.error(f"{msg}")
            resp = response.text
        finally:
            template = """请求URL: {}\n请求方法: {}\n请求头: {}\n请求主体data: {}\n请求主体json: {}\n响应状态码: {}\n响应: {}\n耗时: {}\n"""
            content = template.format(url, method, json.dumps(headers), data, _json, response.status_code, response.text,
                            elapsed)
            allure_attach.text(content)
        return resp

    return wrapper
