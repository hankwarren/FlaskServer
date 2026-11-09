from flask import Blueprint, flash, render_template
from flask import redirect, url_for
from flask_login import current_user, login_user, logout_user
import sqlalchemy as sa
from app import db 
from app.models import User
from app.forms import LoginForm

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    user = {'username': 'Hank'}

    trips = [
        {
            'driver': {'username': 'Hank'},
            'duration': '20 seconds',
            'time': '12:00 am'
        },
        {
            'driver': {'username': 'Hank'},
            'duration': '30 seconds',
            'time': '1:00 am'
        }

    ]
    return render_template('index.html', title='Home', user=user, trips=trips)

@main.route('/profile')
def profile():
    return render_template('profile.html')  

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():

        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
