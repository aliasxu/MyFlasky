#!/usr/bin/env python
#_*_ coding:utf-8 _*_

from flask import Flask
from flask_bootstrap import  Bootstrap
from flask_mail import  Mail
from flask_moment import Moment
from flask_sqlalchemy import  SQLAlchemy
from config import  config
from flask_login import  LoginManager
from flask_pagedown import PageDown


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
#实例化Flask-Login
login_manager = LoginManager()

#实例化Flask-PageDown
pagedown = PageDown()

#session_protection设置为strong来提高用户会话的安全等级
login_manager.session_protection = 'strong'
#设置登陆页面的端点(蓝本函数)
login_manager.login_view = 'auth.login'


#工厂函数
def create_app(config_name):
    '''
    工厂函数
    :param config_name:程序的配置名，在config.py中定义
    :return:
    '''
    app  = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    #注册蓝本
    from .main import  main as main_blueprint
    app.register_blueprint(main_blueprint)

    #注册登陆蓝本
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix='/auth')

    return app