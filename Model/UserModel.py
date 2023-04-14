#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/4/14 14:33
# @Author  : Benjamin
import flask
from app import db

# User实体
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    uid = db.Column(db.String(255), nullable=False, comment="userid")
    gender = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(255), nullable=False)
    occupation = db.Column(db.String(255), nullable=False)