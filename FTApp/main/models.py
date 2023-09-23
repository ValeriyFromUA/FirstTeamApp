from FTApp import db


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
    visible = db.Column(db.Boolean, nullable=False, default=True)
    description = db.Column(db.String(5000))
    salary = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, specialisation, experience, english, description, salary, city, team, visible):
        self.title = title
        self.specialisation = specialisation
        self.experience = experience
        self.english = english
        self.description = description
        self.salary = salary
        self.city = city
        self.team = team
        self.visible = visible
