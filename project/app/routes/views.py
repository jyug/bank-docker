from flask import Blueprint, render_template
from flask_login import current_user, login_required
from project.app.functions.functions import *

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    transactions = []
    incomes = []
    outcomes = []
    for a in current_user.accounts:
        income, outcome = monthly_cash_flow(a)
        incomes.append(income)
        outcomes.append(outcome)
        transaction_list(transactions, a, 'home')
        transactions = transactions[:10]
    return render_template('home.html', user=current_user, records=transactions, income=incomes, outcome=outcomes)


@views.route('/test')
@login_required
def test():
    return render_template('test.html', user=current_user)