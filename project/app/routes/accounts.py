from flask import Blueprint, render_template, request, flash
from flask_login import login_required
from project.app.functions.functions import *

accounts = Blueprint('accounts', __name__)


@accounts.route('/checking', methods=['GET', 'POST'])
@login_required
def checking():
    checking_idx = -1
    for i in range(len(current_user.accounts)):
        if current_user.accounts[i].type == 'checking':
            checking_idx = i
    if checking_idx == -1:
        return render_template('account.html', user=current_user, account=None, records=None, flag='check')
    transactions = []
    transaction_list(transactions, current_user.accounts[checking_idx], 'checking')
    income, outcome = monthly_cash_flow(current_user.accounts[checking_idx])
    if request.method == 'POST':
        search_type = request.form.get('type')
        search_val = request.form.get('val')
        trans_search, valid = search_list(transactions, search_type, search_val)
        if not valid:
            flash('Search input is invalid! Please try again!', category='error')
            return render_template('account.html', user=current_user, account=current_user.accounts[checking_idx],
                                   records=transactions, flag='check', income=income, outcome=outcome)
        return render_template('account.html', user=current_user, account=current_user.accounts[checking_idx],
                               records=trans_search, flag='check', income=income, outcome=outcome)
    return render_template('account.html', user=current_user, account=current_user.accounts[checking_idx],
                           records=transactions, flag='check', income=income, outcome=outcome)


@accounts.route('/saving', methods=['GET', 'POST'])
@login_required
def saving():
    saving_idx = -1
    for i in range(len(current_user.accounts)):
        if current_user.accounts[i].type == 'saving':
            saving_idx = i
    if saving_idx == -1:
        return render_template('account.html', user=current_user, account=None, records=None, flag='save')
    transactions = []
    transaction_list(transactions, current_user.accounts[saving_idx], 'saving')
    income, outcome = monthly_cash_flow(current_user.accounts[saving_idx])
    if request.method == 'POST':
        search_type = request.form.get('type')
        search_val = request.form.get('val')
        trans_search, valid = search_list(transactions, search_type, search_val)
        if not valid:
            flash('Search input is invalid! Please try again!', category='error')
            return render_template('account.html', user=current_user, account=current_user.accounts[saving_idx],
                                   records=transactions, flag='save', income=income, outcome=outcome)
        return render_template('account.html', user=current_user, account=current_user.accounts[saving_idx],
                               records=trans_search, flag='save', income=income, outcome=outcome)
    return render_template('account.html', user=current_user, account=current_user.accounts[saving_idx],
                           records=transactions, flag='save', income=income, outcome=outcome)


@accounts.route('/credit', methods=['GET', 'POST'])
@login_required
def credit():
    credit_idx = -1
    for i in range(len(current_user.accounts)):
        if current_user.accounts[i].type == 'credit':
            credit_idx = i
    if credit_idx == -1:
        return render_template('account.html', user=current_user, account=None, records=None, flag='credit')
    transactions = []
    transaction_list(transactions, current_user.accounts[credit_idx], 'credit')
    income, outcome = monthly_cash_flow(current_user.accounts[credit_idx])
    if request.method == 'POST':
        search_type = request.form.get('type')
        search_val = request.form.get('val')
        trans_search, valid = search_list(transactions, search_type, search_val)
        if not valid:
            flash('Search input is invalid! Please try again!', category='error')
            return render_template('account.html', user=current_user, account=current_user.accounts[credit_idx],
                                   records=transactions, flag='credit', income=income, outcome=outcome)
        return render_template('account.html', user=current_user, account=current_user.accounts[credit_idx],
                               records=trans_search, flag='credit', income=income, outcome=outcome)
    return render_template('account.html', user=current_user, account=current_user.accounts[credit_idx],
                           records=transactions, flag='credit', income=income, outcome=outcome)
