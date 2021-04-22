from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from flask_login import current_user, login_required
from . import db


views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/user_info', methods=['GET', 'POST'])
def user_info():
    return render_template('user_info.html', user=current_user)


@views.route('/edit_user_info', methods=['GET', 'POST'])
def edit_user_info():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        address = request.form.get('address')
        if len(firstName) > 0:
            current_user.first_name = firstName
        if len(lastName) > 0:
            current_user.last_name = lastName
        if len(password1) > 0 and len(password2) > 0:
            if len(password1) < 7:
                flash('password should be longer!', category='error')
            elif password1 != password2:
                flash('Passwords not match', category='error')
            else:
                current_user.password = password2
        if len(address) > 0:
            current_user.address = address
        db.session.commit()
        flash('Information changed! Welcome back '+current_user.first_name + '!',  category='success')
        return redirect(url_for('views.user_info'))
    return render_template('edit_user_info.html', user=current_user)
