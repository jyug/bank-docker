from flask import Blueprint, render_template, request
from project.model.models import User
from flask_login import current_user, login_required

admins = Blueprint('admin', __name__)


@admins.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template('admin.html', user=current_user)


@admins.route('/admin_search', methods=['GET', 'POST'])
@login_required
def admin_search():
    if request.method == 'POST':
        users = User.query.all()
        key = request.form.get('search')
        field = request.form.get('field')
        customers = []
        found = 1
        if field == 'firstName':
            for user in users:
                if user.first_name == key:
                    customers.append(user)
        if field == 'lastName':
            for user in users:
                if user.last_name == key:
                    customers.append(user)
        if field == 'email':
            for user in users:
                if user.email == key:
                    customers.append(user)
        if field == 'username':
            for user in users:
                if user.username == key:
                    customers.append(user)
        if len(customers) == 0:
            found = 0
    return render_template('admin_search.html', user=current_user, customers=customers, found=found)