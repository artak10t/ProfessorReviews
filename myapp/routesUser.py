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
    current_id = current_user.id
    logout_user()
    User.query.filter_by(id = current_id).delete()
    db.session.commit()
    return redirect('/')

@myapp_obj.route("/logout")
def logout():
    db.session.commit()
    logout_user()
    return redirect('/')

@myapp_obj.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeatPassword.data:
            flash('Repeated password is wrong')
            return redirect('register')
        if not form.email.data.endswith('@sjsu.edu'):
            flash('Use SJSU email for registration')
            return redirect('register')

        try:
            p = User(email=form.email.data)
            p.set_password(password=form.password.data)
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
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login invalid email or password!')
            return redirect('/login')

        login_user(user, remember=form.remember_me.data)
    
        db.session.commit()
        return redirect('/')
    return render_template("login.html", form=form, authorized=current_user.is_authenticated)