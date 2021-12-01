from shopping import app, db
from shopping.models import Seller, Buyer, Good 
from flask import render_template, request, flash


def add_user_to_database(username, password):
    '''
    return 0: 注册成功，-1: 用户已存在
    '''
    res = Buyer.query.filter_by(name=username).first()
    if res is not None: # 此用户已注册
        return -1
    else: # 此用户未注册
        user = Buyer(name=username, password = password)
        db.session.add(user)
        db.session.commit()
        return 0
    
def check_user_login(username, password):
    '''
    return 0: 登陆成功，-1：用户不存，-2: 密码错误
    '''
    res = Buyer.query.filter_by(name=username).first()
    if res is None: # 用户不存在
        return -1
    if res.password != password: # 密码错误
        return -2
    return 0




@app.route('/hello')
def homepage():
    goods = Good.query.all()
    return render_template('homepage.html', goods = goods, username = None)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        ret = add_user_to_database(username, password)
        print("ret:", ret)
        goods = Good.query.all()
        if ret == 0:
            flash("注册成功！")
            return render_template('homepage.html', goods = goods, username = username)
        else:
            flash("用户已存在，请登陆！")
            return render_template("homepage.html", goods = goods, username = None)
        
    elif request.method == 'GET':
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        ret = check_user_login(username, password)
        goods = Good.query.all()
        if ret == 0:
            flash("登陆成功!")
            return render_template("homepage.html", goods = goods, username = username)
        if ret == -1:
            flash("用户不存在，请注册！")
            return render_template("homepage.html", goods = goods, username = None)
        if ret == -2:
            flash("密码错误, 请重新输入！")
            return render_template('login.html')

    else:
        return render_template('login.html')