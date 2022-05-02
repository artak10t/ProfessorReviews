from myapp import myapp_obj
from myapp.forms import GrantModeratorForm, AddProfessorForm
from flask import render_template, flash, redirect
from myapp import db
from sqlalchemy.exc import IntegrityError
from myapp.models import User, Professor
from flask_login import current_user, login_required

@myapp_obj.route("/grant_moderator", methods=['GET', 'POST'])
@login_required
def grantModerator():
    if not current_user.moderator:
        flash('Invalid Access')
        return redirect('/')

    form = GrantModeratorForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            user.moderator = form.status.data
            db.session.commit()
            return redirect('/')
        except IntegrityError:
            flash('Email does not exist')
            return redirect('/')

    return render_template('grant_moderator.html', form=form, authorized=current_user.is_authenticated, moderator=current_user.moderator)

@myapp_obj.route("/add_professor", methods=['GET', 'POST'])
@login_required
def addProfessor():
    if not current_user.moderator:
        flash('Invalid Access')
        return redirect('/')

    form = AddProfessorForm()
    if form.validate_on_submit():
        try:
            professor = Professor(image=form.image.data, name=form.name.data, email=form.email.data, department=form.department.data)
            db.session.add(professor)
            db.session.commit()
            return redirect('/')
        except Exception:
            return redirect('/')

    return render_template('add_professor.html', form=form, authorized=current_user.is_authenticated, moderator=current_user.moderator)