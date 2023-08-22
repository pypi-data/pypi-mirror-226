#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

# step1 : 引入需要的存储库
import json
import requests
from collections import defaultdict
from openpyxl import Workbook

# step2: 定义要解析swagger文档的 api.
schema_url = "http://www.ztloo.com/rest-api/schema"

print(requests.get(schema_url).json())

# step3: 缩小解析路径
paths = requests.get(schema_url).json()['paths']


# 提取每个接口参数数据中的参数名和参数类型，返回字典
def get_params(parameters):
    param_dicts = {}  # 收集一个接口的参数字典
    # 解析每个参数属性，例如name,type
    for each in parameters:  # 每个字典
        if each.get('in') in ['query', 'formData', 'path']:
            param_dicts.setdefault(each.get('name'), each.get('type'))
    return param_dicts


# step4: 实现读取各个接口和对应的get\post参数
def read_tags_params():
    """
    :return:  {'tag1':[{'get':params,'post':params}],'tag2':...}
    """
    # 创建存储结构
    tags_res = defaultdict(list)

    # 遍历接口的集合信息，获取单个接口，进行参数抽取
    for tag, tag_value in paths.items():
        # 过滤接口名字，去除前缀/wp/v2/
        tag = tag.replace("/wp/v2/", '')
        # 创建单个接口的请求类型为get和post请求的参数字典
        tag_params = {}  # {'get':params,'post':params}

        # 如果存在get请求数据
        if get_req_data := tag_value.get('get'):
            # 如果存在参数数据
            if get_parameters := get_req_data.get('parameters'):
                tag_params['get'] = get_params(get_parameters)

        # 如果存在post请求数据
        if post_req_data := tag_value.get('post'):
            if post_parameters := post_req_data.get('parameters'):
                tag_params['post'] = get_params(post_parameters)
        tags_res[tag].append(tag_params)
    return tags_res


# step5: 实现把tags_res中的数据，插入到Excel表格
def write_excel(tags_res):
    # 创建工作簿
    wb = Workbook()
    # 激活
    ws = wb.active
    # 添加表头
    ws.append(['接口名字', '请求类型', '参数'])  #
    #  {'tag1':[{'get':params,'post':params}],'tag2':...}
    for tag, tag_list in tags_res.items():
        # req_type：(get、post)  type_dict:params
        for req_type, type_dict in tag_list[0].items():
            row_list = list(map(str, [tag, req_type, type_dict]))
            ws.append(row_list)

    wb.save("ZTLOO_API_CASE.xlsx")  # 保存


if __name__ == '__main__':
    data = read_tags_params()
    print(json.dumps(data, indent=3))
    write_excel(data)
