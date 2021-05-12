from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from project.app import db
from project.app.functions.functions import *
from project.model.models import Transaction

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


@transaction.route('/wire', methods=['GET', 'POST'])
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


@transaction.route('/recurring', methods=['GET', 'POST'])
@login_required
def recurring_transfer():
    return render_template('recurring_transaction.html', user=current_user)