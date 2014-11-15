import json
from flask import flash, render_template, request, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask.ext.login import (login_user, current_user, login_required, logout_user)
from FindFood import FindFood, login_manager
import firebase
from forms import LoginForm, RegisterForm
from models import User

@login_manager.user_loader
def load_user(userid):
	response = firebase.get('/users/' + userid + '.json')
	return User(userid, r['email'], r['password'],r['foods'])

@FindFood.context_processor
def inject_user():
    """Ensure that the user object and login form are available for all
        templates."""
    return dict(user=current_user, login_form=LoginForm())

@FindFood.route('/')
@FindFood.route('/index')
def index():
    form = LoginForm()
    return render_template('index.html',user=current_user, login_form=form)

@FindFood.route('/login',methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = firebase.get('/users/' + form.email.data + '.json')
        if user and check_password_hash(user['password'], form.password.data):
            u = load_user(form.email.data)
            login_user(u)
            flash('Successfully logged in.', 'enchilada!')
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid email or password.', 'enchilada :(')
        return redirect(url_for('index'))
    flash('Please enter an and password.', 'enchilada')
    return redirect(url_for('index'))
    
@FindFood.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        user_data = {
            'foods': form.foods.data,
            'email': form.email.data,
            # We store a hash of the password instead of the actual password so
            # that if our database is compromised, no one can read the
            # passwords.
            'password': generate_password_hash(form.password.data)
        }
        email = form.email.data
        ref = '/users/' + email + '.json'

        if firebase.get(ref):
            flash('Email already registered.', 'danger')
            return redirect(url_for('index'))

        firebase.put(ref, user_data)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

@FindFood.route('/team_data')
@login_required
def team_data():
    return json.dumps({
                      'team_name': current_user.email,
                      })


@FindFood.route('/logout', methods=['POST'])
@login_required
def logout():
    firebase.delete('/teams/' + current_user.email + '.json')
    logout_user()
    flash('Logged out successfully.', 'enchilada!')
    return redirect('/')
	
