from app import db
from app.auth import auth
from flask import render_template, flash, redirect, url_for, request
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse

@auth.get("/login")
@auth.post("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Email or password', 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('public.index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@auth.get("/register")
@auth.post("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))
    form = RegisterForm()
    if request.method == 'POST':
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)
