import os

from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

database = SQLAlchemy()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "YOUR_MYSQL_DATABASE_URL_HERE"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

login_manager = LoginManager(app)
login_manager.login_view = "auth_blueprint.login"
database.init_app(app)
bcrypt = Bcrypt(app)

from blueprints.auth import auth
from blueprints.library import library

app.register_blueprint(auth)
app.register_blueprint(library)


@app.route("/")
def index():
    return redirect(url_for("auth_blueprint.login"))


if __name__ == "__main__":
    app.run()
