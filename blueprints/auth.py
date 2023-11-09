from app import database, bcrypt, login_manager
from flask import Blueprint, request, redirect, render_template
from flask_login import login_user, logout_user
from models.user import User

auth = Blueprint("auth_blueprint", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route("/register", methods=["GET", "POST"])
def register():
    """
    Allow users to register with the library / book service web app
    Returns:
        (html) returns HTML template of the register form.
        (str) returns error message that the user already exists.
    """
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email_address = request.form["email"]
        password = request.form["password"]

        # check if the user already exists, return an error message if they do.
        existing_user = User.query.filter_by(email_address=email_address).first()
        if existing_user:
            return render_template('response.html', response_message="User already exists.")

        # hash the user's plaintext password.
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # create a new user object for the database.
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email_address=email_address,
            password=hashed_password
        )

        # add user to the database, and redirect the user.
        database.session.add(new_user)
        database.session.commit()
        return redirect("/login")

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Allow users to log in to the library / book service web app
    Returns:
        (html) returns HTML template of the login form.
        (str) returns error message that the login is invalid.
    """
    if request.method == "POST":
        # Get email & password from the request form.
        email_address = request.form["email"]
        password = request.form["password"]

        # Query database for a user with that email address.
        user = User.query.filter_by(email_address=email_address).first()

        # Check if the user exists and the password is correct.
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect("/library/all")
        else:
            return render_template('response.html', response_message="That login is invalid.")

    return render_template("login.html")


@auth.route("/logout", methods=["GET"])
def logout():
    """
    Use flask_login library to log out the user.
    Returns:
        (str) message that the user has logged out.
    """
    logout_user()
    return render_template('response.html', response_message="logged out successfully.")
