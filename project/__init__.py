from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_mysqldb import MySQL, MySQLdb


# import yaml


# db = SQLAlchemy()
# DB_NAME = "database.db"
# db = yaml.load(open('db.yaml'))

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3306/banking'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'hahahah'
    # db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

# def create_database(app):
#     if not path.exists('project/'+DB_NAME):
#         db.create_all(app=app)
#         print('Create')
