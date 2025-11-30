from flask import Blueprint, render_template
from db import Post, db

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    """博客首页：展示文章列表"""
    # 按时间倒序排列
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('blog/index.html', posts=posts)

@blog_bp.route('/post/<int:post_id>')
def detail(post_id):
    """文章详情页"""
    post = Post.query.get_or_404(post_id)
    
    # 增加一点阅读量模拟数据变化
    post.views += 1
    db.session.commit()
    
    return render_template('blog/detail.html', post=post)