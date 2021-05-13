import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import click

app = Flask(__name__)
print("__name__:", __name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'dev'

# 设置变量以告诉数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
db = SQLAlchemy(app) # 初始化扩展，传入程序实例app


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


# 自定义数据库初始化命令initdb
@app.cli.command()
@click.option('--drop', is_flag = True, help = 'create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("Initialized database.")


# 往数据库加入假数据
@app.cli.command()
def addfakedata():
    user = User(name = '小胖儿', password = '040607')
    date_time_obj = datetime.strptime('21/12/05 00:00:00', '%d/%m/%y %H:%M:%S')
    d1 = Diary(title = u'我的第一个个人网站', content = u'从上周四到今天，利用工作&吃饭等之外的时间，完成了我的第一个个人网站！比想象的简单有趣多了！ 目前来看，这个网站主要是记录我自己的个人生活及心得，未来我还希望加入更多功能，做一个方便好用的日记工具～到那一天，某人会奖励我一个服务器将我的网站部署在上面给自己提供服务，同时我会考虑将它做成一个苹果或安卓的app分享给自己的亲朋好友使用。 头一回写代码写到了饭也不想吃觉也不想睡的地方，原来编程如此有趣，目测我的代码能力是想不提升也难了！😍!', create_time = date_time_obj, location = '上海古美七村')

    db.session.add(user)
    for diary in [d1]:
        db.session.add(diary)
    db.session.commit()
    click.echo("have added fake data into database")

    # check data
    print("total count of data in user table:", User.query.count())
    print("total count of data in diary table:", Diary.query.count())


# 首页
    # 使用 app.route() 装饰器来为函数hello绑定对应的 URL，
    # 当用户在浏览器访问这个 URL 的时候，就会触发函数hello，获取返回值，并把返回值显示到浏览器窗口
    # 可以把 Web 程序看作是一堆这样的视图函数的集合：编写不同的函数处理对应 URL 的请求。
@app.route('/')
def hello():
    diaries = Diary.query.all()
    return render_template('homepage.html', username='小胖儿', diaries = diaries)
    # flash("hello!")
    # return render_template('test.html')

# template: 包含变量和运算逻辑的html/其他格式文本, 默认存储在项目根目录中（即与app.py相同的目录下）
# 渲染：进行变量替换及逻辑运算的过程，jinja2就是一个模版渲染引擎
# 静态文件：指的是内容不需要动态生成的文件，如图片、css文件和JavaScript脚本等

@app.route('/diaries/<diary_id>')
def show_diary(diary_id):
    cur_diary = Diary.query.get(diary_id)
    id, title, time, content, location = cur_diary.id, cur_diary.title, cur_diary.create_time, cur_diary.content, cur_diary.location
    time = time.strftime('%b %Y %d , %H:%M')
    return render_template('diary.html', diary_id = id, time = time, title = title, content = content, username = '小胖儿', location = location)


# 新建一篇日记
@app.route('/diaries/create', methods=['GET', 'POST'])
def create_diary():
    if request.method == 'POST':
        username = request.form.get('username')
        title = request.form.get('title')
        content = request.form.get('content')
        location = request.form.get('location')
        # 验证数据
        if not username or not title or not content or not location or len(title) > 60 or len(location) > 60:
            flash('Invalid input!')
            return redirect(url_for('hello'))
        diary = Diary(title = title, location = location, content = content, create_time = datetime.date.today())
        db.session.add(diary)
        db.session.commit()
        flash('Diary created successfully!')

        return redirect(url_for('hello'))

    return render_template('create.html')


## 删除一篇日记
@app.route('/diaries/delete/<diary_id>', methods=['POST'])
def delete_diary(diary_id):
    if request.method == 'POST':
        diary = Diary.query.get(diary_id)
        db.session.delete(diary)
        db.session.commit()
        flash('Delete successfully!')

        return redirect(url_for('hello'))


## 编辑一篇已存在的日记
@app.route('/diaries/edit/<diary_id>', methods = ['GET', 'POST'])
def edit_diary(diary_id):
    if request.method == 'POST':
        diary = Diary.query.get(diary_id)
        return render_template('edit.html', diary = diary)

    return redirect(url_for('hello'))


# 保存一篇修改好的日记
@app.route('/diaries/save/<diary_id>', methods = ['GET', 'POST'])
def save_diary(diary_id):
    if request.method == 'POST':
        diary = Diary.query.get(diary_id)
        diary.title = request.form.get('title')
        diary.content = request.form.get('content')
        diary.location = request.form.get('location')
        db.session.commit()
        flash("Save successfully!")
        return redirect(url_for('hello'))

    return redirect(url_for('hello'))


# 注册账号
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 验证数据
        # username是否已存在
        usernames = db.session.query(User.name).all()
        usernames = [item[0] for item in usernames]

        if username in usernames: 
            flash("Username {} has existed!".format(username))
            return render_template('register.html')

        if not password or not username: 
            flash("empty input!")
            return render_template('register.html')
        
        user = User(name = username, password = password)
        db.session.add(user)
        db.session.commit()
        flash("User {} registered successfully! you are {}-th user of this website!".format(username, len(db.session.query(User.name).all())))

        return redirect(url_for('hello'))
    
    return render_template('register.html')

#
#
# # 登陆
# @app.route('/login')
# def login():
#
#
#
# # 登出

