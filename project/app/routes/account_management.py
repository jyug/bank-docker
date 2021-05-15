from flask import Blueprint, render_template, request, flash, make_response, jsonify, redirect, url_for
from flask_login import login_required


from project.app import db
from project.app.functions.functions import *

manage = Blueprint('manage', __name__)


@manage.route('/account_management', methods=['GET', 'POST'])
@login_required
def account_management():
    if request.method == 'POST':
        userid = int(request.form.get('id'))
        customer = User.query.get(userid)
        return render_template('account_management.html', user=current_user, customer=customer)
    return render_template('admin.html', user=current_user)


@manage.route('/open_account', methods=['GET', 'POST'])
@login_required
def open_account():
    if request.method == 'POST':
        if not request.is_json:
            return make_response({'msg': "no json"}, 200)
        req = request.get_json()
        balance = req.get('balance')
        account_type = req.get('type')
        customer_id = req.get('customer_id')

        customer = User.query.get(customer_id)
        for account in customer.accounts:
            if account.type == account_type:
                flash('For ' + customer.first_name + ' ' + customer.last_name + ', ' + account.type + ' account exists '
                                                                                                      'already!',
                      category='error')
                return make_response(redirect(url_for('views.home')), 400)
        new_account = Account(type=account_type, balance=balance,
                              number=account_number_generator(customer, account_type))
        db.session.add(new_account)
        customer.accounts.append(new_account)
        db.session.commit()
        flash('Account opened for ' + customer.first_name + ' ' + customer.last_name + '!', category='success')
        return make_response(redirect(url_for('views.home')), 200)
    return make_response(render_template('admin.html', user=current_user), 200)


@manage.route('/close_account', methods=['GET', 'POST'])
@login_required
def close_account():

    if request.method == 'POST':
        if not request.is_json:
            return make_response({'msg': "no json"}), 200
        req = request.get_json()

        checking_flag = req.get('checking')
        print(checking_flag)
        saving_flag = req.get('saving')
        credit_flag = req.get('credit')
        customer_id = int(req.get('id'))


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

        print(account_status)
        if checking_flag:
            if account_status[0] == 1:
                db.session.delete(customer.accounts[checking_idx])

            else:
                print("1")
                flash('Not able to delete account that does not exist!', category='error')
                return make_response(redirect(url_for('views.home')), 400)
        if saving_flag:
            if account_status[1] == 1:
                db.session.delete(customer.accounts[saving_idx])
            else:
                print("2")
                flash('Not able to delete account that does not exist!', category='error')
                return make_response(redirect(url_for('views.home')), 400)
        print(credit_flag)
        if credit_flag:
            if account_status[2] == 1:
                db.session.delete(customer.accounts[credit_idx])
            else:
                print("3")
                flash('Not able to delete account that does not exist!', category='error')
                return make_response(redirect(url_for('views.home')), 400)
        db.session.commit()
        flash('Account closed for ' + customer.first_name + ' ' + customer.last_name + '!', category='success')
        return make_response(redirect(url_for('views.home')), 400)
    return render_template('admin.html', user=current_user)