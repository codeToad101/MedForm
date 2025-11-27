from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import logout_user
from wellness import login_manager
from werkzeug.security import generate_password_hash
from .models import Admin, staffURL
from . import db

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("entry.login"))

@bp.route('/portal/registration//<token>', methods=['GET', 'POST'])
def register(token):
    
    key = staffURL.query.filter_by(token=token).first()

    if not key:
        return "Invalid link", 404
    
    if key.used:
        return "This link has already been used.", 403
    
    if request.method == 'GET':
        return render_template("register.html", token=token)

    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    userName = request.form.get("userName")
    password = request.form.get("password")
    mail = request.form.get("email")
    #answers = request.form.getlist("answer")
    #answers = [request.form.get(f"ans{i}") for i in range(1, 11)]
    #print(answers[0])

    mannequin = Admin(
        username = userName,
        password_hash = generate_password_hash(password),
        first_name=firstName,
        last_name=lastName,
        email = mail
    )
    db.session.add(mannequin)
    key.used = True
    db.session.commit()

    return render_template("thanks.html")