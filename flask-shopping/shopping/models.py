from shopping import db


# class Seller(db.Model): # 表名将会是user（自动生成，小写处理）
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))


# class Buyer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20))
#     password = db.Column(db.String(20))


# class Good(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(100))
#     price = db.Column(db.Float)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(20)) # 公司全名
    nickname = db.Column(db.String(20)) # 公司昵称，用于登陆使用
    password = db.Column(db.String(20))    
    location = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    company_names = db.Column(db.String(100))  # 餐馆可以对应的公司names

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Float(10))
    rest_name = db.Column(db.String(20)) # 可提供此食物的餐馆fullname

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))
    company = db.Column(db.String(20))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    rest_names = db.Column(db.String(100)) # 公司可以对应的餐馆names



