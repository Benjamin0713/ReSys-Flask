#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/4/14 14:40
# @Author  : Benjamin
import flask
from app import db

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    mid = db.Column(db.String(255), nullable=False, comment="userid")
    title = db.Column(db.String(255), nullable=False)
    genres = db.Column(db.String(255), nullable=False)
