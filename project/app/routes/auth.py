from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from project.app import db
from project.app.functions.functions import *

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_pass = request.form.get('loginpass')
        password = request.form.get('password')
        if check_email_username(login_pass):
            user = User.query.filter_by(username=login_pass).first()
        else:
            user = User.query.filter_by(email=login_pass).first()
        if user:
            if password == user.password:
                flash('Welcome back ' + user.first_name + '!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid password, please try again!', category='error')
        else:
            flash('Invalid email address, please try again!', category='error')
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        u1 = User.query.filter_by(username=username).first()
        u2 = User.query.filter_by(email=email).first()
        if u1:
            flash('Username has already been taken!', category='error')
        elif u2:
            flash('Email has already been taken!', category='error')
        elif len(email) < 4:
            flash('Email should be longer!', category='error')
        elif password1 != password2:
            flash('Passwords not match', category='error')
        elif len(password1) < 7:
            flash('password should be longer!', category='error')
        else:
            # add user to database.
            new_user = User(last_name=lastName, first_name=firstName, email=email, password=password2,
                            username=username)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! Welcome ' + new_user.first_name + '!', category='success')
            return redirect(url_for('views.home'))

    return render_template('signUp.html', user=current_user)