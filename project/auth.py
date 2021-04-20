from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from .models import User
from . import db
from flask_mysqldb import MySQL
from . import create_app

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return render_template('logout.html')


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email should be longer!', category='error')
        elif len(firstName) < 2:
            flash('First Name should be longer!', category='error')
        elif len(lastName) < 2:
            flash('Last Name should be longer!', category='error')
        elif password1 != password2:
            flash('Passwords not match', category='error')
        elif len(password1) < 7:
            flash('password should be longer!', category='error')
        else:
            # add user to database.
            new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password2, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template('signUp.html')
