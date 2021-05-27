from flask_dance.contrib import github
from flask_dance.contrib.github import make_github_blueprint
from flask_login import current_user
from app import db
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from app.models import OAuth

github_blueprint = make_github_blueprint(client_id='XXXX', client_secret='XXXXXXXXXXXXXXX')


github_blueprint.storage = SQLAlchemyStorage(OAuth, db.session)

from app.github import views
