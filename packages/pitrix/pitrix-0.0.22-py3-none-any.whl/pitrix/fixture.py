#!/usr/bin/python
# encoding=utf-8

import os
import json
import yaml
import pytest
from filelock import FileLock

from pitrix.utils.log import pitrix_logger
from pitrix.constants.constants import TargetConf

@pytest.fixture(scope="session")
def case_vars():
    """
    测试用例的动态变量，1条测试用例1个实例，彼此隔离
    """
    class CaseVars:
        def __init__(self):
            self.dict_in_memory = {}

        def put(self, key, value):
            self.dict_in_memory[key] = value

        def get(self, key):
            value = ""
            try:
                value = self.dict_in_memory[key]
            except KeyError:
                pitrix_logger.error(f"获取用例变量的key不存在，返回空串: {key}")
            return value
    return CaseVars()


@pytest.fixture(scope="session")
def tep_context_manager(tmp_path_factory, worker_id):
    """
    pitrix 上下文管理器，在xdist分布式执行时，多个session也只执行一次
    参考：https://pytest-xdist.readthedocs.io/en/latest/how-to.html#making-session-scoped-fixtures-execute-only-once
    命令不带-n auto也能正常执行，不受影响
    @param tmp_path_factory: 内置pytest 临时目录 fixture
    @param worker_id: 内置pytest xdist fixture
    @return:
    """
    def inner(produce_expensive_data, *args, **kwargs):
        if worker_id == "master":
            # not executing in with multiple workers, just produce the data and let
            # pytest's fixture caching do its job
            return produce_expensive_data(*args, **kwargs)

        # get the temp directory shared by all workers
        root_tmp_dir = tmp_path_factory.getbasetemp().parent

        fn = root_tmp_dir / "data.json"
        with FileLock(str(fn) + ".lock"):
            if fn.is_file():
                data = json.loads(fn.read_text())
            else:
                data = produce_expensive_data(*args, **kwargs)
                fn.write_text(json.dumps(data))
        return data

    return inner

