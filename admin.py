from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db, Post, User
from auth import login_required # 导入刚才写的验证装饰器

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    """后台首页：统计数据"""
    post_count = Post.query.count()
    # 统计总阅读量
    total_views = db.session.query(db.func.sum(Post.views)).scalar() or 0
    return render_template('admin/dashboard.html', 
                         post_count=post_count, 
                         total_views=total_views)

@admin_bp.route('/posts')
@login_required
def list_posts():
    """后台博客列表管理"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/list.html', posts=posts)

@admin_bp.route('/post/add', methods=['GET', 'POST'])
@login_required
def add_post():
    """新增博客"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('标题和内容不能为空', 'warning')
        else:
            new_post = Post(title=title, content=content)
            db.session.add(new_post)
            db.session.commit()
            flash('发布成功！', 'success')
            return redirect(url_for('admin.list_posts'))
            
    return render_template('admin/form.html', action="新增")

@admin_bp.route('/post/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """修改博客"""
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        flash('修改成功！', 'success')
        return redirect(url_for('admin.list_posts'))
        
    # 复用 form.html，传入当前文章对象
    return render_template('admin/form.html', action="编辑", post=post)

@admin_bp.route('/post/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    """删除博客"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('文章已删除', 'info')
    return redirect(url_for('admin.list_posts'))
