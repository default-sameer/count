from flask import Flask, blueprints, redirect, url_for, session, flash
from flask_dance.contrib.github import github
import sqlalchemy
from app.github import github_blueprint
from flask import render_template, url_for, redirect
from flask_dance.consumer import oauth_authorized
from app import db
from sqlalchemy.orm.exc import NoResultFound
from app.models import User, OAuth
from flask_login import login_user


@github_blueprint.route("/")
def github_login():
    if not github.authorized:
        return redirect(url_for('github.login'))
    account_info = github.get('/user')
    account = account_info.json()
    return redirect(url_for('user.dashboard'))
    # return redirect(url_for('user.dashboard', account=account))

@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with GitHub.", category="error")
        return False
    
    account_info = blueprint.session.get('/user')
    if not account_info.ok:
        msg = "Failed to fetch user info from GitHub."
        flash(msg, category="error")
        return False
    github_info = account_info.json()
    
    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            token=token,
        )
    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with GitHub.")
    
    else:
        user = User(
            # Remember that `email` can be None, if the user declines
            # to publish their email address on GitHub!
            email=github_info["email"],
            username=github_info["name"],
            image_file=github_info["avatar_url"],
        )
        oauth.user = user
        db.session.add_all([user, oauth])
        db.session.commit()
        login_user(user)
        flash("Successfully signed in with GitHub.")
    return False

    
    # if account_info.ok:
    #     account = account_info.json()
    #     username = account['login']
    #     email = account['email']
        
    #     query = User.query.filter_by(username=username)
        
    #     try:
    #         user = query.one()
    #     except NoResultFound:
    #         user = User(username=username, email=email)
    #         db.session.add(user)
    #         db.session.commit()
    #     login_user(user)
