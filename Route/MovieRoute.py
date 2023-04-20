# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# # @Time    : 2023/4/18 12:43
# # @Author  : Benjamin
#
# # Movie实体
# class Movies(db.Model):
#     __tablename__ = 'movies'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
#     mid = db.Column(db.String(255), nullable=False, comment="movieid")
#     title = db.Column(db.String(255), nullable=False)
#     genres = db.Column(db.String(255), nullable=False)
#
#
# @app.route('/movie/getall')
# def get_movie():
#     movie = Movies.query.all()
#     for m in  movie:
#         print(1)
#
#     return "查询所有电影信息"