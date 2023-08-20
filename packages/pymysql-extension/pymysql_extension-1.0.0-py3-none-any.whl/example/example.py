# -*- coding: utf-8 -*-
# @Time: 2023/8/19 19:43
# @File: example.py
# @Desc：示例
import os

from pymysql_extension import SqlReader, SqlObjectConverter

if __name__ == '__main__':
    # 写入环境变量
    os.environ["SQL_PATH"] = "example"
    sql = SqlReader.reader("sql/example.sql", user_name="Joker-desire")
    print(sql)
    # 创建SQL对象转换器
    converter = SqlObjectConverter()
    # 执行SQL,并获取结果
    results = converter.exec(sql).fetch_all()
    print(results)
    # 执行SQL,并获取结果
    result = converter.exec(sql).fetch_one()
    # 将结果转换成字典
    print(result.to_dict())
