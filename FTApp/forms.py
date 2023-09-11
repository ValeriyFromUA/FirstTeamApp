from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

from FTApp.models import Specialisation, English, City, Experience


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
    phone = StringField('Phone')
    about = TextAreaField('About')
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


class TeamRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    company = StringField('Company', validators=[DataRequired()])
    website = StringField('Website', validators=[DataRequired()])
    telegram = StringField('Telegram')
    facebook = StringField('Facebook')
    instagram = StringField('Instagram')
    linkedin = StringField('LinkedIn')
    phone = StringField('Phone')
    about = TextAreaField('About')
    profile_image = FileField('Profile Image URL')
    city = SelectField('City', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Register as Team')

    def __init__(self, *args, **kwargs):
        super(TeamRegistrationForm, self).__init__(*args, **kwargs)

        self.city.choices = [(city.id, city.name) for city in City.query.all()]
