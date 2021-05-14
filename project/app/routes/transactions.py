from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from project.app import db
from project.app.functions.functions import *
from project.model.models import Transaction
from project.app import scheduler

transaction = Blueprint('transaction', __name__)


@transaction.route('/internal_trans', methods=['GET', 'POST'])
@login_required
def internal_trans():
    if request.method == 'POST':
        money = float(request.form.get('money'))
        if money <= 0:
            flash('Invalid money amount!', category='error')
            return render_template('internal_trans.html', user=current_user)
        source = request.form.get('source')
        destination = request.form.get('destination')
        source_idx, destination_idx, error = internal_validation(source, destination, current_user)
        if error == 'no source':
            flash('You do not have a ' + source + ' account yet, not able to issue transaction!',
                  category='error')
            return render_template('internal_trans.html', user=current_user)
        elif error == 'no target':
            flash('You do not have a ' + destination + ' account yet, not able to issue transaction!',
                  category='error')
            return render_template('internal_trans.html', user=current_user)
        elif error == 'same account':
            flash('Can not transfer between same accounts!', category='error')
            return render_template('internal_trans.html', user=current_user)
        else:
            if money > current_user.accounts[source_idx].balance:
                flash('You do not have enough money!', category='error')
                return render_template('internal_trans.html', user=current_user)
            transaction_generator(current_user.accounts[source_idx],
                                  current_user.accounts[destination_idx], money, 'Internal transfer', 'internal')
            flash('Successfully issued an internal money transfer!', category='success')
            return render_template('internal_trans.html', user=current_user)
    return render_template('internal_trans.html', user=current_user)


@transaction.route('/re_internal', methods=['GET', 'POST'])
@login_required
def re_internal():
    if request.method == 'POST':
        date = request.form.get('date')
        if not date:
            flash('Please select the start date!', category='error')
            return render_template('re_wire.html', user=current_user)
        money = float(request.form.get('money'))
        if money <= 0:
            flash('Invalid money amount!', category='error')
            return render_template('re_internal.html', user=current_user)
        source = request.form.get('source')
        destination = request.form.get('destination')
        period = request.form.get('period')
        date_arr = date.split('-')
        source_idx, destination_idx, error = internal_validation(source, destination, current_user)
        if error == 'no source':
            flash('You do not have a ' + source + ' account yet, not able to issue transaction!',
                  category='error')
            return render_template('re_internal.html', user=current_user)
        elif error == 'no target':
            flash('You do not have a ' + destination + ' account yet, not able to issue transaction!',
                  category='error')
            return render_template('re_internal.html', user=current_user)
        elif error == 'same account':
            flash('Can not transfer between same accounts!', category='error')
            return render_template('re_internal.html', user=current_user)
        else:
            if money > current_user.accounts[source_idx].balance:
                flash('You do not have enough money!', category='error')
                return render_template('re_internal.html', user=current_user)
            recurring_execution(current_user.accounts[source_idx].id, current_user.accounts[destination_idx].id,
                                money, 'Recurring internal transfer', period, date_arr)
            flash('Successfully issued an internal money transfer!', category='success')
            return render_template('internal_trans.html', user=current_user)
    return render_template('re_internal.html', user=current_user)


@transaction.route('/wire', methods=['GET', 'POST'])
@login_required
def wire():
    if request.method == 'POST':
        money = float(request.form.get('money'))
        if money <= 0:
            flash('Invalid money amount!', category='error')
            return render_template('wire.html', user=current_user)
        name = request.form.get('name')
        firstName, lastName = name_splitter(name)
        email = request.form.get('email')
        note = request.form.get('note')
        method = request.form.get('method')
        source_idx = source_index(current_user, method)
        if source_idx not in [0, 1, 2]:
            flash('You do not have a checking account yet, please contact the bank to open!', category='error')
            return redirect(url_for('views.home'))
        account, flag = target_account(email, firstName, lastName)
        if flag == 'no email':
            flash('Email not found! No such user!', category='error')
            return render_template('wire.html', user=current_user)
        elif flag == 'wrong name':
            flash('Incorrect name! Not able to issue the wire transfer!', category='error')
            return render_template('wire.html', user=current_user)
        elif not account:
            flash('The target user do not have a checking account yet, unable to issue the transfer!',
                  category='error')
            return redirect(url_for('views.home'))
        else:
            if money > current_user.accounts[source_idx].balance:
                flash('You do not have enough money!', category='error')
                return render_template('wire.html', user=current_user)
            else:
                transaction_generator(current_user.accounts[source_idx], account, money, note, method)
                flash('Wire transfer complete!', category='success')
                return redirect(url_for('views.home'))
    return render_template('wire.html', user=current_user)


