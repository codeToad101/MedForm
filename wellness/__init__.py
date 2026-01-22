from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_login import LoginManager, logout_user, login_required, current_user
import time
#from .models import Admin
import pymysql
#from .models import Admin, Patient

db = SQLAlchemy()
login_manager = LoginManager()
# login_manager.login_view = "bp.login"

app = Flask("wellness")

from .secret import secreter, sqlSecret

app.secret_key = secreter
login_manager.login_view = "entry.login"
login_manager.remember_cookie_duration = timedelta(seconds=0)
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = sqlSecret
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["REMEMBER_COOKIE_DURATION"] = 0
app.config["SESSION_PERMANENT"] = False
    
    # Initialize extensions with app
db.init_app(app)

from .auth import bp as auth_bp
app.register_blueprint(auth_bp)

from .quiz import bp as response_bp
app.register_blueprint(response_bp)

from .access import bp
app.register_blueprint(bp)

@app.before_request
def make_session_permanent():
    session.permanent = False
    now = time.time()
    timeout = 600  # seconds

    if "last_seen" in session:
        if now - session["last_seen"] > timeout:
            logout_user()
            session.clear()
    session["last_seen"] = now


# @login_manager.user_loader
# def load_user(user_id):
#     return Admin.query.get(int(user_id))