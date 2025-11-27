from flask import Blueprint, Flask, request, render_template
from .models import Patient, validURL
from . import db


bp = Blueprint('response', __name__)

@bp.route('/quiz/<token>', methods=['GET', 'POST'])
def quiz(token):
    key = validURL.query.filter_by(token=token).first()

    if not key:
        return "Invalid link", 404
    
    if key.used:
        return "This link has already been used.", 403
    
    if request.method == 'GET':
        return render_template("reply.html", token=token)

    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    mail = request.form.get("email")
    ring = request.form.get("phone")
    #answers = request.form.getlist("answer")
    answers = [request.form.get(f"ans{i}") for i in range(1, 11)]
    #print(answers[0])

    dummy = Patient(
        first_name=firstName,
        last_name=lastName,
        pref1 = answers[0],
        pref2 = answers[1],
        pref3 = answers[2],
        pref4 = answers[3],
        pref5 = answers[4],
        pref6 = answers[5],
        pref7 = answers[6],
        pref8 = answers[7],
        pref9 = answers[8],
        pref10 = answers[9],
        email = mail,
        phone = ring,
        notes = None
    )
    db.session.add(dummy)
    key.used = True
    db.session.commit()

    return render_template("thanks.html") #tbd boi