@transaction.route('/re_wire', methods=['GET', 'POST'])
@login_required
def re_wire():
    if request.method == 'POST':
        date = request.form.get('date')
        if not date:
            flash('Please select the start date!', category='error')
            return render_template('re_wire.html', user=current_user)
        money = float(request.form.get('money'))
        if money <= 0:
            flash('Invalid money amount!', category='error')
            return render_template('re_wire.html', user=current_user)
        name = request.form.get('name')
        firstName, lastName = name_splitter(name)
        email = request.form.get('email')
        description = request.form.get('note')
        method = request.form.get('method')
        period = request.form.get('period')
        date_arr = date.split('-')
        source_idx = source_index(current_user, method)
        if source_idx not in [0, 1, 2]:
            flash('You do not have a ' + method + " account yet, please contact the bank to open!", category='error')
            return redirect(url_for('views.home'))
        account, flag = target_account(email, firstName, lastName)
        if flag == 'no email':
            flash('Email not found! No such user!', category='error')
            return render_template('re_wire.html', user=current_user)
        elif flag == 'wrong name':
            flash('Incorrect name! Not able to issue the wire transfer!', category='error')
            return render_template('re_wire.html', user=current_user)
        elif not account:
            flash('The target user do not have a checking account yet, unable to issue the transfer!',
                  category='error')
            return redirect(url_for('views.home'))
        else:
            if money > current_user.accounts[source_idx].balance:
                flash('You do not have enough money!', category='error')
                return render_template('re_wire.html', user=current_user)
            else:
                recurring_execution(current_user.accounts[source_idx].id, account.id,
                                    money, description, period, date_arr)
                flash('Recurring wire transfer set!', category='success')
                return redirect(url_for('views.home'))
    return render_template('re_wire.html', user=current_user)


@transaction.route('/recurring', methods=['GET', 'POST'])
@login_required
def recurring_transfer():
    if request.method == 'POST':
        method = request.form.get('method')
        if method == 'internal':
            return render_template('re_internal.html', user=current_user)
        elif method == 'wire':
            return render_template('re_wire.html', user=current_user)
        else:
            jobs = scheduler.get_jobs()
            jobs_id = [(job.id, job.name) for job in jobs]
            return render_template('re_cancel.html', user=current_user, jobs=jobs_id)
    return render_template('recurring_transaction.html', user=current_user)


@transaction.route('/re_cancel', methods=['GET', 'POST'])
@login_required
def re_cancel():
    if request.method == 'POST':
        job_id = request.form.get('cancel')
        print(job_id)
        scheduler.delete_job(job_id)
        flash('Job deleted!', category='success')
        return redirect(url_for('views.home'))


def recurring_execution(src_id, tgt_id, money, description, period, date_arr):
    src_acc = Account.query.get(src_id)
    tgt_acc = Account.query.get(tgt_id)
    src = User.query.get(src_acc.user_id)
    tgt = User.query.get(tgt_acc.user_id)
    date = datetime_str(date_arr)
    job_id = ''
    name = ''
    if src.id == tgt.id:
        job_id += ('Internal' + str(src_acc.id) + str(tgt_acc.id) + str(date))
        name += ('Internal recurring: from ' + src_acc.type + ' to '
                 + tgt_acc.type + ', ' + period + ', starting on ' + str(date)
                 + ', amount: $' + str(money))
    else:
        job_id += ('Wire' + str(src_acc.id) + str(tgt_acc.id) + str(date))
        name += ('Wire recurring: to ' + tgt.first_name + ' '
                 + tgt.last_name + ', ' + period + ', starting on ' + str(date)
                 + ', amount: $' + str(money))

    if period == 'demo':
        scheduler.add_job(id=job_id, name=name,
                          func=recurring_transaction_generator,
                          trigger='interval',
                          seconds=5, args=[src_id, tgt_id, money, description, 'recurring demo'])
    elif period == 'daily':
        scheduler.add_job(id=job_id, name=name,
                          func=recurring_transaction_generator,
                          trigger='cron',
                          day='*', hour=5, minute=30, args=[src_id, tgt_id, money, description, 'daily recurring wire'])
    elif period == 'weekly':
        weekday = weekday_calculator(date_arr)
        scheduler.add_job(id=job_id, name=name,
                          func=recurring_transaction_generator,
                          trigger='cron',
                          day_of_week=weekday, hour=5, minute=30,
                          args=[src_id, tgt_id, money, description, 'weekly recurring wire'])
    elif period == 'monthly':
        scheduler.add_job(id=job_id, name=name,
                          func=recurring_transaction_generator,
                          trigger='cron',
                          month='*', day=date_arr[2], hour=5, minute=30,
                          args=[src_id, tgt_id, money, description, 'weekly recurring wire'])
    else:
        scheduler.add_job(id=job_id, name=name,
                          func=recurring_transaction_generator,
                          trigger='cron',
                          year='*', month=date_arr[1], day=date_arr[2], hour=5, minute=30,
                          args=[src_id, tgt_id, money, description, 'weekly recurring wire'])


def recurring_transaction_generator(src_id, tgt_id, money, des, method):
    with scheduler.app.app_context():
        src = Account.query.get(src_id)
        tgt = Account.query.get(tgt_id)
        if money > src.balance:
            flash('You don not have enough money for recurring payment to', User.query.get(tgt.user_id).first_name)
            return 1
        src.balance -= money
        tgt.balance += money
        trans = Transaction(type=method, amount=money, target_id=tgt_id, source_id=src_id,
                            time=datetime.datetime.now(), description=des)
        src.payments.append(trans)
        tgt.incomes.append(trans)
        db.session.add(trans)
        db.session.commit()
        print('transaction complete!')


def transaction_generator(src_account, tgt_account, amount, description, method):
    trans = Transaction(type=method, amount=amount, target_id=tgt_account.id, source_id=src_account.id,
                        time=datetime.datetime.now(), description=description)
    src_account.balance -= amount
    src_account.payments.append(trans)
    tgt_account.balance += amount
    tgt_account.incomes.append(trans)
    db.session.add(trans)
    db.session.commit()
