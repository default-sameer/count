from flask import Blueprint

public = Blueprint('public', __name__,  url_prefix='/')

from app.public import views
