from flask.helpers import url_for
from shopping import app, db
from shopping.models import Restaurant, Food, User
from flask import render_template, request, flash, redirect, session


    
def check_user_login(username, password):
    '''
    return 0: 登陆成功，-1：用户不存在，-2: 密码错误
    '''
    res = User.query.filter_by(name=username).all()
    if len(res) == 0: # 用户不存在
        return -1
    if res[0].password != password: # 密码错误
        return -2
    return 0

def add_user_to_database(username, password):
    '''
    return 0: 注册成功，-1: 用户已存在
    '''
    res = User.query.filter_by(name = username).all()
    if len(res) > 0: # 用户已存在
        return -1 
    user = User(name = username, password = password)
    db.session.add(user)
    db.session.commit()
    return 0


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        chosen_foods = request.form.getlist("chosen_foods")
        print("chosen_foods:", chosen_foods)
        foods_names = [x.split('##')[0] for x in chosen_foods]
        foods_prices = [float(x.split('##')[1]) for x in chosen_foods]
        assert len(foods_names) == len(foods_prices)
        total_price = round(sum(foods_prices), 1)
        print("total_price:", total_price)
        return render_template('user/user_confirm_foods.html', foods_names = foods_names, foods_prices = foods_prices, total_price = total_price)
         
    else:
        foods = Food.query.order_by("rest_name").all()
        return render_template('hello.html', foods = foods)


@app.route('/user_login', methods = ["GET", "POST"])
def user_login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        ret = check_user_login(username, password)
        if ret == 0:
            flash("登陆成功！")
            session['username'] = username
            return redirect(url_for('hello'))
        if ret == -1:
            flash("账号不存在，请注册！")
            return redirect(url_for('user_register'))
        if ret == -2:
            flash("密码输入错误，请重新登录！")
            return redirect(url_for('user_login'))

    return render_template('user/user_login.html')

@app.route('/user_register', methods = ['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        ret = add_user_to_database(username, password)
        if ret == 0:
            flash("注册成功，请登录！")
            return redirect(url_for('user_login'))
        else:
            flash("用户已存在，请登录！")
            return redirect(url_for('user_login'))

    return render_template('user/user_register.html')


@app.route('/user_logout')
def user_logout():
    session.clear()
    return redirect(url_for('hello'))


@app.route('/user_pay')
def user_pay():
    return 'Not implemented（此处应有付款二维码）!'


##############################################  seller ##################################################

def add_seller_to_database(fullname, nickname, location, phone, password):
    '''
    添加一个商家到数据库中, 若商家已存在则返回-1，否则返回0
    '''
    res = Restaurant.query.filter_by(nickname = nickname).all()
    if len(res) > 0: # 此商家已注册
        return -1
    rest = Restaurant(fullname = fullname, nickname = nickname, location = location, phone = phone, password = password)
    db.session.add(rest)
    db.session.commit()
    return 0


def check_seller_login(nickname, password):
    '''
    卖家登陆验证, 账号不存在-1，密码输入错误-2，登陆成功0
    '''
    res = Restaurant.query.filter_by(nickname = nickname).all()
    print("nickname:", nickname)
    print("res:", res)
    if len(res) == 0: # 账号不存在
        return -1
    if res[0].password != password: # 密码输入错误
        return -2
    return 0



@app.route('/seller_homepage/<nickname>')
def seller_homepage(nickname):
    foods = Food.query.filter_by(rest_name = nickname).all()
    return render_template('seller/seller_homepage.html', foods = foods, nickname = nickname)


# 卖家注册
@app.route('/seller_register', methods=["GET", "POST"])
def seller_register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        nickname = request.form.get("nickname")
        location = request.form.get("location")
        phone = request.form.get("phone")
        password = request.form.get("password")
        ret = add_seller_to_database(fullname = fullname, nickname = nickname, location = location, phone = phone, password = password)
        print("register ret:", ret)
        
        if ret == 0:
            flash("注册成功,请登录！")
            # 去登陆
            return redirect(url_for('seller_login'))
        else:
            flash("商家已存在，请登陆！")
            return redirect(url_for('seller_login'))
        
    elif request.method == 'GET':
        return render_template('seller/seller_register.html')


@app.route('/seller_login', methods=['GET', 'POST'])
def seller_login():
    if request.method == 'POST':
        nickname = request.form.get("nickname")
        password = request.form.get("password")
        ret = check_seller_login(nickname, password)
        print("login ret:", ret)

        if ret == 0:
            flash("登陆成功!")
            session['seller_name'] = nickname
            return redirect(url_for('seller_homepage', nickname = nickname))
        if ret == -1:
            flash("用户不存在，请注册！")
            return redirect(url_for('seller_register'))
        if ret == -2:
            flash("密码错误, 请重新输入！")
            return redirect(url_for('seller_login'))

    else:
        return render_template('seller/seller_login.html')

def add_food_to_database(name, price, rest_name):
    '''
    return 0:添加成功，-1:已存在同名商品！
    '''
    print("name:", name)
    res = Food.query.filter_by(rest_name = rest_name).filter_by(name = name).all()
    print("res:", res)
    if len(res) > 0: # 存在同名商品！
        return -1

    food = Food(name = name, price = float(price), rest_name = rest_name)
    db.session.add(food)
    db.session.commit()
    return 0


@app.route('/seller_add_food', methods=['GET', 'POST'])
def seller_add_food():
    if request.method == 'POST':
        foodname = request.form.get("foodname")
        price = request.form.get("price")
        seller_name = session['seller_name']
        ret = add_food_to_database(foodname, price, seller_name)
        print("add food ret:", ret)
        if ret == 0:
            flash("新商品上架成功！")
            return redirect(url_for('seller_homepage', nickname = seller_name))
        if ret == -1:
            flash("已存在同名商品，添加失败！")
            return redirect(url_for('seller_homepage', nickname = seller_name))

    return render_template('seller_add_food.html')