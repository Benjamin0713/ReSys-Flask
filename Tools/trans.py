#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/4/14 15:41
# @Author  : Benjamin
# 格式化输出
import datetime

from sqlalchemy.orm import class_mapper


def model_to_dict(result):
    if result is None:
        return None
    if isinstance(result, list):
        if len(result) == 0:
            return None
        model = result[0]
        columns = [c for c in class_mapper(model.__class__).columns]
        result_dict = []

        for r in result:
            dic = {}
            for c in columns:
                c_type = str(c.type)
                if c_type == "DATETIME":
                    dic[c.key] = datetime.datetime.strftime(getattr(r, c.key), "%Y-%m-%d %H:%M:%S")
                elif c_type == "DATE":
                    dic[c.key] = datetime.datetime.strftime(getattr(r, c.key), "%Y-%m-%d")
                else:
                    dic[c.key] = getattr(r, c.key)
            result_dict.append(dic)
        # result_dict = [dict((c, getattr(r, c.key)) for c in columns) for r in result]
    else:
        model = result
        columns = [c for c in class_mapper(model.__class__).columns]
        result_dict = {}
        for c in columns:
            c_type = str(c.type)
            # print(c.type == "DATETIME")
            if c_type == "DATETIME":
                result_dict[c.key] = datetime.datetime.strftime(getattr(model, c.key), "%Y-%m-%d %H:%M:%S")
            elif c_type == "DATE":
                result_dict[c.key] = datetime.datetime.strftime(getattr(model, c.key), "%Y-%m-%d")
            else:
                result_dict[c.key] = getattr(model, c.key)
        # result_dict = dict((c, getattr(model, c)) for c in columns)
    return result_dict
