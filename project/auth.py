from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Account, Transaction
from . import db
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from random import randint
import datetime

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
        userid = int(request.form.get('id'))
        customer = User.query.get(userid)
        return render_template('account_management.html', user=current_user, customer=customer)
    return render_template('admin.html', user=current_user)


@auth.route('/open_account', methods=['GET', 'POST'])
@login_required
def open_account():
    if request.method == 'POST':
        balance = request.form.get('balance')
        account_type = request.form.get('type')
        customer_id = int(request.form.get('customer_id'))
        customer = User.query.get(customer_id)
        for account in customer.accounts:
            if account.type == account_type:
                flash('For ' + customer.first_name + ' ' + customer.last_name + ', ' + account.type + ' account exists '
                                                                                                      'already!',
                      category='error')
                return render_template('admin.html', user=current_user, customers=[customer], found=1)
        new_account = Account(type=account_type, balance=balance,
                              number=account_number_generator(customer, account_type))
        db.session.add(new_account)
        customer.accounts.append(new_account)
        db.session.commit()
        flash('Account opened for ' + customer.first_name + ' ' + customer.last_name + '!', category='success')
        return render_template('admin.html', user=current_user, customers=[customer], found=1)
    return render_template('admin.html', user=current_user)


@auth.route('/close_account', methods=['GET', 'POST'])
@login_required
def close_account():
    if request.method == 'POST':
        checking_flag = request.form.get('checking')
        saving_flag = request.form.get('saving')
        credit_flag = request.form.get('credit')
        customer_id = int(request.form.get('id'))
        customer = User.query.get(customer_id)
        # A list contain 3 integer 0/1 to indicate whether the customer has checking/saving/credit account
        account_status = [0, 0, 0]
        for i in range(len(customer.accounts)):
            if customer.accounts[i].type == 'checking':
                checking_idx = i
                account_status[0] = 1
            if customer.accounts[i].type == 'saving':
                saving_idx = i
                account_status[1] = 1
            if customer.accounts[i].type == 'credit':
                credit_idx = i
                account_status[2] = 1

        if checking_flag:
            if account_status[0] == 1:
                db.session.delete(customer.accounts[checking_idx])

            else:
                flash('Not able to delete account that does not exist!', category='error')
                return render_template('admin.html', user=current_user, customers=[customer], found=1)
        if saving_flag:
            if account_status[1] == 1:
                db.session.delete(customer.accounts[saving_idx])
            else:
                flash('Not able to delete account that does not exist!', category='error')
                return render_template('admin.html', user=current_user, customers=[customer], found=1)
        if credit_flag:
            if account_status[2] == 1:
                db.session.delete(customer.accounts[credit_idx])
            else:
                flash('Not able to delete account that does not exist!', category='error')
                return render_template('admin.html', user=current_user, customers=[customer], found=1)
        db.session.commit()
        flash('Account closed for ' + customer.first_name + ' ' + customer.last_name + '!', category='success')
        return render_template('admin.html', user=current_user, customers=[customer], found=1)
    return render_template('admin.html', user=current_user)


def account_number_generator(user, account_type):
    if account_type == 'checking':
        type_digit = 0
    elif account_type == 'saving':
        type_digit = 1
    else:
        type_digit = 2
    return int('8888' + '%0.4d' % randint(0, 9999) + str(type_digit) + '%0.4d' % user.id)


@auth.route('/deposit_info', methods=['GET', 'POST'])
@login_required
def deposit_info():
    if request.method == 'POST':
        userid = int(request.form.get('id'))
        customer = User.query.get(userid)
        return render_template('deposit_info.html', user=current_user, customer=customer)
    return render_template('admin.html', user=current_user)


