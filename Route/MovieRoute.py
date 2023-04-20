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
# 查询所有movie信息
# @app.route('/movie/getall')
# def get_movie():
#     movie = Movies.query.all()
#     # return "查询所有电影信息"
#     return jsonify(ts.model_to_dict(movie))

# # 分页查询
# @app.route('/movie/get/<int:num>/<int:per>/')
# def goodslist(num, per):
#     # 第num页
#     # 每页显示per行
#     movie = Movies.query.offset((num - 1) * per).limit(per).all()
#     return jsonify(ts.model_to_dict(movie))