from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)
HOST = 'localhost'
PORT = '3306'
DATABASE_NAME = 'recommend'
USERNAME = 'syh'
PASSWORD = '123'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{databasename}?charset=utf8mb4" \
    .format(username=USERNAME, password=PASSWORD, host=HOST, port=PORT, databasename=DATABASE_NAME)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def start():
    print("后端启动成功!")
    return '后端启动成功!'

# @app.route('/test')
# def test():
#     sql = text('SELECT * FROM users')
#     cursor = db.session.execute(sql).cursor
#     db.session.commit()
#     # print(cursor.fetchall())
#     return jsonify(cursor.fetchall())

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
