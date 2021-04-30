from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Account, Payment
from . import db
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required

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


def check_email_username(s):
    c = 0
    for i in range(len(s)):
        if s[i] == '@':
            c += 1
        if s[i] == '.':
            c += 1
    if c >= 2:
        return False
    return True


@auth.route('/user_info', methods=['GET', 'POST'])
@login_required
def user_info():
    return render_template('user_info.html', user=current_user)


@auth.route('/edit_user_info', methods=['GET', 'POST'])
@login_required
def edit_user_info():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        if len(firstName) > 0:
            current_user.first_name = firstName
        if len(lastName) > 0:
            current_user.last_name = lastName
        if len(password1) > 0 and len(password2) > 0:
            if len(password1) < 7:
                flash('password should be longer!', category='error')
            elif password1 != password2:
                flash('Passwords not match', category='error')
            else:
                current_user.password = password2
        if len(address) > 0:
            current_user.address = address
        db.session.commit()
        print(current_user.accounts)
        flash('Information changed! Welcome back ' + current_user.first_name + '!', category='success')
        return redirect(url_for('auth.user_info'))
    return render_template('edit_user_info.html', user=current_user)


@auth.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        users = User.query.all()
        key = request.form.get('search')
        field = request.form.get('field')
        customers = []
        found = 1
        if field == 'firstName':
            for user in users:
                if user.first_name == key:
                    customers.append(user)
        if field == 'lastName':
            for user in users:
                if user.last_name == key:
                    customers.append(user)
        if field == 'email':
            for user in users:
                if user.email == key:
                    customers.append(user)
        if field == 'username':
            for user in users:
                if user.username == key:
                    customers.append(user)
        if len(customers) == 0:
            found = 0
        return render_template('admin.html', user=current_user, customers=customers, found=found)
    return render_template('admin.html', user=current_user)


@auth.route('/account_management', methods=['GET', 'POST'])
@login_required
def account_management():
    if request.method == 'POST':
        users = User.query.all()
        userid = int(request.form.get('id'))
        for u in users:
            if u.id == userid:
                return render_template('account_management.html', user=current_user, customer=u)
    return 'Error'


@auth.route('/open_account', methods=['GET', 'POST'])
@login_required
def open_account():
    if request.method == 'POST':
        users = User.query.all()
        balance = request.form.get('balance')
        account_type = request.form.get('type')
        customer_id = int(request.form.get('customer_id'))
        for user in users:
            if user.id == customer_id:
                new_account = Account(type=account_type, balance=balance)
                db.session.add(new_account)
                user.accounts.append(new_account)
                db.session.commit()
                flash('Account opened for ' + user.first_name + '!', category='success')
                return redirect(url_for('auth.admin'))
    return 'Error'


@auth.route('/close_account', methods=['GET', 'POST'])
@login_required
def close_account():
    if request.method == 'POST':
        users = User.query.all()
        checking = request.form.get('checking')
        saving = request.form.get('saving')
        credit = request.form.get('credit')
        customer_id = int(request.form.get('id'))
        for user in users:
            if user.id == customer_id:
                for account in user.accounts:
                    if checking:
                        if checking == account.type:
                            db.session.delete(account)
                    if saving:
                        if saving == account.type:
                            db.session.delete(account)
                    if credit:
                        if credit == account.type:
                            db.session.delete(account)
                db.session.commit()
                flash('Account closed for ' + user.first_name + '!', category='success')
                return redirect(url_for('auth.admin'))
    return 'Error'
