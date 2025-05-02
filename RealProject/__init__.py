import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from RealProject.settings import BASE_DIR
from flask_migrate import Migrate

#操作数据库
db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    # 创建Flask应用实例
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        #如果没有传入，则从py文件加载配置，slient=true，代表文件，文件加载成功则返回true
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        #如果传入了配置，则加载传入的配置
        app.config.from_mapping(test_config)
    
    db.init_app(app)  # 初始化数据库
    migrate.init_app(app, db)  # 初始化数据库迁移


    # 引入视图文件
    from app import views as ai 
    app.register_blueprint(ai.bp)  # 注册蓝图

    # url引入
    app.add_url_rule('/',endpoint='index', view_func=ai.index)  # 注册路由

    # 引入模型文件
    from app import models 
    return app  # 返回Flask应用实例



