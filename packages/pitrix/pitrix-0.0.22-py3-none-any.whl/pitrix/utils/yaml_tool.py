#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import yaml

def load_yaml(yaml_file,mode='r'):
    """
    加载 yaml 文件并检查文件内容格式
    @param yaml_file:
    @param mode:
    @return:
    """
    with open(yaml_file, mode=mode) as stream:
        try:
            yaml_content = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as ex:
            err_msg = f"YAMLError:\n file: {yaml_file}\n error: {ex}"
            raise err_msg
        return yaml_content