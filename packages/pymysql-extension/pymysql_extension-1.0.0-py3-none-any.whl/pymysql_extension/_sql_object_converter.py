# -*- coding: utf-8 -*-
# @Time: 2023/8/19 19:16
# @File: sql_object_converter.py
# @Desc：SQL对象转换器

__all__ = ["SqlObjectConverter"]

from typing import List

import pymysql


class Result:
    def __init__(self, **kwargs):
        self.__dict__ = dict(kwargs)

    def to_dict(self):
        return self.__dict__


class SqlObjectConverter:

    def __init__(self, **kwargs):
        self._field_names = None
        self._conn = pymysql.connect(
            host=kwargs.get("host", "localhost"),
            port=kwargs.get("port", 3306),
            user=kwargs.get("user", "root"),
            password=kwargs.get("password", "root"),
            db=kwargs.get("db", ""),
            charset=kwargs.get("charset", "utf8"),
        )
        self._cursor = self._conn.cursor()

    def exec(self, sql: str):
        self._cursor.execute(sql)
        # 获取表字段名,整理成字典
        self._field_names = {desc[0]: i for i, desc in enumerate(self._cursor.description)}
        return self

    def fetch_all(self) -> List[Result]:
        """
        获取所有数据
        :return:
        """
        return [Result(**dict(zip(self._field_names, row))) for row in self._cursor.fetchall()]

    def fetch_one(self) -> Result:
        """
        获取一条数据
        :return:
        """
        res = self._cursor.fetchone()
        return Result(**dict(zip(self._field_names, res))) if res else res

    def __del__(self):
        self._cursor.close()
        self._conn.close()
