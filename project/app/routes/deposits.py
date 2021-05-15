from flask import Blueprint, render_template, request, flash, make_response, jsonify, redirect, url_for
from flask_login import login_required
from project.app import db
from project.app.functions.functions import *
from project.model.models import Transaction

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
        if not request.is_json:
            return make_response({'msg': "no json"}, 200)
        req = request.get_json()
        money = float(req.get('money'))
        account_type = req.get('account')
        method = req.get('method')
        customer_id = int(req.get('customer_id'))
        # money = float(request.form.get('money'))
        # account_type = request.form.get('account')
        # method = request.form.get('method')
        # customer_id = int(request.form.get('customer_id'))
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
                # return render_template('admin.html', user=current_user, customers=[customer], found=1)
                return make_response(redirect(url_for('views.home')), 200)
        flash('This customer does not have ' + account_type + ' yet!', category='error')
        # return render_template('admin.html', user=current_user, customers=[customer], found=1)
        return make_response(render_template('admin.html', user=current_user, customers=[customer], found=1), 400)