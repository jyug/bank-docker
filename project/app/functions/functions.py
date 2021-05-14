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


def transaction_list(transactions, account, flag):
    time = datetime.datetime.now().replace(microsecond=0)
    # According to Google, 18 months is 547.501 days, so we take 547 days as the time difference boundary
    eighteen_months = datetime.timedelta(days=547)
    if flag == 'home':
        iteration_pay = 0
        iteration_income = 0
        for p in account.payments:
            try:
                target = User.query.get(Account.query.get(p.target_id).user_id)
                t_type = Account.query.get(p.target_id).type
            except AttributeError:
                continue
            iteration_pay += 1
            if iteration_pay == 5:
                break
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
            iteration_income += 1
            if iteration_income == 5:
                break
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
    else:
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


def weekday_calculator(date_arr):
    return datetime.date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2])).strftime('%a').lower()


def datetime_str(date_arr):
    return datetime.date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))


def name_splitter(name):
    name_arr = name.split()
    if len(name_arr) > 1:
        return name_arr[0], name_arr[1]
    else:
        return name_arr[0], ''


def source_index(user, method):
    source_idx = -1
    account_type = 'checking'
    if method == 'credit':
        account_type = 'credit'
    for i in range(len(user.accounts)):
        if user.accounts[i].type == account_type:
            source_idx = i
    return source_idx


def target_account(email, first_name, last_name):
    users = User.query.all()
    for user in users:
        if user.email == email:
            if user.first_name == first_name and user.last_name == last_name:
                for account in user.accounts:
                    if account.type == 'checking':
                        return account, 'valid'
            else:
                return None, 'wrong name'
    return None, 'no email'


def internal_validation(source, destination, user):
    source_idx = -1
    destination_idx = -1
    for i in range(len(user.accounts)):
        if user.accounts[i].type == source:
            source_idx = i
        if user.accounts[i].type == destination:
            destination_idx = i
    if source_idx == -1 or destination_idx == -1:
        if source_idx == -1:
            return source_idx, destination_idx, 'no source'
        else:
            return source_idx, destination_idx, 'no target'
    if source_idx == destination_idx:
        return source_idx, destination_idx, 'same account'
    return source_idx, destination_idx, 'no error'
