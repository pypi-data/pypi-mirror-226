#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import json
import allure
from pitrix.utils.log import logger

class AllureAttach:

    @staticmethod
    def text(body='',name='result'):
        """附加text类型文本到测试报告中"""
        try:
            allure.attach(body=body, name=name, attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def json(body={},name='result'):
        """附加json类型文本到测试报告中"""
        try:
            if body is None:
                body = {}
            _attachment = json.dumps(body, sort_keys=True, indent=2, separators=(',', ':'), ensure_ascii=False)
            allure.attach(body=_attachment, name=name, attachment_type=allure.attachment_type.JSON)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def csv(body='',name='result'):
        """附加csv类型文本到测试报告中"""
        try:
            allure.attach(body=body, name=name, attachment_type=allure.attachment_type.CSV)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def html(body='',name='result'):
        """附加html类型文本到测试报告中"""
        try:
            allure.attach(body=body, name=name, attachment_type=allure.attachment_type.HTML)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def yaml(body='',name='result'):
        """附加yaml类型文本到测试报告中"""
        try:
            allure.attach(body=body, name=name, attachment_type=allure.attachment_type.YAML)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def mp4_file(source, name='result'):
        """附加mp4类型文件到测试报告中"""
        try:
            allure.attach.file(source=source, name=name, attachment_type=allure.attachment_type.MP4)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def html_file(source, name='result'):
        """附加html文件到测试报告中"""
        try:
            allure.attach.file(source=source, name=name, attachment_type=allure.attachment_type.HTML)
        except Exception as e:
            logger.error(e)


allure_attach = AllureAttach()


__all__ = [allure_attach]

