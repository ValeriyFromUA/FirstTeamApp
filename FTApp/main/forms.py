from flask_wtf import FlaskForm
from wtforms import (BooleanField, FileField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired

from FTApp.main.models import City, English, Experience, Specialisation


class CandidateEditForm(FlaskForm):
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

    submit = SubmitField('Edit Candidate')


class OpportunityForm(FlaskForm):
    title = StringField('Title')
    description = StringField('Title')
    salary = StringField('Title')
    city = SelectField('City', validators=[DataRequired()], coerce=int)
    english = SelectField('English Level', validators=[DataRequired()], coerce=int)
    specialisation = SelectField('Specialisation', validators=[DataRequired()], coerce=int)
    experience = SelectField('Experience', validators=[DataRequired()], coerce=int)

    submit = SubmitField('Register as Candidate')

    def __init__(self, *args, **kwargs):
        super(OpportunityForm, self).__init__(*args, **kwargs)

        self.city.choices = [(city.id, city.name) for city in City.query.all()]
        self.english.choices = [(english.id, english.level) for english in English.query.all()]
        self.specialisation.choices = [(specialisation.id, specialisation.name) for specialisation in
                                       Specialisation.query.all()]
        self.experience.choices = [(experience.id, experience.name) for experience in Experience.query.all()]
