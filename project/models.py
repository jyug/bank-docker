from flask_login import UserMixin
from . import db
from datetime import datetime
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    address = db.Column(db.String(255))
    accounts = db.relationship('Account')
    receive_transaction = db.relationship('Transaction')


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150))
    transactions = db.relationship('Transaction')
    balance = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float)
    time = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)
    from_account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'))
