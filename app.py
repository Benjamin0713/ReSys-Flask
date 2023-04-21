import json

from flask import Flask, jsonify
from flask_cors import CORS
import Config.config
from Config.extensions import db
import Tools.trans as ts
import tqdm
from Algorithm.AGRM import loadData, splitData, UserCF, AGRM

app = Flask(__name__)
# 加载配置文件
app.config.from_object(Config.config)
# db绑定app
db.init_app(app)

CORS(app, resources=r'/*')  # 注册CORS, "/*" 允许访问所有api


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
def userslist(num, per):
    # 第num页
    # 每页显示per行
    user = Users.query.offset((num - 1) * per).limit(per).all()
    return jsonify(ts.model_to_dict(user))


# 查询所有movie信息
@app.route('/movie/getall')
def get_movie():
    movie = Movies.query.all()
    # return "查询所有电影信息"
    # print(movie)
    return jsonify(ts.model_to_dict(movie))


# 分页查询
@app.route('/movie/get/<int:num>/<int:per>/')
def movieslist(num, per):
    # 第num页
    # 每页显示per行
    movie = Movies.query.offset((num - 1) * per).limit(per).all()
    return jsonify(ts.model_to_dict(movie))


# 查询所有rate信息
@app.route('/rate/getall')
def get_rate():
    rate = Ratings.query.all()
    # return "查询所有评分信息"
    # print(rate)
    return jsonify(ts.model_to_dict(rate))


# 分页查询
@app.route('/rate/get/<int:num>/<int:per>/')
def rateslist(num, per):
    # 第num页
    # 每页显示per行
    rate = Ratings.query.offset((num - 1) * per).limit(per).all()
    return jsonify(ts.model_to_dict(rate))


# 给用户推荐电影
@app.route('/resys/<string:uid>/<int:num>/')
def recommend(uid, num):
    tf = open("Algorithm/Resys_result_%d.json" % num, "r")
    user_recs = json.load(tf)

    resys_item = []
    for i in range(0, num):
        resys_item.append(user_recs[uid][i][0])

    movie = Movies.query.filter(Movies.mid.in_(resys_item)).all()

    print(movie)
    return jsonify(ts.model_to_dict(movie))


# @app.route('/resys/<string:uid>/<int:num>/')
# def recommend(uid,num):
#     fp = './Algorithm/Movielens dataset/ratings.dat'  # 读取文件路径
#     data = loadData(fp)
#     train, test, train_ex, test_ex, long, item_user, user50_test = splitData(data)
#     wait_user = []  # 候选集用户列表
#     getRecommendation, sorted_user_sim = UserCF(train, train_ex, num)
#     for user in user50_test:
#         wait_user.append(user)
#
#     user_recs = {}
#     agrm = AGRM(fp, data, user_recs, train, test, train_ex, test_ex, long, item_user, user50_test, wait_user,
#                 getRecommendation, sorted_user_sim)
#
#     for user in wait_user:
#         user_recs[user] = agrm.run(user)
#
#     resys_list = open("Algorithm/Resys_result_15.json", "w")
#     json.dump(user_recs, resys_list)
#     resys_list.close()
#
#     tf = open("Algorithm/Resys_result_%d.json" %num,"r")
#     # if num==1:
#     #     tf = open("Algorithm/Resys_result_1.json", "r")
#     # elif num==5:
#     #     tf = open("Algorithm/Resys_result_5.json", "r")
#     # elif num==10:
#     #     tf = open("Algorithm/Resys_result_10.json", "r")
#     user_recs = json.load(tf)
#
#     resys_item = []
#     for i in range(0, num):
#         resys_item.append(user_recs[uid][i][0])
#
#     movie = Movies.query.filter(Movies.mid.in_(resys_item)).all()
#
#     # print(movie)
#     return jsonify(ts.model_to_dict(movie))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
