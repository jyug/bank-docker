from flask import Blueprint, render_template
from flask_login import current_user, login_required

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/test')
@login_required
def test():
    return render_template('test.html', user=current_user)