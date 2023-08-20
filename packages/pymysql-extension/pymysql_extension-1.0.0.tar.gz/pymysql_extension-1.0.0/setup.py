# -*- coding: utf-8 -*-
# @Time: 2023/8/19 20:43
# @File: setup.py
# @Desc：
import os

from setuptools import setup, find_packages

filepath = os.path.join(os.getcwd(), 'README.md')
setup(
    name='pymysql_extension',
    version='1.0.0',
    description='pymysql-extension是一个基于pymysql的扩展，主要是为了解决pymysql在使用过程中的一些不便之处。',
    long_description=open(filepath, encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Joker-desire/pymysql-extension",
    author='Joker-desire',
    author_email="2590205729@qq.com",
    requires=['pymysql'],
    packages=find_packages(),
    license="MIT Licence",
    data_files=[filepath],
    platforms="any",
    include_dirs=['pymysql_extension'],
)
