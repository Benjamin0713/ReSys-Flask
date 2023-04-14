from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import Config.config

app = Flask(__name__)
app.config.from_object(Config.config)

db = SQLAlchemy(app)


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
    rate = db.Column(db.String(255), nullable=False)


@app.route('/')
def start():
    print("后端启动成功!")
    return '后端启动成功!'


@app.route('/user/getall')
def get_user():
    user = Users.query.all()
    for u in user:
        print("id: {}, uid: {},gender: {},age: {},occupation: {}".format(u.id, u.uid, u.gender, u.age, u.occupation))
    return "查询所有用户"


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
