from flask import Blueprint, render_template, request, flash, redirect, url_for
from project.model.models import User, Account, Transaction
from project.app import db
from werkzeug.security import generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from random import randint
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
    transaction_list(transactions, current_user.accounts[checking_idx])
    if request.method == 'POST':
        search_type = request.form.get('type')
        search_val = request.form.get('val')
        trans_search, valid = search_list(transactions, search_type, search_val)
        if not valid:
            flash('Search input is invalid! Please try again!', category='error')
            return render_template('account.html', user=current_user, account=current_user.accounts[checking_idx],
                                   records=transactions, flag='check')
        return render_template('account.html', user=current_user, account=current_user.accounts[checking_idx],
                               records=trans_search, flag='check')
    return render_template('account.html', user=current_user, account=current_user.accounts[checking_idx],
                           records=transactions, flag='check')


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
    transaction_list(transactions, current_user.accounts[saving_idx])
    if request.method == 'POST':
        search_type = request.form.get('type')
        search_val = request.form.get('val')
        trans_search, valid = search_list(transactions, search_type, search_val)
        if not valid:
            flash('Search input is invalid! Please try again!', category='error')
            return render_template('account.html', user=current_user, account=current_user.accounts[saving_idx],
                                   records=transactions, flag='save')
        return render_template('account.html', user=current_user, account=current_user.accounts[saving_idx],
                               records=trans_search, flag='save')
    return render_template('account.html', user=current_user, account=current_user.accounts[saving_idx],
                           records=transactions, flag='save')


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
    transaction_list(transactions, current_user.accounts[credit_idx])
    if request.method == 'POST':
        search_type = request.form.get('type')
        search_val = request.form.get('val')
        trans_search, valid = search_list(transactions, search_type, search_val)
        if not valid:
            flash('Search input is invalid! Please try again!', category='error')
            return render_template('account.html', user=current_user, account=current_user.accounts[credit_idx],
                                   records=transactions, flag='credit')
        return render_template('account.html', user=current_user, account=current_user.accounts[credit_idx],
                               records=trans_search, flag='credit')
    return render_template('account.html', user=current_user, account=current_user.accounts[credit_idx],
                           records=transactions, flag='credit')
