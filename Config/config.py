#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/4/14 14:54
# @Author  : Benjamin
# 数据库配置文件

# 数据库连接配置
HOST = 'localhost'
PORT = '3306'
DATABASE_NAME = 'recommend'
USERNAME = 'syh'
PASSWORD = '123'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{databasename}?charset=utf8mb4" \
    .format(username=USERNAME, password=PASSWORD, host=HOST, port=PORT, databasename=DATABASE_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

# sqlacodegen --outfile "UserModel.py" "mysql+pymysql://syh:123@localhost:3306/recommend?charset=utf8mb4"