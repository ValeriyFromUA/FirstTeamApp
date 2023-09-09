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
        self.name = level


class Experience(db.Model):
    __tablename__ = 'experience'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class BaseUser(db.Model):
    __tablename__ = 'base_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_staff = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    creation_date = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, email, password, is_staff=False, confirmed=False):
        self.email = email
        self.password = password
        self.is_staff = is_staff
        self.confirmed = confirmed


class ExtendedUser(BaseUser):
    __tablename__ = 'extended_user'
    telegram = db.Column(db.String(300), nullable=True)
    facebook = db.Column(db.String(300), nullable=True)
    instagram = db.Column(db.String(300), nullable=True)
    linkedin = db.Column(db.String(300), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    about = db.Column(db.String(3000), nullable=True)
    profile_image = db.Column(db.String(300))

    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    city = db.relationship('City', backref='extended_users')

    def __init__(self, email, password, is_staff=False, confirmed=False, city=None,
                 telegram=None, facebook=None, instagram=None, linkedin=None,
                 phone=None, about=None, profile_image=None):
        super().__init__(email=email, password=password, is_staff=is_staff, confirmed=confirmed)
        self.city = city
        self.telegram = telegram
        self.facebook = facebook
        self.instagram = instagram
        self.linkedin = linkedin
        self.phone = phone
        self.about = about
        self.profile_image = profile_image


class Administrator(BaseUser):
    __tablename__ = 'administrators'
    username = db.Column(db.String(128), nullable=False, unique=True)
    is_staff = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, email, password, username):
        super().__init__(email=email, password=password, is_staff=True, confirmed=True)
        self.username = username


class Candidate(ExtendedUser):
    __tablename__ = 'candidates'
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)

    cv = db.Column(db.String(300))

    english_id = db.Column(db.Integer, db.ForeignKey('english.id'))
    english = db.relationship('English', backref='candidate')

    specialisation_id = db.Column(db.Integer, db.ForeignKey('specialisation.id'))
    specialisation = db.relationship('Specialisation', backref='candidate')

    experience_id = db.Column(db.Integer, db.ForeignKey('experience.id'))
    experience = db.relationship('Experience', backref='candidate')

    def __init__(self, email, password, first_name, last_name, city=None, telegram=None,
                 facebook=None, instagram=None, linkedin=None, phone=None, about=None,
                 profile_image=None, cv=None, english=None, specialisation=None, experience=None):
        super().__init__(email=email, password=password, city=city, telegram=telegram,
                         facebook=facebook, instagram=instagram, linkedin=linkedin, phone=phone,
                         about=about, profile_image=profile_image)
        self.first_name = first_name
        self.last_name = last_name
        self.cv = cv
        self.english = english
        self.specialisation = specialisation
        self.experience = experience


class Team(ExtendedUser):
    company = db.Column(db.String(300), nullable=False)
    website = db.Column(db.String(300), nullable=False)

    def __init__(self, email, password, company, website, city=None, telegram=None,
                 facebook=None, instagram=None, linkedin=None, phone=None, about=None,
                 profile_image=None):
        super().__init__(email=email, password=password, city=city, telegram=telegram,
                         facebook=facebook, instagram=instagram, linkedin=linkedin, phone=phone,
                         about=about, profile_image=profile_image)
        self.company = company
        self.website = website


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

    description = db.Column(db.String(256))
    salary = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, title, specialisation, experience, english, description, salary):
        self.title = title
        self.specialisation = specialisation
        self.experience = experience
        self.english = english
        self.description = description
        self.salary = salary


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
