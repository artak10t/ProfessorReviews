from myapp import myapp_obj
from flask import render_template, flash, redirect
from flask_login import current_user, login_user, logout_user, login_required
from myapp import db

@myapp_obj.route("/")
def home():
    if(current_user.is_authenticated):
        return render_template('home.html', authorized=current_user.is_authenticated, moderator=current_user.moderator)

    return render_template('home.html', authorized=current_user.is_authenticated)
