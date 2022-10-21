from os import environ

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = environ.get("DB_SECRET")
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI', 'sqlite:///db.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from app.endpoints.gitlab_hook import bp as gitlab_hook_bp
    app.register_blueprint(gitlab_hook_bp)

    return app
