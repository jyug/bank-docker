from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, jsonify
from flask_login import login_user, logout_user, login_required
from project.app import db
from project.app.functions.functions import *


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    #     login_pass = request.form.get('loginpass')
    #     password = request.form.get('password')
    #     if check_email_username(login_pass):
    #         user = User.query.filter_by(username=login_pass).first()
    #     else:
    #         user = User.query.filter_by(email=login_pass).first()
    #     if user:
    #         if password == user.password:
    #             flash('Welcome back ' + user.first_name + '!', category='success')
    #             login_user(user, remember=True)
    #             return redirect(url_for('views.home'))
    #         else:
    #             flash('Invalid password, please try again!', category='error')
    #     else:
    #         flash('Invalid email address, please try again!', category='error')
    # return render_template('login.html', user=current_user)
    if request.method == 'POST':
        if not request.is_json:
            return make_response({'msg': "no json"}), 200
        req = request.get_json()
        login_pass = req.get('loginpass')
        password = req.get('password')
        if check_email_username(login_pass):
            user = User.query.filter_by(username=login_pass).first()
        else:
            user = User.query.filter_by(email=login_pass).first()
        if user:
            if password == user.password:
                flash('Welcome back ' + user.first_name + '!', category='success')
                login_user(user, remember=True)
                return make_response(jsonify({'msg': 'correct'})), 302
                # return redirect(url_for('views.home'))
            else:
                flash('Invalid password, please try again!', category='error')
                return make_response(jsonify({'msg': 'invalid password'}), 409)
        else:
            flash('Invalid email address, please try again!', category='error')
            return make_response(jsonify({'msg': 'invalid email'}), 409)
    else:
        # return render_template('login.html', user=current_user)
        return make_response(render_template('login.html', user=current_user))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # if request.method == 'POST':
    #     username = request.form.get('username')
    #     email = request.form.get('email')
    #     firstName = request.form.get('firstName')
    #     lastName = request.form.get('lastName')
    #     password1 = request.form.get('password1')
    #     password2 = request.form.get('password2')
    #     u1 = User.query.filter_by(username=username).first()
    #     u2 = User.query.filter_by(email=email).first()
    #     if u1:
    #         flash('Username has already been taken!', category='error')
    #     elif u2:
    #         flash('Email has already been taken!', category='error')
    #     elif len(email) < 4:
    #         flash('Email should be longer!', category='error')
    #     elif password1 != password2:
    #         flash('Passwords not match', category='error')
    #     elif len(password1) < 7:
    #         flash('password should be longer!', category='error')
    #     else:
    #         # add user to database.
    #         new_user = User(last_name=lastName, first_name=firstName, email=email, password=password2,
    #                         username=username)
    #         db.session.add(new_user)
    #         db.session.commit()
    #         login_user(new_user, remember=True)
    #         flash('Account created! Welcome ' + new_user.first_name + '!', category='success')
    #         return redirect(url_for('views.home'))
    #
    # return render_template('signUp.html', user=current_user)
    if request.method == 'POST':
        if not request.is_json:
            return make_response({'msg': "no json"}), 200

        req = request.get_json()
        username = req.get('username')
        email = req.get('email')
        firstName = req.get('firstName')
        lastName = req.get('lastName')
        password1 = req.get('password1')
        password2 = req.get('password2')

        u1 = User.query.filter_by(username=username).first()
        u2 = User.query.filter_by(email=email).first()
        if u1:
            flash('Username has already been taken!', category='error')
            return make_response(jsonify({'msg': 'invalid email taken'}), 409)
        elif u2:
            flash('Email has already been taken!', category='error')
            return make_response(jsonify({'msg': 'invalid email taken'}), 409)
        elif len(email) < 4:
            flash('Email should be longer!', category='error')
            return make_response(jsonify({'msg': 'invalid email longer'}), 409)
        elif password1 != password2:
            flash('Passwords not match', category='error')
            return make_response(jsonify({'msg': 'invalid passwords not same input'}), 409)
        elif len(password1) < 7:
            flash('password should be longer!', category='error')
            return make_response(jsonify({'msg': 'invalid password length input '}), 409)
        else:
            # add user to database.
            new_user = User(last_name=lastName, first_name=firstName, email=email, password=password2,
                            username=username)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! Welcome ' + new_user.first_name + '!', category='success')
            return make_response(redirect(url_for('views.home'))), 302
            # return redirect(url_for('views.home'))
    else:
        return make_response(render_template('signUp.html', user=current_user))
    # return render_template('signUp.html', user=current_user)

