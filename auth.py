from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from db import User

# 定义蓝图
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(f):
    """自定义登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 查询数据库
        user = User.query.filter_by(username=username).first()
        
        # 简单比对密码（实际开发请用 werkzeug.security 的 check_password_hash）
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('登录成功！', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('用户名或密码错误', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))