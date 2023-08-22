#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author  : tython
# @Email   : 892398433@qq.com

import pymysql
from pitrix.utils.log import pitrix_logger

class MySQL:

    def __init__(self, **kwargs):
        """
        @param kwargs:
        """
        try:
            self.connection = pymysql.connect(charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,**kwargs)
        except Exception as e:
            pitrix_logger.error(f'数据库连接失败，连接参数：{kwargs}')
            raise e
        else:
            self.cursor = self.connection.cursor()

    def create_sql(self,db_name=None, table_sql=None,**kwargs):
        """
        create database
        @param db_name: DB NAME
        @param table_sql: TABLE CONTEXT
        @param kwargs:
        @return:
        """
        self.cursor.execute("SHOW DATABASES")
        dbs = [x['Database'] for x in self.cursor]
        if db_name not in dbs:
            SQL = f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
            self.cursor.execute(SQL)
            self.cursor.execute(f"USE {db_name}")
            try:
                self.cursor.execute(table_sql)
            except Exception as e:
                pitrix_logger.warning(str(e))
                self.connection.rollback()
            else:
                self.connection.commit()

    def do_sql(self,sql,value=None,select_type=None, **connect_kwargs):
        """
        query database
        @param sql: SQL
        @param value: 查询的条件或具体的创建或修改的参数数据
        @param select_type: "one"查询一条数据、"all"查询全部数据、"int(数字)":提取多行
        @return:
        """
        try:
            self.cursor.execute(sql, value)
            if select_type is not None:
                return self.do_query_type(select_type)
        except Exception as e:
            pitrix_logger.error(f"执行错误:{str(e)}")
            self.connection.rollback()
        else:
            self.connection.commit()

    def do_query_type(self,select_type='one'):
        """
        处理查询类型，封装pymysql 中查询函数，
        :param select_type:  处理do_sql中 的查询逻辑。
        :return:
        """
        if isinstance(select_type, str):
            if 'one' in select_type.lower():
                return self.cursor.fetchone()
            elif 'all' in select_type.lower():
                return self.cursor.fetchall()
            elif select_type.isdigit():
                return self.cursor.fetchmany(eval(select_type))
        if isinstance(select_type, int):
            return self.cursor.fetchmany(select_type)

    def close(self):
        self.cursor.close()
        self.connection.close()