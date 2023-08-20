# -*- coding: utf-8 -*-
# @Time: 2023/8/19 19:13
# @File: sql_reader.py
# @Desc：SQL文件读取

__all__ = ["SqlReader"]

import os


class SqlReader:
    @staticmethod
    def reader(path, *args, **kwargs):
        """
        读取sql文件
        :param path: sql文件路径
        :param args: sql参数
        :param kwargs: sql参数
        :return: 完整SQL
        """
        sql_path = os.getenv("SQL_PATH")
        path = os.path.join(sql_path, path) if not path else path
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
        begin_index = 0
        for index, line in enumerate(lines):
            if line.lower().startswith("select"):
                begin_index = index
                break
        sql = "".join(lines[begin_index:])
        for key, value in kwargs.items():
            sql = sql.replace(f"${key}", str(value))
        return sql.format(*args)
