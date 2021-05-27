from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_fontawesome import FontAwesome
from app.config import Config


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
fa = FontAwesome()
login.login_view = 'auth.login'
login.login_message = ('Please log in to access this page.')
login.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    fa.init_app(app)
    
    from app.public import public
    app.register_blueprint(public)
    
    from app.user import user
    app.register_blueprint(user)

    from app.github import github_blueprint
    app.register_blueprint(github_blueprint,  url_prefix='/github_login')

    from app.auth import auth
    app.register_blueprint(auth)

    from app.errors import error
    app.register_blueprint(error)
    
    return app


from app import models
