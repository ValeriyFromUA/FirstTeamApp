from flask_login import UserMixin

from FTApp import db


class Candidate(db.Model, UserMixin):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, default=db.func.now())
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    telegram = db.Column(db.String(300), nullable=True)
    facebook = db.Column(db.String(300), nullable=True)
    instagram = db.Column(db.String(300), nullable=True)
    linkedin = db.Column(db.String(300), nullable=True)
    github = db.Column(db.String(300), nullable=True)
    user_type = db.Column(db.String(300), nullable=True, default='candidate')
    show_me = db.Column(db.Boolean, nullable=False, default=False)
    phone = db.Column(db.String(20), nullable=True)
    about = db.Column(db.String(5000), nullable=True)
    profile_image = db.Column(db.String(300))

    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship('City', backref='candidates')

    cv = db.Column(db.String(300))

    english_id = db.Column(db.Integer, db.ForeignKey('english.id'))
    english = db.relationship('English', backref='candidates')

    specialisation_id = db.Column(db.Integer, db.ForeignKey('specialisations.id'))
    specialisation = db.relationship('Specialisation', backref='candidates')

    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'))
    experience = db.relationship('Experience', backref='candidates')

    def __init__(self, email, password, first_name, last_name, user_type, city=None, github=None, telegram=None,
                 facebook=None, instagram=None, linkedin=None, phone=None, about=None,
                 profile_image=None, cv=None, english=None, specialisation=None, experience=None):
        self.email = email
        self.password = password
        self.is_staff = False
        self.confirmed = False
        self.first_name = first_name
        self.last_name = last_name
        self.telegram = telegram
        self.facebook = facebook
        self.instagram = instagram
        self.linkedin = linkedin
        self.github = github
        self.phone = phone
        self.about = about
        self.profile_image = profile_image
        self.city = city
        self.cv = cv
        self.english = english
        self.specialisation = specialisation
        self.experience = experience
        self.user_type = user_type


class Team(db.Model, UserMixin):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, default=db.func.now())
    company = db.Column(db.String(300), nullable=False)
    website = db.Column(db.String(300), nullable=True)
    telegram = db.Column(db.String(300), nullable=True)
    facebook = db.Column(db.String(300), nullable=True)
    instagram = db.Column(db.String(300), nullable=True)
    linkedin = db.Column(db.String(300), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    about = db.Column(db.String(5000), nullable=True)
    user_type = db.Column(db.String(5000), nullable=True, default='team')
    profile_image = db.Column(db.String(300))

    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship('City', backref='extended_users')

    def __init__(self, email, password, company, user_type, website, city=None, telegram=None,
                 facebook=None, instagram=None, linkedin=None, phone=None, about=None,
                 profile_image=None):
        self.email = email
        self.password = password
        self.is_staff = False
        self.confirmed = False
        self.company = company
        self.website = website
        self.telegram = telegram
        self.facebook = facebook
        self.instagram = instagram
        self.linkedin = linkedin
        self.phone = phone
        self.about = about
        self.profile_image = profile_image
        self.city = city
        self.user_type = user_type
