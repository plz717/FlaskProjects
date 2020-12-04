import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import datetime
import click

app = Flask(__name__)
app.config['DEBUG'] = True

# 设置变量以告诉数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
db = SQLAlchemy(app) # 初始化扩展，传入程序实例app


# 创建数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20))


class Diary(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    create_time = db.Column(db.DateTime)
    title = db.Column(db.String(60))
    content = db.Column(db.Text)


# 自定义数据库初始化命令initdb
@app.cli.command()
@click.option('--drop', is_flag = True, help = 'create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


# 假数据
def fake_data():
    user = User(name = '小胖儿')
    d1 = Diary(title = 'my first diary', content = 'Im so happy today!', create_time = datetime.datetime.utcnow().strftime("%b %d %Y, %H:%M"))
    d2 = Diary(title = 'my second diary', content = 'Today is so exciting!', create_time = datetime.datetime.utcnow().strftime("%b %d %Y, %H:%M"))
    d3 = Diary(title = 'my third diary', content = 'So hard my way...', create_time = datetime.datetime.utcnow().strftime("%b %d %Y, %H:%M"))
    diaries = [d1, d2, d3]

    print("d1.create_time:", d1.create_time)
    print("d2.create_time:", d2.create_time)

    return diaries




# 首页
@app.route('/')
def hello():
    # return 'Welcome to My World!'
    # return '<h1>Hello my Friend！</h1><img src="http://helloflask.com/totoro.gif">'
    diaries = fake_data()
    return render_template('homepage.html', username='小胖儿', diaries = diaries)
    # return render_template('homepage.html', username = '小胖儿')

# template: 包含变量和运算逻辑的html/其他格式文本, 默认存储在项目根目录中（即与app.py相同的目录下）
# 渲染：进行变量替换及逻辑运算的过程，jinja2就是一个模版渲染引擎
# 静态文件：指的是内容不需要动态生成的文件，如图片、css文件和JavaScript脚本等
#
# @app.route('/homepage/<name>')
# def homepage(name):
#     return render_template('homepage.html', username = name, biography = 'my self-introduction')

# 注册
@app.route('/register')
def register():
    return
#
#
# # 登陆
# @app.route('/login')
# def login():
#
#
#
# # 登出
#
# # 新建博客

# 删除博客

