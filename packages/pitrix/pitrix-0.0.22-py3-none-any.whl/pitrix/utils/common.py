#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import os
from pitrix.constants.constants import PitrixConf
from pitrix.utils.log import pitrix_logger

def add_template_suffix(dir='./', target_suffix=PitrixConf.PITRIX_TEMPLATE_SUFFIX):
    """
    将执行目录下的文件后缀名改为.temp
    @param dir:
    @param target_suffix:
    @return:
    """
    for root,dir,files in os.walk(dir):
        if files:
            for file in files:
                source_file = os.path.join(root,file)
                file_name, file_extension = os.path.splitext(source_file)
                if file_extension != target_suffix:
                    target_file = source_file + target_suffix
                    pitrix_logger.info(f"源文件:{source_file},目标文件:{target_file}")
                    os.rename(source_file,target_file)





if __name__ == '__main__':
    add_template_suffix(dir=PitrixConf.PITRIX_TEMPLATE_DIR)