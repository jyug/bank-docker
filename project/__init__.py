from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mysqldb import MySQL
import yaml


db = SQLAlchemy()
#DB_NAME = "database.db"
#db = yaml.load(open('db.yaml'))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:CMPE202@localhost/users'
    app.config['SECRET_KEY'] = 'hahahah'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, SavingAccount, CheckingAccount

    #create_database(app)

    return app


def create_database(app):
    if not path.exists('project/'+DB_NAME):
        db.create_all(app=app)
        print('Create')