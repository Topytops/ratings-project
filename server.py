"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, sessions
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


@app.route('/checking_in', methods=['POST'])
def sign_in():
	"""Adding end_users"""
	email = request.form.get("email")
	password = request.form.get("password")

	checks = User.query.filter_by(email=email).all()

	if checks == []:

		user = User(email=email,
                    password=password)
                    
		db.session.add(user)

		db.session.commit()

		return render_template("homepage.html")

	else:
		return render_template("homepage.html")
			



@app.route('/check_in')
def display_form():
	"""show checking_in form"""

	return render_template("checking_in.html")




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
