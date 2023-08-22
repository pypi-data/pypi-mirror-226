from flask import Flask
from .views import get_user

def create_app():
    app = Flask(__name__)
    app.add_url_rule('/<user_page>', view_func=get_user)

    return app