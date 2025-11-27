#this is admin routes
from flask import Blueprint, Flask, request, render_template, redirect, url_for, session
from werkzeug.security import check_password_hash
import secrets
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash
from . import db
from .models import Admin, validURL, staffURL, Patient
from thefuzz import fuzz, process
from sqlalchemy import or_, func
#from .quiz import bp as response

bp = Blueprint('entry', __name__)

@bp.route("/", methods=['GET', 'POST']) #add an "i forgot" demo to b integrated w email recovery
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        # Find user in MySQL
        user = Admin.query.filter_by(username=username).first()

        # Validate
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=False)
            return redirect(url_for("entry.inPortal"))

        return render_template("log.html", error="Invalid username/password")
    return render_template("log.html")
    #return render_template("log.html")

@bp.route('/portal', methods=['GET', 'POST']) #still auto-remembering...bad
@login_required
def inPortal():

    generated_url = None
    staff_url = None
    results =[]

    if request.method == "POST":
        action = request.form.get("btn") or request.form.get("top_btn")

        if action == "team":
            staff_url = Staff_URL_maker()
            #return redirect(url_for("auth.register"))
        elif action == "intake":
            generated_url = URL_maker()
        elif action == "info":
            search_value = request.form.get("search_value", "").strip()

            if search_value:
                first_letter = search_value[0].lower()

            # Step 1: Filter database by first letter
                matching_rows = (
                    Patient.query.filter(
                        or_(
                            func.lower(Patient.first_name).like(f"{first_letter}%"),
                            func.lower(Patient.last_name).like(f"{first_letter}%")
                        )
                    ).all()
                )

                choices = { p.id: f"{p.first_name} {p.last_name}" for p in matching_rows }


            # Step 2: Fuzzy search
                fuzzy_matches = process.extract(search_value, choices, scorer=fuzz.WRatio, limit=10)


            # Step 3: Filter by score
                #threshold = 70
                #good = [m for m in fuzzy_matches if m[1] >= threshold]

                results = [
                    {
                        "id": id_key,
                        "name": matched_name,
                        "score": score
                    }
                    for matched_name, score, id_key in fuzzy_matches
                    if score >= 70
                ]
            # Step 4: Map back to rows
                #results = []
                # for matched_name, score in good:
                #     match = next((n for n in name_pairs if n[1] == matched_name), None) #need to make much looser lol
                #     if match:
                #         results.append({
                #             "id": match[0],
                #             "name": match[1],
                #         #"score": score
                #         })

    #return render_template("portal.html")
    return render_template(
        "portal.html",
        first_name=current_user.first_name,
        generated_url=generated_url,
        staff_url=staff_url,
        results=results
    )
    #return render_template("portal.html", first_name=current_user.first_name)

@bp.route("/portal/patient/<int:patient_id>") #notes add ability to change
@login_required
def patient_profile(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    return render_template( #need to make it so data provides not js MCQ answers but whole thing--
        "patient_profile.html", #ez fix js have to touch up SQL too
        patient=patient
    )


def URL_maker():
    t = validURL(token=secrets.token_urlsafe(32))
    db.session.add(t)
    db.session.commit()
    full_url = url_for("response.quiz", token=t.token, _external=True)
    return full_url
    #return t.token

def Staff_URL_maker():
    t = staffURL(token=secrets.token_urlsafe(32))
    db.session.add(t)
    db.session.commit()
    full_url = url_for("auth.register", token=t.token, _external=True)
    return full_url
    #return t.token

# @bp.route('/add_dummy')
# def add_dummy():
#     hashed = generate_password_hash("abc123")
#     dummy = Admin(
#         username="testuser",
#         password_hash=hashed,
#         first_name="adamtobe",
#         last_name="butisntyet"
#     )
#     db.session.add(dummy)
#     db.session.commit()
#     return "Dummy user added!"

# @bp.route('/show_dummy')
# def show_dummy():
#     user = Admin.query.filter_by(username="testuser").first()
#     return f"Found user: {user.first_name} {user.last_name}"

# CREATE TABLE validURL (
#         link VARCHAR(100) UNIQUE
#     );

# @bp.route('/logout_all')
# def logout_all():
#     resp = logout_user()
#     session.clear()
#     return "cleared"