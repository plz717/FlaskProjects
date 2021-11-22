from shopping import db


class Seller(db.Model): # 表名将会是user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Good(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    price = db.Column(db.Float)