@auth.route('/deposit', methods=['GET', 'POST'])
@login_required
def deposit():
    if request.method == 'POST':
        money = float(request.form.get('money'))
        account_type = request.form.get('account')
        method = request.form.get('method')
        customer_id = int(request.form.get('customer_id'))
        customer = User.query.get(customer_id)
        for account in customer.accounts:
            if account.type == account_type:
                transaction = Transaction(type='deposit', amount=money,
                                          target_id=account.id,
                                          source_id=1,
                                          time=datetime.datetime.now(),
                                          description='Deposit by ' + method)
                account.incomes.append(transaction)
                account.balance += money
                db.session.add(transaction)
                db.session.commit()
                flash('$' + str(money) + 'has been added to ' + customer.first_name + ' '
                      + customer.last_name + 's ' + account_type + ' account!', category='success')
                return render_template('admin.html', user=current_user, customers=[customer], found=1)
        flash('This customer does not have ' + account_type + ' yet!', category='error')
        return render_template('admin.html', user=current_user, customers=[customer], found=1)


@auth.route('/checking', methods=['GET', 'POST'])
@login_required
def checking():
    if request.method == 'POST':
        search_type = request.form.get('type')
        search_val = request.form.get('val')
        search_transaction = Transaction.query.get(search_val)
    checking_idx = -1
    for i in range(len(current_user.accounts)):
        if current_user.accounts[i].type == 'checking':
            checking_idx = i

    if checking_idx == -1:
        return render_template('account.html', user=current_user, account=None, records=None, flag='check')
    transactions = []
    transaction_list(transactions, current_user.accounts[checking_idx])
    return render_template('account.html', user=current_user, account=current_user.accounts[checking_idx],
                           records=transactions, flag='check')


@auth.route('/saving', methods=['GET', 'POST'])
@login_required
def saving():
    saving_idx = -1
    for i in range(len(current_user.accounts)):
        if current_user.accounts[i].type == 'saving':
            saving_idx = i
    if saving_idx == -1:
        return render_template('account.html', user=current_user, account=None, records=None, flag='save')
    transactions = []
    transaction_list(transactions, current_user.accounts[saving_idx])
    return render_template('account.html', user=current_user, account=current_user.accounts[saving_idx],
                           records=transactions, flag='save')


@auth.route('/credit', methods=['GET', 'POST'])
@login_required
def credit():
    credit_idx = -1
    for i in range(len(current_user.accounts)):
        if current_user.accounts[i].type == 'credit':
            credit_idx = i
    if credit_idx == -1:
        return render_template('account.html', user=current_user, account=None, records=None, flag='credit')
    transactions = []
    transaction_list(transactions, current_user.accounts[credit_idx])
    return render_template('account.html', user=current_user, account=current_user.accounts[credit_idx],
                           records=transactions, flag='credit')


@auth.route('/internal_trans', methods=['GET', 'POST'])
@login_required
def internal_trans():
    if request.method == 'POST':
        money = float(request.form.get('money'))
        if money <= 0:
            flash('Invalid money amount!', category='error')
            return render_template('internal_trans.html', user=current_user)
        source = request.form.get('source')
        destination = request.form.get('destination')
        source_idx = -1
        destination_idx = -1
        for i in range(len(current_user.accounts)):
            if current_user.accounts[i].type == source:
                source_idx = i
            if current_user.accounts[i].type == destination:
                destination_idx = i
        if source_idx == -1 or destination_idx == -1:
            if source_idx == -1:
                flash('You do not have a ' + source + ' account yet, not able to issue transaction!',
                      category='error')
                return render_template('internal_trans.html', user=current_user)
            if destination_idx == -1:
                flash('You do not have a ' + destination + ' account yet, not able to issue transaction!',
                      category='error')
                return render_template('internal_trans.html', user=current_user)
        if source_idx == destination_idx:
            flash('Can not transfer between same accounts!', category='error')
            return render_template('internal_trans.html', user=current_user)
        else:
            transaction = Transaction(type='internal', amount=money,
                                      target_id=current_user.accounts[destination_idx].id,
                                      source_id=current_user.accounts[source_idx].id,
                                      time=datetime.datetime.now(),
                                      description='Internal transfer')

            current_user.accounts[source_idx].payments.append(transaction)
            current_user.accounts[destination_idx].incomes.append(transaction)
            current_user.accounts[source_idx].balance -= money
            current_user.accounts[destination_idx].balance += money
            db.session.add(transaction)
            db.session.commit()
            flash('Successfully issued an internal money transfer!', category='success')
            return render_template('internal_trans.html', user=current_user)
    return render_template('internal_trans.html', user=current_user)


