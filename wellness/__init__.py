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

#def create_app():
    # app = Flask("wellness")
    
    # # Configuration
    # #app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mycomputer:RemoteGoat80085();@localhost/wellnessUsers'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # # Initialize extensions with app
    # db.init_app(app)
    
    # Configure Flask-Login
    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)
    
    # User loader function for Flask-Login
    # from .models import User
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))
    
    # # Register blueprints
    # from .auth import auth as auth_blueprint
    # app.register_blueprint(auth_blueprint)
    
    # from .main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    
    #return app

# @bp.route("/", methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get("username")
#         password = request.form.get("password")

#         # Find user in MySQL
#         user = Admin.query.filter_by(username=username).first()

#         # Validate
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             return redirect(url_for("bp.inPortal"))

#         return render_template("log.html", error="Invalid username or password")
#     return render_template("log.html")
#     #return render_template("log.html")
    #return #"<p>Hello, World!</p>"

# @bp.route("/quiz")
# def hello_worl():
#     return #"<p>Hello, quiz time!</p>"