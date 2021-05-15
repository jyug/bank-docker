from flask import Blueprint, render_template
from flask_login import login_required

from app.functions.functions import *

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    transactions = []  # transaction list that will be displayed at home page
    incomes = []  # monthly incomes that will be displayed at each account block at home page
    outcomes = []  # monthly payments that will be displayed at each account block at home page
    for a in current_user.accounts:
        income, outcome = monthly_cash_flow(a)
        incomes.append(income)
        outcomes.append(outcome)
        transaction_list(transactions, a, 'home')
        transactions = transactions[:10]  # display only first 11 transactions
    return render_template('home.html', user=current_user, records=transactions, income=incomes, outcome=outcomes)
