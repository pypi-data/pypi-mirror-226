#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

from datetime import datetime
from mitmproxy import ctx
from pitrix.database.mysql import MySQL
from pitrix.constants.constants import MysqlConfig


api_data = {}
DB = MySQL(**MysqlConfig.MYSQL_CONF)
API_DATA_TABLE = """
    CREATE TABLE IF NOT EXISTS api_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    start_time datetime,
    host VARCHAR (255),
    url text,
    method VARCHAR (255),
    headers LONGTEXT,
    body LONGTEXT,
    response LONGTEXT,
    duration float,
    status_code float)
    """

def request(flow):
    if 'qingcloud.com' in flow.request.url:
        api_data['host'] = flow.request.host
        api_data['url'] = flow.request.url
        api_data['method'] = flow.request.method

        headers_dict = {}
        headers = flow.request.headers
        for key, value in headers.items():
            headers_dict[key] = value
        api_data['headers'] = str(headers_dict)

        if flow.request.method == 'POST':
            api_data['body'] = flow.request.get_text()


def response(flow):
    if 'qingcloud.com' in flow.request.url:
        api_data['response'] = flow.response.text

        req_start_time = flow.request.timestamp_start
        start_time = datetime.fromtimestamp(req_start_time).strftime('%Y-%m-%d %H:%M:%S')
        ctx.log.info(start_time)
        api_data['start_time'] = start_time

        res_end_time = flow.response.timestamp_end

        api_data['duration'] = float(res_end_time) - float(req_start_time)

        api_data['status_code'] = float(flow.response.status_code)

        ctx.log.info(f"tyw debug:{api_data['duration']}")
        ctx.log.info(f"tyw debug:{api_data['status_code']}")

        save_api_table(db_name='api_data', table=API_DATA_TABLE)

def save_api_table(db_name, table):
    DB.create_sql(db_name, table)

    insert_sql = "INSERT INTO `api_data`" \
                 " (`start_time`, `host`,`url`,`method`," \
                 " `headers`,`body`,`response`," \
                 "`duration`,`status_code`) " \
                 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    insert_values = (
        api_data.get('start_time'),
        api_data.get('host'),
        api_data.get('url'),
        api_data.get('method'),
        api_data.get('headers'),
        api_data.get('body'),
        api_data.get('response'),
        api_data.get('duration'),
        api_data.get('status_code'),
    )
    DB.do_sql(insert_sql, value=insert_values)
