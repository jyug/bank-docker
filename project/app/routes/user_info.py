from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, jsonify
from flask_login import login_required
from project.app import db
from project.app.functions.functions import *

user = Blueprint('user', __name__)


@user.route('/user_info', methods=['GET', 'POST'])
@login_required
def user_info():
    return render_template('user_info.html', user=current_user)


@user.route('/edit_user_info', methods=['GET', 'POST'])
@login_required
def edit_user_info():
    if request.method == 'POST':
        if not request.is_json:
            return make_response({'msg': "no json"}, 200)
        req = request.get_json()
        address = req.get('address')
        firstName = req.get('firstName')
        lastName = req.get('lastName')
        password1 = req.get('password1')
        password2 = req.get('password2')
        if len(firstName) > 0:
            current_user.first_name = firstName
        if len(lastName) > 0:
            current_user.last_name = lastName
        if len(password1) > 0 and len(password2) > 0:
            if len(password1) < 7:
                flash('password should be longer!', category='error')
                return make_response(jsonify({'msg': 'invalid password length input '}), 409)
            elif password1 != password2:
                flash('Passwords not match', category='error')
                return make_response(jsonify({'msg': 'invalid password the same input '}), 409)
            else:
                current_user.password = password2
        if len(address) > 0:
            current_user.address = address
        db.session.commit()
        flash('Information changed! Welcome back ' + current_user.first_name + '!', category='success')
        return make_response(redirect(url_for('auth.user_info')), 302)
    else:
        return make_response(render_template('edit_user_info.html', user=current_user))
