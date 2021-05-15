from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_apscheduler import APScheduler

db = SQLAlchemy()
scheduler = APScheduler()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:cmpe202bank@bankdb.cing882ce6yu.us-west-1.rds.amazonaws' \
                                            '.com:3306/bank'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'whats up'
    db.init_app(app)

    from .routes.views import views
    from .routes.auth import auth
    from .routes.admins import admins
    from .routes.user_info import user
    from .routes.account_management import manage
    from .routes.deposits import deposits
    from .routes.accounts import accounts
    from .routes.transactions import transaction

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admins, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(manage, url_prefix='/')
    app.register_blueprint(deposits, url_prefix='/')
    app.register_blueprint(accounts, url_prefix='/')
    app.register_blueprint(transaction, url_prefix='/')

    from model.models import User

    #create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def create_database(app):
    if not path.exists('project/' + DB_NAME):
        db.create_all(app=app)
        print('Create')
