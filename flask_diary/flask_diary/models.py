from flask_diary import db


# 创建数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))


class Diary(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    create_time = db.Column(db.DateTime)
    location = db.Column(db.String(60))
    title = db.Column(db.String(60))
    content = db.Column(db.Text)