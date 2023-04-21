#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/3/12 19:22
# @Author  : Benjamin
import random
import math
import string

import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# 读取数据集
def loadData(fp):
    data = []
    for l in open(fp, encoding='gb18030', errors='ignore'):
        data.append(tuple(l.strip().split('::')))
    return data


def pd_toExcel(data, fileName):  # pandas库储存数据到excel
    movieid = []
    title = []
    genres = []
    occupy = []
    for i in range(len(data)):
        movieid.append(data[i][0])
        title.append(data[i][1])
        genres.append(data[i][2])
        occupy.append(data[i][3])

    dfData = {  # 用字典设置DataFrame所需数据
        'UserId': movieid,
        'Gender': title,
        'Age': genres,
        'Occupation': occupy
    }
    df = pd.DataFrame(dfData)  # 创建DataFrame
    df.to_excel(fileName, index=False)  # 存表，去除原始索引列（0,1,2...）

if __name__ == '__main__':
    fp = 'users.dat'  # 读取文件路径
    data = loadData(fp)
    # print(data)
    pd_toExcel(data,"users.xlsx")

