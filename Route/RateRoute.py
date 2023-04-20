#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/4/20 15:04
# @Author  : Benjamin
# Rateing实体
# class Ratings(db.Model):
#     __tablename__ = 'ratings'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
#     uid = db.Column(db.String(255), nullable=False, comment="userid")
#     mid = db.Column(db.String(255), nullable=False, comment="movieid")
#     rates = db.Column(db.String(255), nullable=False)
#
# # 查询所有rate信息
# @app.route('/rate/getall')
# def get_rate():
#     rate = Ratings.query.all()
#     # return "查询所有评分信息"
#     return jsonify(ts.model_to_dict(rate))

# # 分页查询
# @app.route('/rate/get/<int:num>/<int:per>/')
# def goodslist(num, per):
#     # 第num页
#     # 每页显示per行
#     rate = Ratings.query.offset((num - 1) * per).limit(per).all()
#     return jsonify(ts.model_to_dict(rate))