from myapp import myapp_obj
from myapp.models import Professor
from flask import render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from myapp import db

@myapp_obj.route("/")
def home():
    if(current_user.is_authenticated):
        return render_template('home.html', authorized=current_user.is_authenticated, moderator=current_user.moderator)

    return render_template('home.html', authorized=current_user.is_authenticated)

@myapp_obj.route("/search", methods=['GET'])
def search():
    name = request.args.get('name')
    search = "%{}%".format(name)
    professors = Professor.query.filter(Professor.name.like(search)).limit(12).all()
    if(current_user.is_authenticated):
        return render_template('search.html', professors=professors, authorized=current_user.is_authenticated, moderator=current_user.moderator)

    return render_template('search.html', professors=professors, authorized=current_user.is_authenticated)