from myapp import myapp_obj
from myapp.forms import LoginForm
from myapp.forms import RegisterForm
from flask import render_template, flash, redirect
from myapp import db
from sqlalchemy.exc import IntegrityError
from myapp.models import User
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime, timedelta

@myapp_obj.route("/delete")
@login_required
def delete():
    #current_user is our User class that is loggedin
    current_id = current_user.id
    logout_user()
    User.query.filter_by(id = current_id).delete()
    db.session.commit()
    return redirect('/')

@myapp_obj.route("/logout")
def logout():
    current_user.online = current_user.online + (datetime.utcnow() - current_user.lastOnline)
    db.session.commit()
    logout_user()
    return redirect('/')

@myapp_obj.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
	#Check if repeated password is correct
        if form.password.data != form.repeatPassword.data:
            flash('Repeated password is wrong')
            return redirect('register')

	#Handle errors for adding unique users
	#For example if username exists already
        try:
            p = User(username=form.username.data)
            p.set_password(password=form.password.data)
            p.lastOnline = datetime.utcnow()
            db.session.add(p)
            db.session.commit()
            login_user(p, remember=False)
            return redirect('/')
        except IntegrityError:
            flash('Username exists')
            return redirect('register')

    return render_template('register.html', form=form, authorized=current_user.is_authenticated)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
	#Query from database and see if user exists
	#Check the password
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login invalid username or password!')
            return redirect('/login')

        login_user(user, remember=form.remember_me.data)

        #Check if 24 hours passed and reset online timer
        if(datetime.utcnow() - current_user.lastOnline) > timedelta(1):
            current_user.online = datetime(1,1,1,0,0)
        current_user.lastOnline = datetime.utcnow()
        db.session.commit()
        return redirect('/')
    return render_template("login.html", form=form, authorized=current_user.is_authenticated)