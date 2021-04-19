from project import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Saving_Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    save_money = db.Column(db.Integer(20))


class Checking_Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    check_money = db.Column(db.Integer(20))

# Testing sss
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    saving_account = db.relationship('Saving_Account')
    checking_account = db.relationship('Checking_Account')
