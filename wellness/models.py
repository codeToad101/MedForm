from . import db
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    first_name = db.Column(db.String(50));
    last_name = db.Column(db.String(50));

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50));
    last_name = db.Column(db.String(50));
    pref1 = db.Column(db.String(1))
    pref2 = db.Column(db.String(1))
    pref3 = db.Column(db.String(1))
    pref4 = db.Column(db.String(1))
    pref5 = db.Column(db.String(1))
    pref6 = db.Column(db.String(1))
    pref7 = db.Column(db.String(1))
    pref8 = db.Column(db.String(1))
    pref9 = db.Column(db.String(1))
    pref10 = db.Column(db.String(1))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(25))
    notes = db.Column(db.String(1000))


class validURL(db.Model):
    __tablename__ = "validURL"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)

class staffURL(db.Model):
    __tablename__ = "staffURL"
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    used = db.Column(db.Boolean, default=False)