@auth.route('/wire', methods=['GET', 'POST'])
@login_required
def wire():
    if request.method == 'POST':
        money = float(request.form.get('money'))
        if money <= 0:
            flash('Invalid money amount!', category='error')
            return render_template('wire.html', user=current_user)
        name = request.form.get('name')
        firstName = name.split()[0]
        lastName = name.split()[1]
        email = request.form.get('email')
        note = request.form.get('note')
        method = request.form.get('method')
        users = User.query.all()
        source_idx = -1
        account_type = 'checking'
        if method == 'credit':
            account_type = 'credit'
        for i in range(len(current_user.accounts)):
            if current_user.accounts[i].type == account_type:
                source_idx = i
        if source_idx not in [0, 1, 2]:
            flash('You do not have a checking account yet, please contact the bank to open!', category='error')
            return redirect(url_for('views.home'))
        for user in users:
            if user.email == email:
                if user.first_name == firstName and user.last_name == lastName:
                    for account in user.accounts:
                        if account.type == 'checking':
                            transaction = Transaction(type=method, amount=money,
                                                      target_id=account.id,
                                                      source_id=current_user.accounts[source_idx].id,
                                                      description=note,
                                                      time=datetime.datetime.now())

                            current_user.accounts[source_idx].payments.append(transaction)
                            account.incomes.append(transaction)

                            if money > current_user.accounts[source_idx].balance:
                                flash('You do not have enough money!', category='error')
                                return render_template('wire.html', user=current_user)
                            else:
                                current_user.accounts[source_idx].balance -= money
                                account.balance += money
                                db.session.add(transaction)
                                db.session.commit()
                                flash('Wire transfer complete!', category='success')
                                return redirect(url_for('views.home'))
                    flash('The target user do not have a checking account yet, unable to issue the transfer!',
                          category='error')
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect name! Not able to issue the wire transfer!', category='error')
                    return render_template('wire.html', user=current_user)
        flash('Email not found! No such user!', category='error')
        return render_template('wire.html', user=current_user)
    return render_template('wire.html', user=current_user)


def transaction_sort(e):
    return e[0].time


def transaction_list(transactions, account):
    time = datetime.datetime.now().replace(microsecond=0)
    # According to Google, 18 months is 547.501 days, so we take 547 days as the time difference boundary
    eighteen_months = datetime.timedelta(days=547)
    for p in account.payments:
        try:
            target = User.query.get(Account.query.get(p.target_id).user_id)
            t_type = Account.query.get(p.target_id).type
        except AttributeError:
            continue

        payment_time_diff = time - p.time.replace(microsecond=0)
        if eighteen_months > payment_time_diff:
            if target.id == current_user.id:
                notation = 'Internal transaction to: ' + str(t_type)
            else:
                if p.type == 'deposit':
                    notation = 'Deposit to: ' + str(target.first_name) + ' ' + str(target.last_name)
                else:
                    notation = 'Payment to: ' + str(target.first_name) + ' ' + str(target.last_name)
            transactions.append((p, notation, '-', t_type, p.type, p.description))
        else:
            pass
    for i in account.incomes:
        try:
            source = User.query.get(Account.query.get(i.source_id).user_id)
            s_type = Account.query.get(i.source_id).type
        except AttributeError:
            continue

        income_time_diff = time - i.time.replace(microsecond=0)
        if eighteen_months > income_time_diff:
            if source.id == current_user.id:
                notation = 'Internal transaction from: ' + str(s_type)
            else:
                if i.type == 'deposit':
                    notation = 'Deposit'
                else:
                    notation = 'Income from: ' + str(source.first_name) + ' ' + str(source.last_name)
            transactions.append((i, notation, '+', s_type, i.type, i.description))
        else:
            pass
    transactions.sort(reverse=True, key=transaction_sort)


@auth.route('/recurring', methods=['GET', 'POST'])
@login_required
def recurring_transfer():
    return render_template('recurring_transaction.html', user=current_user)
