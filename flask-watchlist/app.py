from flask import Flask # 导入Flask类
app = Flask(__name__) # 实例化一个类对象

# 注册一个view function，可以理解为一个请求处理函数
# 注册：指的是给这个函数加一个装饰器帽子，并绑定到一个url
# 当用户在浏览器访问这个url时，就会触发这个函数，获取返回值，
# 并把返回值显示到浏览器窗口
# ---可以将web程序理解为一堆view function的集合：
# ---编写不同的函数处理对应url的请求

# 整个请求的处理过程如下：
#  当用户在浏览器地址栏访问这个地址，在这里即 http://localhost:5000/
#  服务器解析请求，发现请求 URL 匹配的 URL 规则是 /，因此调用对应的处理函数 hello()
#  获取 hello() 函数的返回值，处理后返回给客户端（浏览器）
#  浏览器接受响应，将其显示在窗口上

@app.route('/')
def hello():

    return '<h1> 欢迎来到我的世界！</h1> <img src="http://helloflask.com/totoro.gif">'


# 由于浏览器默认会把响应数据当作html格式解析
# escape对用户name变量进行转义处理，比如把<转换成&lt;
# 这样在返回响应时浏览器就不会把name变量当作html代码执行
from flask import escape

@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)


from flask import url_for

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='plz'))
    print(url_for('user_page', name = 'xcc'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for', num=2))
    return 'Test Page'

