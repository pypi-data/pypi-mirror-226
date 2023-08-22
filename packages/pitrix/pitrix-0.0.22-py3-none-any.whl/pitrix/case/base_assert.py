#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import pytest
from pitrix.utils.log import logger

class BaseAssert:

    @staticmethod
    def assert_eq(actual_value, expected_value):
        if actual_value == expected_value:...
        else:
            msg = f"eq断言失败，预期结果：{expected_value}，实际结果：{actual_value}"
            logger.error(msg)
            pytest.fail(msg)

    @staticmethod
    def assert_gt(actual_value, expected_value):
        if actual_value > expected_value:...
        else:
            msg = f"gt断言失败，预期结果：{expected_value}，实际结果：{actual_value}"
            logger.error(msg)
            pytest.fail(msg)

    @staticmethod
    def assert_lt(actual_value, expected_value):
        if actual_value < expected_value:...
        else:
            msg = f"lt断言失败，预期结果：{expected_value}，实际结果：{actual_value}"
            logger.error(msg)
            pytest.fail(msg)

    @staticmethod
    def assert_neq(actual_value, expected_value):
        if actual_value != expected_value:...
        else:
            msg = f"neq断言失败，预期结果：{expected_value}，实际结果：{actual_value}"
            logger.error(msg)
            pytest.fail(msg)

    @staticmethod
    def assert_ge(actual_value, expected_value):
        if actual_value >= expected_value:...
        else:
            msg = f"ge断言失败，预期结果：{expected_value}，实际结果：{actual_value}"
            logger.error(msg)
            pytest.fail(msg)

    @staticmethod
    def assert_le(actual_value, expected_value):
        if actual_value <= expected_value:...
        else:
            msg = f"le断言失败，预期结果：{expected_value}，实际结果：{actual_value}"
            logger.error(msg)
            pytest.fail(msg)

    @staticmethod
    def assert_contains(actual_value, expected_value):
        if expected_value in actual_value:...
        else:
            msg = f"contains断言失败，预期结果：{expected_value}，实际结果：{actual_value}"
            logger.error(msg)
            pytest.fail(msg)

case = BaseAssert()