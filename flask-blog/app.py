from flask import Flask, render_template

app = Flask(__name__)

# 首页
@app.route('/')
def hello():
    # return 'Welcome to My World!'
    # return '<h1>Hello my Friend！</h1><img src="http://helloflask.com/totoro.gif">'
    return render_template('homepage.html', username='小胖儿')

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

