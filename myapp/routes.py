from myapp import myapp_obj
from myapp.forms import ReviewForm, CommentForm
from myapp.models import Professor, Review, Like, Comment
from flask import render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from myapp import db
import hashlib

@myapp_obj.route("/")
def home():
    professors = Professor.query.order_by(Professor.rating.desc()).limit(4).all()

    if(current_user.is_authenticated):
        return render_template('home.html', professors=professors, authorized=current_user.is_authenticated, moderator=current_user.moderator)

    return render_template('home.html', professors=professors, authorized=current_user.is_authenticated)

@myapp_obj.route("/about")
def about():
    if(current_user.is_authenticated):
        return render_template('about.html', authorized=current_user.is_authenticated, moderator=current_user.moderator)

    return render_template('about.html', authorized=current_user.is_authenticated)

@myapp_obj.route("/search", methods=['GET'])
def search():
    name = request.args.get('name')
    search = "%{}%".format(name)
    professors = Professor.query.filter(Professor.name.like(search)).limit(12).all()
    if(current_user.is_authenticated):
        return render_template('search.html', professors=professors, authorized=current_user.is_authenticated, moderator=current_user.moderator)

    return render_template('search.html', professors=professors, authorized=current_user.is_authenticated)

@myapp_obj.route("/show_professor/<id>", methods=['GET', 'POST'])
@login_required
def show(id):
    professor = Professor.query.filter_by(id=id).first()
    if professor == None:
        return redirect('/')

    reviews = Review.query.filter_by(professor_id=professor.id).order_by(Review.likes.desc()).limit(30).all()
    for review in reviews:
        review.comments = Comment.query.filter_by(review_id=review.id).all()
    txtRating = 'Awesome'
    txtDifficulty = 'Impossible'

    if professor.rating >= 0:
        txtRating = 'Awful'
    if professor.rating >= 1:
        txtRating = 'Bad'
    if professor.rating >= 2:
        txtRating = 'Okay'
    if professor.rating >= 3:
        txtRating = 'Good'
    if professor.rating >= 4:
        txtRating = 'Awesome'

    if professor.difficulty >= 0:
        txtDifficulty = 'Very Easy'
    if professor.difficulty >= 1:
        txtDifficulty = 'Easy'
    if professor.difficulty >= 2:
        txtDifficulty = 'Average'
    if professor.difficulty >= 3:
        txtDifficulty = 'Hard'
    if professor.difficulty >= 4:
        txtDifficulty = 'Impossible'

    form = CommentForm()
    if form.validate_on_submit():
        try:
            hash_email = hashlib.sha256(current_user.email.encode('ascii'))
            hash_email = hash_email.hexdigest()
            hash_email = hash_email[:12]
            comment = Comment(hash_email=hash_email, review_id=form.review_id.data, message=form.message.data)
            db.session.add(comment)
            db.session.commit()
            return redirect('/show_professor/' + id)
        except Exception:
            return redirect('/show_professor/' + id)

    if(current_user.is_authenticated):
        return render_template('show_professor.html', form=form, txtDifficulty=txtDifficulty, txtRating=txtRating, reviews=reviews, professor=professor, authorized=current_user.is_authenticated, moderator=current_user.moderator)

    return render_template('show_professor.html', form=form, txtDifficulty=txtDifficulty, txtRating=txtRating, reviews=reviews, professor=professor, authorized=current_user.is_authenticated)

@myapp_obj.route("/add_review/<id>", methods=['GET', 'POST'])
@login_required
def addReview(id):
    professor = Professor.query.filter_by(id=id).first()
    if professor == None:
        return redirect('/')

    form = ReviewForm()
    if form.validate_on_submit():
        try:
            rating = 0
            if form.rating.data == 'Awesome':
                rating = 5
            elif form.rating.data == 'Good':
                rating = 4
            elif form.rating.data == 'Okay':
                rating = 3
            elif form.rating.data == 'Bad':
                rating = 2
            elif form.rating.data == 'Awful':
                rating = 1

            difficulty = 0
            if(form.difficulty.data == 'Impossible'):
                difficulty = 5
            elif(form.difficulty.data == 'Hard'):
                difficulty = 4
            elif(form.difficulty.data == 'Average'):
                difficulty = 3
            elif(form.difficulty.data == 'Easy'):
                difficulty = 2
            elif(form.difficulty.data == 'Very Easy'):
                difficulty = 1

            hash_email = hashlib.sha256(current_user.email.encode('ascii'))
            hash_email = hash_email.hexdigest()
            hash_email = hash_email[:12]
            review = Review(hash_email=hash_email, professor_id=professor.id, message=form.message.data, rating=rating, difficulty=difficulty, recommend=form.recommend.data)
            db.session.add(review)
            db.session.commit()

            reviews = Review.query.filter_by(professor_id=professor.id).all()
            avgRating = 0
            avgDifficulty = 0
            awesome = 0
            good = 0
            okay = 0
            bad = 0
            awful = 0
            for review in reviews:
                avgRating += review.rating
                avgDifficulty += review.difficulty
                if review.rating == 5:
                    awesome += 1
                elif review.rating == 4:
                    good += 1
                elif review.rating == 3:
                    okay += 1
                elif review.rating == 2:
                    bad += 1
                elif review.rating == 1:
                    awful += 1

            avgRating = round(avgRating/len(reviews), 1)
            avgDifficulty = round(avgDifficulty/len(reviews), 1)
            awesome = round(awesome/len(reviews) * 100, 1)
            good = round(good/len(reviews) * 100, 1)
            okay = round(okay/len(reviews) * 100, 1)
            bad = round(bad/len(reviews) * 100, 1)
            awful = round(awful/len(reviews) * 100, 1)

            professor.reviews = len(reviews)
            professor.rating = avgRating
            professor.difficulty = avgDifficulty
            professor.awesome = awesome
            professor.good = good
            professor.okay = okay
            professor.bad = bad
            professor.awful = awful
            db.session.commit()
            return redirect('/show_professor/' + id)
        except Exception:
            return redirect('/show_professor/' + id)

    if(current_user.is_authenticated):
        return render_template('add_review.html', form=form, authorized=current_user.is_authenticated, moderator=current_user.moderator)

    return render_template('add_review.html', form=form, authorized=current_user.is_authenticated)

@myapp_obj.route("/show_professor/<id>/like/<review_id>", methods=['GET', 'POST'])
@login_required
def GiveLike(id, review_id):
    review = Review.query.filter_by(id=review_id).first()
    if review == None:
        return redirect('/show_professor/' + id)

    try:
        likeCheck = Like.query.filter_by(user_id=current_user.id, review_id=review_id).first()
        if likeCheck == None:
            like = Like(user_id=current_user.id, review_id=review_id)
            review.likes += 1
            db.session.add(like)
        elif likeCheck != None:
            Like.query.filter_by(id=likeCheck.id).delete()
            review.likes -= 1

        db.session.commit()           
        return redirect('/show_professor/' + id)
    except Exception:
        return redirect('/show_professor/' + id)