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


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(150))
    balance = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    number = db.Column(db.BigInteger, unique=True)
    payments = db.relationship('Payment')
    incomes = db.relationship('Income')


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    target_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    time = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)
    type = db.Column(db.String(150), default='payment')


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    source_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    time = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)
    type = db.Column(db.String(150), default='income')

