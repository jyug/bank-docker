from flask import Blueprint, render_template, request, flash, redirect, url_for
from project.model.models import User, Account, Transaction
from project.app import db
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from random import randint
from project.app.functions.functions import *

deposits = Blueprint('deposits', __name__)


@deposits.route('/deposit_info', methods=['GET', 'POST'])
@login_required
def deposit_info():
    if request.method == 'POST':
        userid = int(request.form.get('id'))
        customer = User.query.get(userid)
        return render_template('deposit_info.html', user=current_user, customer=customer)
    return render_template('admin.html', user=current_user)


@deposits.route('/deposit', methods=['GET', 'POST'])
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
