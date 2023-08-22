#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import decimal
import json
import time
import jsonpath
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from requests import Response

from pitrix.utils.log import logger
from pitrix.utils.allure_attach import allure_attach
from pitrix.utils.decorator import request_wrapper


def request(method, url, **kwargs):
    template = """请求URL: {}\n请求方法: {}\n请求头: {}\n请求主体: {}\n响应状态码: {}\n响应: {}\n耗时: {}\n"""
    start = time.process_time()
    response = requests.request(method, url, **kwargs)
    end = time.process_time()
    elapsed = str(decimal.Decimal("%.3f" % float(end - start))) + "s"
    headers = kwargs.get("headers", {})
    kwargs.pop("headers")
    payload = kwargs
    rep = template.format(url, method, json.dumps(headers), json.dumps(payload), response.status_code, response.text,
                          elapsed)
    logger.info(rep)
    # allure_attach.text(rep, f'request & response')
    return PitrixResponse(response)

class PitrixResponse(Response):

    def __init__(self, response):
        """
        二次封装requests.Response，添加额外方法
        @param response:
        """
        super().__init__()
        for k, v in response.__dict__.items():
            self.__dict__[k] = v

    def jsonpath(self, expr):
        """
        此处强制取第一个值，便于简单取值
        如果复杂取值，建议直接jsonpath原生用法
        """
        return jsonpath.jsonpath(self.json(), expr)[0]


class BaseApi:

    def __init__(self):
        from pitrix.plugin import db_config, db_cache
        self.config = db_config.get_all()
        self._host = self.config.get('host')
        self._headers = self.cache.get('headers')

    @request_wrapper
    def send_http(self, http_data: dict):
        """
        发送http请求
        @param http_data:
        @return:
        """
        new_headers = http_data.get("headers")
        payload = self._payload_schema(**http_data)
        if new_headers:
            headers = self._headers
            headers.update(new_headers)
            payload["headers"] = headers
            logger.debug(f"请求头【新增】 =====> {new_headers}")
        response = requests.request(**payload)
        return response

    def _payload_schema(self, **kwargs):
        """
        构建参数
        @param kwargs:
        @return:
        """
        api_path = kwargs.get('api_path', '')
        method = kwargs.get('method')
        payload = {
            'url': self._host + api_path,
            'method': method,
            'headers': self._headers,
            'cookies': kwargs.get('cookies'),
            'auth': kwargs.get('auth'),
            'params': kwargs.get('params'),
            'data': kwargs.get('data'),
            'json': kwargs.get('json'),
            'files': kwargs.get('files')
        }
        return payload

