from random import randint
from project.model.models import User, Account
import datetime
import re
from flask_login import current_user


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


def account_number_generator(user, account_type):
    if account_type == 'checking':
        type_digit = 0
    elif account_type == 'saving':
        type_digit = 1
    else:
        type_digit = 2
    return int('8888' + '%0.4d' % randint(0, 9999) + str(type_digit) + '%0.4d' % user.id)


def transaction_sort(e):
    return e[0].time


def monthly_cash_flow(account):
    month = datetime.datetime.now().month
    income = 0
    outcome = 0
    for i in account.incomes:
        if i.time.month == month:
            income += i.amount
    for p in account.payments:
        if p.time.month == month:
            outcome += p.amount
    return income, outcome


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


def search_list(trans_list, filter_type, key):
    res = []
    if filter_type == 'amt':
        try:
            money = float(key)
            for t in trans_list:
                if t[0].amount == money:
                    res.append(t)
        except ValueError:
            return res, False
    elif filter_type == 'name':
        for t in trans_list:
            temp = re.split(': ', t[1])
            if len(temp) > 1:
                if temp[1] == key:
                    res.append(t)
    elif filter_type == 'src':
        for t in trans_list:
            if t[2] == '+':
                temp = re.split(': ', t[1])
                if len(temp) > 1:
                    if temp[1] == key:
                        res.append(t)
    elif filter_type == 'tgt':
        for t in trans_list:
            if t[2] == '-':
                temp = re.split(': ', t[1])
                if len(temp) > 1:
                    if temp[1] == key:
                        res.append(t)
    else:
        for t in trans_list:
            if t[4] == key:
                res.append(t)
    return res, True
