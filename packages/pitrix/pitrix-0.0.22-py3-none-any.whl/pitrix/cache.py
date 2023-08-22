#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import json
import sqlite3
from jsonpath import jsonpath
from pitrix.utils.log import logger
from pitrix.database.sqlite import SQLiteDB
from pitrix.constants.constants import DataBase



class Config(SQLiteDB):
    def __init__(self,db_path):
        super(Config, self).__init__(db_path)
        self.table = DataBase.CONFIG_TABLE

    def set(self, key: str, value):
        sql = f"""insert into {self.table}(key,value) values (:key,:value)"""
        value = json.dumps(value)
        try:
            self.execute_sql(sql, (key, value))
        except sqlite3.IntegrityError as ie:
            logger.debug(f"config全局配置已加载=====>key: {key}, value: {value}")
            self.connection.commit()
            sql = "update {} set value=? where key=?".format(self.table)
            self.execute_sql(sql, (value, key))

    def get(self, key: str):
        sql = f"""select value from {self.table} where key=:key"""
        query_res = self.query_sql(sql, (key,))
        try:
            res = query_res[0][0]
        except IndexError:
            return None
        res = json.loads(res)

        return res

    def get_all(self) -> dict:
        """
        获取config表所有数据
        :return: {key:value,...}
        """
        all_data = self.select_data(self.table)
        dic = {}
        for m in all_data:
            dic[m[0]] = json.loads(m[1])
        return dic

    def clear(self):
        """清空表"""
        sql = """delete from {}""".format(self.table)
        self.execute_sql(sql)

    def del_(self, where: dict = None):
        """根据条件删除"""
        sql = """delete from {}""".format(self.table)
        if where is not None:
            sql += ' where {};'.format(self.dict_to_str_and(where))
        self.execute_sql(sql)


class Schema(SQLiteDB):
    def __init__(self,db_path):
        super(Schema, self).__init__(db_path)
        self.table = DataBase.SCHEMA_TABLE

    def set(self, key: str, value):
        sql = f"""insert into {self.table} (api_name,schema) values (:key,:value)"""
        try:
            self.execute_sql(sql, (key, json.dumps(value)))
        except sqlite3.IntegrityError:
            logger.debug(f"Schema表插入重复数据，key: {key},已被忽略！")
            self.connection.commit()

    def get(self, key: str):
        sql = f"""select schema from {self.table} where api_name=:key"""
        query_res = self.query_sql(sql, (key,))
        try:
            res = query_res[0][0]
        except IndexError:
            return None
        res = json.loads(res)

        return res

    def clear(self):
        sql = """delete from {}""".format(self.table)
        self.execute_sql(sql)

    def del_(self, where: dict = None):
        """根据条件删除"""
        sql = """delete from {}""".format(self.table)
        if where is not None:
            sql += ' where {};'.format(self.dict_to_str_and(where))
        self.execute_sql(sql)

    def count(self):
        """数量统计"""
        sql = f"""select count(*) from {self.table}"""
        try:
            res = self.query_sql(sql)[0][0]
        except IndexError:
            logger.error("shema表数据统计失败！")
            res = None
        return res


class Cache(SQLiteDB):
    def __init__(self,db_path):
        super(Cache, self).__init__(db_path)
        self.table = DataBase.CACHE_TABLE

    def set(self, key: str, value, api_info=None):
        sql = f"""insert into {self.table} (var_name,response,worker) values (:key,:value,:worker)"""
        if self.get(key) is not None:
            logger.debug(f"缓存插入重复数据, key:{key}，已被忽略！")
            return
        try:
            if api_info:
                sql = f"""insert into {self.table} (var_name,response,worker,api_info) values (:key,:value,:worker,:api_info)"""
                self.execute_sql(sql, (key, json.dumps(value), json.dumps(api_info)))
            else:
                self.execute_sql(sql, (key, json.dumps(value)))
        except sqlite3.IntegrityError as e:
            raise e

    def update(self, key, value):
        key_value = {"response": json.dumps(value)}
        condition = {"var_name": key}
        self.update_data(self.table, key_value, where=condition)
        logger.info(f"缓存数据更新完成, 表：{self.table},\n var_name: {key},\n response: {value}")

    def get(self, key: str, select_field="response"):
        if key == "headers":
            sql = f"""select {select_field} from {self.table} where var_name=:key"""
            query_res = self.query_sql(sql, (key,))
        else:
            sql = f"""select {select_field} from {self.table} where var_name=:key and worker=:worker"""
            query_res = self.query_sql(sql, (key))
        try:
            res = query_res[0][0]
        except IndexError:
            return None
        res = json.loads(res)

        return res

    def get_by_jsonpath(self, key: str, jsonpath_expr, expr_index: int = 0):
        res = self.get(key)
        extract_var = jsonpath(res, jsonpath_expr)
        if extract_var is False:
            raise ValueError(res,jsonpath_expr)
        extract_var = extract_var[expr_index]
        return extract_var

    def clear(self):
        sql = """delete from {}""".format(self.table)
        self.execute_sql(sql)

    def del_(self, where: dict = None):
        """根据条件删除"""
        sql = """delete from {}""".format(self.table)
        if where is not None:
            sql += ' where {};'.format(self.dict_to_str_and(where))
        self.execute_sql(sql)