from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Census
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, EditProfileForm, CensusForm
import datetime
from datetime import datetime as dt


@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'James'}
    # posts = [
    #     {
    #         'author': {'username': 'James'},
    #         'body': 'Beautiful day in Worle!'
    #     },
    #     {
    #         'author': {'username': 'Barry'},
    #         'body': 'Flask seems pretty neat!!'
    #     }
    # ]
    return render_template('index.html', title='Home', user=User, census=Census)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    date = datetime.datetime(1990, 8, 14)
    census = [
        {'participant': user, 'name': 'A Real Name', 'dob': date}
    ]
    return render_template('user.html', user=user, census=census)


@app.before_request
def before_request():
    time = dt.utcnow()
    if current_user.is_authenticated:
        current_user.last_seen = time
        db.session.commit()


@app.route('/edit_profile', methods = ['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/census', methods=['GET', 'POST'])
@login_required
def census():
    form = CensusForm(current_user.username)
    if form.validate_on_submit():
        census = Census(name=form.name.data, dob=form.dob.data)
        print(census)
        db.session.add(census)
        db.session.commit()
        flash('Congratulations, you have submitted your information!')
    return render_template('census.html', title='Census', form=form)
