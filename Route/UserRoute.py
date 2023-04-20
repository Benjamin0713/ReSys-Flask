# # User实体
# class Users(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
#     uid = db.Column(db.String(255), nullable=False, comment="userid")
#     gender = db.Column(db.String(255), nullable=False)
#     age = db.Column(db.String(255), nullable=False)
#     occupation = db.Column(db.String(255), nullable=False)
#
#
# # 查询所有user信息
# @app.route('/user/getall')
# def get_user():
#     user = Users.query.all()
#     return jsonify(ts.model_to_dict(user))
#
# # 分页查询
# @app.route('/user/get/<int:num>/<int:per>/')
# def goodslist(num, per):
#     # 第num页
#     # 每页显示per行
#     user = Users.query.offset((num - 1) * per).limit(per).all()
#     return jsonify(ts.model_to_dict(user))