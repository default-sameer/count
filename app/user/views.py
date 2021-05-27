from app.user import user
from flask import render_template
from flask_login import login_required, current_user
from .utlis import save_picture

@user.route('/dashboard')
@login_required
def dashboard():
    return render_template('users/dashboard.html', title='Dashboard')

@user.route('/settings')
@login_required
def setting():
    return render_template('users/setting.html', title='Setting')

@user.route('/dash')
@login_required
def dash():
    return render_template('users/dash.html', title='Setting')

