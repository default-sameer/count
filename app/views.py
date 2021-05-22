from app import app, db
from app.models import User
from app.forms import LoginForm, RegisterForm
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html', title='Home')

@app.route('/test')
def test():
    return render_template('test.html', title='Test')

@app.get("/login")
@app.post("/login")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Email or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.get("/register")
@app.post("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/pricing")
def pricing():
    return render_template('pricing.html', title='Pricing')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('users/dashboard.html', title='Dashboard')

@app.route('/settings')
@login_required
def setting():
    return render_template('users/setting.html', title='Setting')

# Erorrs
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
# End Errors

