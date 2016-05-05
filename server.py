"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Ratings, Movies


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/users')
def user_list():
	"""Show list of users"""

	users = User.query.all()
	return render_template("user_list.html", users=users)


@app.route('/sign_in', methods=['POST'])
def sign_in():
	"""Adding end_users"""
	email = request.form.get("email")
	password = request.form.get("password")

	checks = User.query.filter_by(email=email).first()

	if checks == None:

		user = User(email=email,
                    password=password)
                    
		db.session.add(user)
		db.session.commit()

		return render_template("homepage.html")

	else:
		session["user_id"] = checks.user_id
		flash('You were successfully logged in')
		return render_template("homepage.html")


@app.route('/logout')
def logout():
	"""Logging out"""
	session.pop('user_id', None)
	flash('you were logged out')
	return render_template("homepage.html")

			
@app.route('/login')
def display_form():
	"""show login form"""

	return render_template("login.html")


@app.route('/users/<user_id>')
def user_page(user_id):
	""" get user info page """

	user = User.query.filter_by(user_id=user_id).first()

	user_ratings = db.session.query(Movies.title, Ratings.movie_id, Ratings.score, Ratings.user_id).join(Ratings).filter_by(user_id=user_id)

	return render_template("user_detail.html", user_id=user, user_ratings=user_ratings)


@app.route('/movies')
def movie_list():
	"""Show list of movies"""

	movies = Movies.query.order_by(Movies.title).all()
	return render_template("movie_list.html", movies=movies)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
