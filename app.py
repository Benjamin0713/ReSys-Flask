from flask import Flask, jsonify
from flask_cors import CORS
import Config.config
from Config.extensions import db
import Tools.trans as ts

app = Flask(__name__)
# 加载配置文件
app.config.from_object(Config.config)
# db绑定app
db.init_app(app)

CORS(app, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

# User实体
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    uid = db.Column(db.String(255), nullable=False, comment="userid")
    gender = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(255), nullable=False)
    occupation = db.Column(db.String(255), nullable=False)


# Movie实体
class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    mid = db.Column(db.String(255), nullable=False, comment="movieid")
    title = db.Column(db.String(255), nullable=False)
    genres = db.Column(db.String(255), nullable=False)


# Rateing实体
class Ratings(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    uid = db.Column(db.String(255), nullable=False, comment="userid")
    mid = db.Column(db.String(255), nullable=False, comment="movieid")
    rates = db.Column(db.String(255), nullable=False)


@app.route('/')
def start():
    print("后端启动成功!")
    return '后端启动成功!'

# 查询所有user信息
@app.route('/user/getall')
def get_user():
    user = Users.query.all()
    return jsonify(ts.model_to_dict(user))

# 分页查询
@app.route('/user/get/<int:num>/<int:per>/')
def goodslist(num, per):
    # 第num页
    # 每页显示per行
    user = Users.query.offset((num - 1) * per).limit(per).all()
    return jsonify(ts.model_to_dict(user))


# 查询所有movie信息
@app.route('/movie/getall')
def get_movie():
    movie = Movies.query.all()
    # return "查询所有电影信息"
    return jsonify(ts.model_to_dict(movie))

# 查询所有rate信息
@app.route('/rate/getall')
def get_rate():
    rate = Ratings.query.all()
    # return "查询所有评分信息"
    return jsonify(ts.model_to_dict(rate))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
