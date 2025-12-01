from flask import Flask
from db import db, User
import os

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = 'dev-secret-key-123456' # 开发环境密钥
    # 使用当前目录下的 blog.sqlite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'blog.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化插件
    db.init_app(app)

    # 注册蓝图
    from auth import auth_bp
    from blog import blog_bp
    from admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp)

    # 创建数据库表和默认管理员
    with app.app_context():
        db.create_all()
        # 如果没有用户，创建一个默认管理员 admin/123456
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password='123456')
            db.session.add(admin)
            db.session.commit()
            print("初始化完成：默认管理员已创建 (admin/123456)")
        return app
    


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)