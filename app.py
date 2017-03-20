from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db
# 这里 import db 是为了给 migrate 用
# 如果不 import 数据库无法迁移
from models.user import User
from models.topic import Topic
from models.topic import Comment

app = Flask(__name__)
manager = Manager(app)


def configured_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # 设置上传文件的最大尺寸为 2M
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
    # secret key 和 数据库配置我都放在 config.py 里面
    import config
    app.secret_key = config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    # 初始化一个 db
    db.init_app(app)
    # 统一注册路由
    register_routes(app)
    # 配置日志
    configure_log(app)
    # 返回一个配置好的 app
    return app


def configure_log(app):
    # 设置 log, 否则输出会被 gunicorn 吃掉
    # 如果 app 是 debug 模式的话, 就不用了
    if not app.debug:
        import logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


def configure_manager():
    """
    这个函数用来配置命令行选项
    """
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


def register_routes(app):
    """
    在这个函数里面统一注册蓝图
    """
    from routes.static import main as routes_static
    app.register_blueprint(routes_static)

    from routes.user import main as routes_user
    app.register_blueprint(routes_user, url_prefix='/user')

    from routes.topic import main as routes_topic
    app.register_blueprint(routes_topic, url_prefix='/topic')

    from routes.upload import main as routes_upload
    app.register_blueprint(routes_upload, url_prefix='/uploads')


# 用自定义的命令行命令来运行服务器
# 用 @manager.command这种方法可以创建命令行运行方式
@manager.command
def server():
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
    )
    app.run(**config)


if __name__ == '__main__':
    configure_manager()
    configured_app()
    manager.run()
