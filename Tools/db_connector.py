#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/4/14 15:36
# @Author  : Benjamin
# 测试代码
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import trans
from model import *


class MysqlConnect:
    def __init__(self, host, user, pwd):
        self.host = host
        self.user = user
        self.pwd = pwd

    def connect(self, db_name):
        URL = "mysql+pymysql://{}:{}@{}/{}".format(self.user, self.pwd, self.host, db_name)
        print(URL)
        try:
            engine = create_engine(URL, max_overflow=0, pool_size=8)
            Session = sessionmaker(bind=engine)
            return Session
        except:
            return None
        # 每次执行数据库操作时，都需要创建一个session


if __name__ == '__main__':
    session = MysqlConnect("127.0.0.1:3306", "syh", "123").connect("recommend")
    mysql_session: Session = session()
    # r  = mysql_session.execute("select * from movies limit 5").all()
    filter = {
        "id":1
    }
    r = mysql_session.query(User).filter_by(**filter).all()
    for i in r:
        print(trans.model_to_dict(i))