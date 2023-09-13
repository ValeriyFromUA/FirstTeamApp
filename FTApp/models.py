from flask_login import UserMixin
from FTApp import db, login_manager


class Specialisation(db.Model):
    __tablename__ = 'specialisations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name


class English(db.Model):
    __tablename__ = 'english'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(128), nullable=False)

    def __init__(self, level):
        self.level = level


class Experience(db.Model):
    __tablename__ = 'experience'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Administrator(db.Model, UserMixin):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, default=db.func.now())
    username = db.Column(db.String(128), nullable=False, unique=True)
    user_type = db.Column(db.String(300), nullable=True, default='admin')

    def __init__(self, email, password, username, user_type):
        self.email = email
        self.password = password
        self.is_staff = True
        self.confirmed = True
        self.username = username
        self.user_type = user_type


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

    # responses = db.relationship('Response', backref='candidate',
    #                             primaryjoin='Candidate.id == Response.candidate_id')

    def __init__(self, email, password, first_name, last_name, user_type, city=None, github=None, telegram=None,
                 facebook=None, instagram=None, linkedin=None, phone=None, about=None,
                 profile_image=None, cv=None, english=None, specialisation=None, experience=None, show_me=False):
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
        self.show_me = show_me


class Team(db.Model, UserMixin):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, default=db.func.now())
    company = db.Column(db.String(300), nullable=False)
    website = db.Column(db.String(300), nullable=False)
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


class Opportunity(db.Model):
    __tablename__ = 'opportunities'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)

    specialisation_id = db.Column(db.Integer, db.ForeignKey('specialisations.id'))
    specialisation = db.relationship('Specialisation', backref='opportunities')

    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'))
    experience = db.relationship('Experience', backref='opportunities')

    english_id = db.Column(db.Integer, db.ForeignKey('english.id'))
    english = db.relationship('English', backref='opportunities')

    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship('City', backref='opportunities')

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', backref='opportunities')

    description = db.Column(db.String(5000))
    salary = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, specialisation, experience, english, description, salary, city, team):
        self.title = title
        self.specialisation = specialisation
        self.experience = experience
        self.english = english
        self.description = description
        self.salary = salary
        self.city = city
        self.team = team


class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)

    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'))
    opportunity = db.relationship('Opportunity', backref='responses')

    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    candidate = db.relationship('Candidate', backref='responses')

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', backref='responses')

    creation_date = db.Column(db.DateTime, default=db.func.now())
    user_read = db.Column(db.Boolean, nullable=False, default=False)
    team_read = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, opportunity, candidate, team, user_read=False, team_read=False):
        self.opportunity = opportunity
        self.candidate = candidate
        self.team = team
        self.user_read = user_read
        self.team_read = team_read


class EmailConfirmation(db.Model):
    __tablename__ = 'email_confirmations'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    token = db.Column(db.String(200), unique=True, nullable=False)
    creation_date = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, token, user_id=None, team_id=None):
        self.user_id = user_id
        self.team_id = team_id
        self.token = token


class Complaint(db.Model):
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'))
    opportunity = db.relationship('Opportunity', backref='complaints')
    creation_date = db.Column(db.DateTime, default=db.func.now())
    description = db.Column(db.String(5000))
