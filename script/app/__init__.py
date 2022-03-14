#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# __author__: 'junxing'
# date: 2016/10/11

from flask import Flask, request, g
from flask_assets import Environment
import os
from werkzeug.middleware.shared_data import SharedDataMiddleware
# from .default.routes import configure_routes
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf import CSRFProtect

# from config import development, production
# from .utils import assets
# from .utils.assets import bundles
from app.utils.salt import SaltApi

from .config import read_config


# login_manager = LoginManager()
# csrf = CSRFProtect()


# config = {
#     'dev': development.Development,
#     'pro': production.Production,
# }

db = SQLAlchemy()

# app = Flask(__name__)

# @app.route('/')
# def index():
#     f = app.static_folder + "\\index.html"
#     return send_file(f)
    # if request.args:
    #     # print(request.args)
    #     key = list(request.args)[0]
    #     return send_from_directory(f"{os.getcwd()}/app/dist/app", key)
    # else:
    #     return send_from_directory(f"{os.getcwd()}/app/dist/app", "index.html")
    # print(os.getcwd())
    # return send_from_directory(f"{os.getcwd()}/script/static/","index.html")

def create_app(config_name):
    '''初始化 应用'''
    config = read_config(config_name)
    app = Flask(__name__,static_folder="static")

    with app.app_context():
        
        app.config.update(config)
        # app.config.from_envvar()
        app.static_folder = os.path.dirname(__file__) + "\\..\\static\\"
        ##config[config_name].init_app(app)

        # login_manager.session_protection = "strong"
        # login_manager.login_view = 'user.login'  # 未认证用户跳转

        db.init_app(app)
        # static_path = os.path.dirname(__file__) + "\\..\\static\\"
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/': app.static_folder
        })
        # 1
        # Register our blueprints
        # if 'saltapi' not in g:
        #     g.saltapi = SaltApi(app.config["SALT_URL"],app.config["SALT_USER"],app.config["SALT_PASS"])
        from .default import default as default_blueprint
        app.register_blueprint(default_blueprint)
    # app.app_context().push()
    # 2
    # configure_routes(app)
    # 3
    # bootstrap.init_app(app)
    # login_manager.init_app(app)
    #csrf.init_app(app)
    # assets = Environment(app)
    # assets.register(bundles)

    # from app.views import user
    # from app.views import dashboard
    # from app.views import api
    # from app.views import machine
    # from app.views import publish

    # app.register_blueprint(user)
    # app.register_blueprint(dashboard)
    # app.register_blueprint(api)
    # app.register_blueprint(machine)
    # app.register_blueprint(publish)

    return app