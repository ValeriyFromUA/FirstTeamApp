from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS, UploadNotAllowed
from werkzeug.utils import secure_filename

from FTApp import db
from FTApp.forms import CandidateRegistrationForm, TeamRegistrationForm
from FTApp.models import Candidate, Team, Opportunity, City, English, Experience, Specialisation

core = Blueprint('core', __name__)


@core.route('/')
@core.route('/main')
def main():
    return render_template('main.html', title='Main')


@core.route('/login', methods=('GET', 'POST'))
def login():
    return render_template('login.html', title='Main')


candidates_photos = UploadSet('CandidatesPhotos', IMAGES, default_dest='static/candidates_photos')
teams_photos = UploadSet('TeamsPhotos', IMAGES, default_dest='static/teams_photos')
cv = UploadSet('cv', IMAGES, default_dest='static/cv')


@core.route('/registration', methods=['GET', 'POST'])
def registration():
    cities = [(city.id, city.name) for city in City.query.all()]
    english_levels = [(english.id, english.level) for english in English.query.all()]
    specialisations = [(specialisation.id, specialisation.name) for specialisation in
                       Specialisation.query.all()]
    experiences = [(experience.id, experience.name) for experience in Experience.query.all()]

    current_datetime = datetime.now()
    filename_prefix = current_datetime.strftime('%Y%m%d%H%M%S')
    candidate_form = CandidateRegistrationForm()
    team_form = TeamRegistrationForm()
    if request.method == 'POST':
        print(candidate_form.validate_on_submit())
        print('************************************')
        print(candidate_form.submit.data)
        if candidate_form.validate_on_submit():
            print(1, candidate_form.email.data)
            existing_user = Candidate.query.filter_by(email=candidate_form.email.data).first()
            if existing_user is None:
                selected_city_id = candidate_form.city.data
                selected_city = City.query.get(selected_city_id)  # Знайти об'єкт міста за ID

                selected_english_id = candidate_form.english.data
                selected_english = English.query.get(selected_english_id)  # Знайти об'єкт рівня англійської мови за ID

                selected_specialisation_id = candidate_form.specialisation.data
                selected_specialisation = Specialisation.query.get(
                    selected_specialisation_id)  # Знайти об'єкт спеціалізації за ID

                selected_experience_id = candidate_form.experience.data
                selected_experience = Experience.query.get(selected_experience_id)  # Знайти об'єкт досвіду за ID
                print(2, candidate_form.email.data)
                try:
                    profile_image = candidate_form.profile_image.data
                    cv = candidate_form.cv.data
                    if profile_image:
                        profile_image_filename = f'{filename_prefix}_{secure_filename(profile_image.filename)}'
                        profile_image.save(profile_image_filename)
                    else:
                        profile_image_filename = None

                    if cv:
                        cv_filename = f'{filename_prefix}_{secure_filename(cv.filename)}'
                        cv.save(cv_filename)
                    else:
                        cv_filename = None

                    new_user = Candidate(
                        email=candidate_form.email.data,
                        password=candidate_form.password.data,
                        first_name=candidate_form.first_name.data,
                        last_name=candidate_form.last_name.data,
                        telegram=candidate_form.telegram.data,
                        facebook=candidate_form.facebook.data,
                        instagram=candidate_form.instagram.data,
                        linkedin=candidate_form.linkedin.data,
                        phone=candidate_form.phone.data,
                        about=candidate_form.about.data,
                        profile_image=profile_image_filename,
                        city=selected_city,  # Зберегти об'єкт міста, а не ID
                        cv=cv_filename,
                        english=selected_english,  # Зберегти об'єкт рівня англійської мови, а не ID
                        specialisation=selected_specialisation,  # Зберегти об'єкт спеціалізації, а не ID
                        experience=selected_experience,  # Зберегти об'єкт досвіду, а не ID
                    )

                    db.session.add(new_user)
                    db.session.commit()

                    return redirect(url_for('core.main'))  # Перенаправте на сторінку логіну після реєстрації

                except UploadNotAllowed:
                    print(UploadNotAllowed)
                    flash('Invalid file type. Upload images or PDFs only.', 'danger')

    #     elif team_form.validate_on_submit() and team_form.submit.data:
    #         existing_user = Team.query.filter_by(email=team_form.email.data).first()
    #         if existing_user is None:
    #             # Створення нового користувача з даними з форми
    #             new_user = Team(
    #                 email=team_form.email.data,
    #                 password=team_form.password.data,
    #                 company=team_form.company.data,
    #                 website=team_form.website.data,
    #                 telegram=team_form.telegram.data,
    #                 facebook=team_form.facebook.data,
    #                 instagram=team_form.instagram.data,
    #                 linkedin=team_form.linkedin.data,
    #                 phone=team_form.phone.data,
    #                 about=team_form.about.data,
    #                 profile_image=team_form.profile_image.data,
    #                 city=team_form.city.data,
    #                 # Додайте інші поля з форми сюди
    #             )
    # # Обробка реєстрації команди
    # # ...
    return render_template('registration.html', title='Registration', candidate_form=candidate_form, cities=cities,
                           english_levels=english_levels,
                           specialisations=specialisations, experiences=experiences)


@core.route('/candidates/<int:candidate_id>', methods=('GET', 'POST'))
def candidate_profile(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    # is_owner = current_user.is_authenticated and current_user.id == candidate.id if candidate else False
    if candidate:
        return render_template('candidate_profile.html', title='Profile', candidate=candidate)
    return render_template('404.html', title='Not found')


@core.route('/teams/<int:team_id>', methods=('GET', 'POST'))
def team_profile(team_id):
    team = Team.query.get(team_id)
    # is_owner = current_user.is_authenticated and current_user.id == team.id if team else False
    if team:
        return render_template('team_profile.html', title=team.company, team=team)
    return render_template('404.html', title='Not found')


@core.route('/opportunities')
@core.route('/opportunities/<int:opp_id>')
def opportunities(opp_id=None):
    if opp_id:
        opportunity = Opportunity.query.get(opp_id)
        if opportunity:
            return render_template('opportunity.html', title=opportunity.title, opportunity=opportunity)
        return render_template('404.html', title='Not found')
    opportunities_list = Opportunity.query.all()
    return render_template('opportunities.html', title='Main', opportunities=opportunities_list)
