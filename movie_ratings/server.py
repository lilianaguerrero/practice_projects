"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, redirect, request, flash,
                   session)

from model import User, Rating, Movie, connect_to_db, db



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# raises an error for undefined variables
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/login')
def login():
    login_email = request.args.get("email")
    login_password = request.args.get("password")

    new_user_record = User.query.filter(User.email == login_email).first() 
    if new_user_record.password == login_password:
        print('Trueeeee')

    

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/register", methods=["GET"])
def register_form():
    
    return render_template("register_form.html")

@app.route("/register", methods=["POST"])
def register_process():
    new_email = request.form.get("email")
    new_password = request.form.get("password")

    if not User.query.filter(User.email == new_email).first():
        new_user = User(email=new_email, password=new_password)
        db.session.add(new_user)
        db.session.commit()


    return redirect("/")

if __name__ == "__main__":
    # set debug=True here, since it has to be True to invoke the DebugToolbarExtension
    app.debug = True
    # ensures templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
