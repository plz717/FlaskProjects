
from flask_diary import app, db
from flask_diary.models import User, Diary
import click
import datetime


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
    date_time_obj = datetime.datetime.strptime('21/12/05 00:00:00', '%d/%m/%y %H:%M:%S')
    d1 = Diary(title = u'我的第一个个人网站', content = u'从上周四到今天，利用工作&吃饭等之外的时间，完成了我的第一个个人网站！比想象的简单有趣多了！ 目前来看，这个网站主要是记录我自己的个人生活及心得，未来我还希望加入更多功能，做一个方便好用的日记工具～到那一天，某人会奖励我一个服务器将我的网站部署在上面给自己提供服务，同时我会考虑将它做成一个苹果或安卓的app分享给自己的亲朋好友使用。 头一回写代码写到了饭也不想吃觉也不想睡的地方，原来编程如此有趣，目测我的代码能力是想不提升也难了！😍!', create_time = date_time_obj, location = '上海古美七村')

    db.session.add(user)
    for diary in [d1]:
        db.session.add(diary)
    db.session.commit()
    click.echo("have added fake data into database")

    # check data
    print("total count of data in user table:", User.query.count())
    print("total count of data in diary table:", Diary.query.count())

