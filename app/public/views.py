from flask import render_template, current_app, redirect, url_for
from app.public import public
from flask_login import current_user

@public.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    return render_template('index.html', title='Home')


@public.route('/test')
def test():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    return render_template('test.html', title='Test')


@public.route("/pricing")
def pricing():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    return render_template('pricing.html', title='Pricing')
