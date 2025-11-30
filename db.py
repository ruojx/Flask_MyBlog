from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 初始化数据库实例
db = SQLAlchemy()

# --- 模型定义 ---

class User(db.Model):
    """管理员用户表"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # 实际项目中记得加密存储！

class Post(db.Model):
    """博客文章表"""
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 浏览量，做统计数据用
    views = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Post {self.title}>'