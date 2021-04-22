# from project import db
# from flask_login import UserMixin
# from sqlalchemy.sql import func
#
#
# class SavingAccount(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     save_money = db.Column(db.Integer)
#
#
# class CheckingAccount(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     check_money = db.Column(db.Integer)
#
#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     password = db.Column(db.String(150))
#     first_name = db.Column(db.String(150))
#     last_name = db.Column(db.String(150))
#
#     def __init__(self, email, password, first_name, last_name):
#         self.email = email
#         self.password = password
#         self.first_name = first_name
#         self.last_name = last_name