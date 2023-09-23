from flask_wtf import FlaskForm
from wtforms import (BooleanField, FileField, PasswordField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from FTApp.auth.models import Candidate
from FTApp.main.models import City, English, Experience, Specialisation


class CandidateRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    telegram = StringField('Telegram')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    linkedin = StringField('LinkedIn')
    github = StringField('GitHub')
    phone = StringField('Phone')
    about = TextAreaField('About')
    show_me = BooleanField('Show me')
    profile_image = FileField('Profile Image URL')
    cv = FileField('CV URL')
    city = SelectField('City', validators=[DataRequired()], coerce=int)
    english = SelectField('English Level', validators=[DataRequired()], coerce=int)
    specialisation = SelectField('Specialisation', validators=[DataRequired()], coerce=int)
    experience = SelectField('Experience', validators=[DataRequired()], coerce=int)

    submit = SubmitField('Register as Candidate')

    def __init__(self, *args, **kwargs):
        super(CandidateRegistrationForm, self).__init__(*args, **kwargs)

        self.city.choices = [(city.id, city.name) for city in City.query.all()]
        self.english.choices = [(english.id, english.level) for english in English.query.all()]
        self.specialisation.choices = [(specialisation.id, specialisation.name) for specialisation in
                                       Specialisation.query.all()]
        self.experience.choices = [(experience.id, experience.name) for experience in Experience.query.all()]

    def validate_email(self, email):
        user = Candidate.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email exists, please pick another one')

    def validate_phone(self, phone):
        user = Candidate.query.filter_by(phone=phone.data).first()
        if user is not None:
            raise ValidationError('Phone exists, please pick another one')


class TeamRegistrationForm(FlaskForm):
    team_email = StringField('Email', validators=[DataRequired(), Email()])
    team_password = PasswordField('Password', validators=[DataRequired()])
    team_confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('team_password')])
    team_company = StringField('Company', validators=[DataRequired()])
    team_website = StringField('Website', validators=[DataRequired()])
    team_telegram = StringField('Telegram')
    team_facebook = StringField('Facebook')
    team_instagram = StringField('Instagram')
    team_linkedin = StringField('LinkedIn')
    team_phone = StringField('Phone')
    team_about = TextAreaField('About')
    team_profile_image = FileField('Profile Image URL')
    team_city = SelectField('City', validators=[DataRequired()], coerce=int)
    team_submit = SubmitField('Register as Team')

    def __init__(self, *args, **kwargs):
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)

        self.team_city.choices = [(city.id, city.name) for city in City.query.all()]

    def validate_email(self, team_email):
        user = Candidate.query.filter_by(email=team_email.data).first()
        if user is not None:
            raise ValidationError('Email exists, please pick another one')

    def validate_phone(self, team_phone):
        user = Candidate.query.filter_by(phone=team_phone.data).first()
        if user is not None:
            raise ValidationError('Phone exists, please pick another one')

    def validate_company(self, team_company):
        user = Candidate.query.filter_by(phone=team_company.data).first()
        if user is not None:
            raise ValidationError('Company exists, please pick another one')


class CandidateLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enter as Candidate')


class TeamLoginForm(FlaskForm):
    team_email = StringField('Email', validators=[DataRequired(), Email()])
    team_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enter as Team')
