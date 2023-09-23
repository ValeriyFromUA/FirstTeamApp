import os

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from flask_login import current_user, login_user, logout_user
from flask_uploads import UploadNotAllowed
from werkzeug.utils import secure_filename

from FTApp import bcrypt, db, login_manager
from FTApp.auth.forms import (CandidateLoginForm, CandidateRegistrationForm,
                              TeamLoginForm, TeamRegistrationForm)
from FTApp.auth.models import Candidate, Team
from FTApp.auth.security import auth_required
from FTApp.config import (CANDIDATE_PIC_DIR, CV_DIR, FILENAME_PREFIX,
                          TEAM_LOGO_DIR)
from FTApp.main.models import City, English, Experience, Specialisation

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    user = None
    user_type = session.get('user_type', None)

    if user_type == 'candidate':
        user = Candidate.query.get(int(user_id))
    elif user_type == 'team':
        user = Team.query.get(int(user_id))

    return user


@auth.route('/logout')
@auth_required
def logout():
    logout_user()
    flash('You have logged out now.', category='info')
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=('GET', 'POST'))
def login():
    candidate_login_form = CandidateLoginForm()
    team_login_form = TeamLoginForm()
    if request.method == 'POST':
        if candidate_login_form.validate_on_submit():
            email = candidate_login_form.email.data
            password = candidate_login_form.password.data

            candidate = Candidate.query.filter_by(email=email).first()
            if candidate and bcrypt.check_password_hash(candidate.password, password):
                login_user(candidate)
                session['user_type'] = 'candidate'
                current_user.user_type = 'candidate'
                flash('Ви увійшли як кандидат', 'success')
                return redirect(url_for('main_router.candidate_profile', candidate_id=candidate.id))
            else:
                flash('Wrong password or email', 'danger')

        if team_login_form.validate_on_submit():
            email = team_login_form.team_email.data
            password = team_login_form.team_password.data

            team = Team.query.filter_by(email=email).first()
            if team and bcrypt.check_password_hash(team.password, password):
                login_user(team)
                session['user_type'] = 'team'
                current_user.user_type = 'team'
                flash('Ви увійшли як команда', 'success')
                return redirect(url_for('main_router.team_profile', team_id=team.id))
            else:
                flash('Wrong password or email', 'danger')

    return render_template('login.html', title='Login', candidate_login_form=candidate_login_form,
                           team_login_form=team_login_form, current_user=current_user)


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    cities = [(city.id, city.name) for city in City.query.all()]
    english_levels = [(english.id, english.level) for english in English.query.all()]
    specialisations = [(specialisation.id, specialisation.name) for specialisation in
                       Specialisation.query.all()]
    experiences = [(experience.id, experience.name) for experience in Experience.query.all()]

    candidate_form = CandidateRegistrationForm()
    team_form = TeamRegistrationForm()
    if request.method == 'POST':
        if candidate_form.validate_on_submit():
            existing_user = Candidate.query.filter_by(email=candidate_form.email.data).first()
            if existing_user is None:
                selected_city_id = candidate_form.city.data
                selected_city = City.query.get(selected_city_id)

                selected_english_id = candidate_form.english.data
                selected_english = English.query.get(selected_english_id)

                selected_specialisation_id = candidate_form.specialisation.data
                selected_specialisation = Specialisation.query.get(
                    selected_specialisation_id)

                selected_experience_id = candidate_form.experience.data
                selected_experience = Experience.query.get(selected_experience_id)
                try:
                    profile_image = candidate_form.profile_image.data
                    cv = candidate_form.cv.data
                    if profile_image:
                        profile_image_filename = f'{FILENAME_PREFIX}_{secure_filename(profile_image.filename)}'
                        full_pic_path = os.path.join(CANDIDATE_PIC_DIR, profile_image_filename)
                        profile_image.save(full_pic_path)
                    else:
                        profile_image_filename = None

                    if cv:
                        cv_filename = f'{FILENAME_PREFIX}_{secure_filename(cv.filename)}'
                        full_cv_path = os.path.join(CV_DIR, cv_filename)
                        cv.save(full_cv_path)
                    else:
                        cv_filename = None

                    new_user = Candidate(
                        email=candidate_form.email.data,
                        password=bcrypt.generate_password_hash(candidate_form.password.data).decode('utf-8'),
                        first_name=candidate_form.first_name.data,
                        last_name=candidate_form.last_name.data,
                        telegram=candidate_form.telegram.data,
                        facebook=candidate_form.facebook.data,
                        instagram=candidate_form.instagram.data,
                        linkedin=candidate_form.linkedin.data,
                        github=candidate_form.github.data,
                        phone=candidate_form.phone.data,
                        about=candidate_form.about.data,
                        profile_image=profile_image_filename,
                        user_type='candidate',
                        city=selected_city,
                        cv=cv_filename,
                        english=selected_english,
                        specialisation=selected_specialisation,
                        experience=selected_experience,
                    )

                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user)
                    session['user_type'] = 'candidate'
                    current_user.user_type = 'candidate'

                    return redirect(url_for('main_router.candidate_profile', candidate_id=new_user.id))

                except UploadNotAllowed:
                    flash('Invalid file type. Upload images or PDFs only.', 'danger')

        elif team_form.validate_on_submit():
            existing_user = Team.query.filter_by(email=team_form.team_email.data).first()
            if existing_user is None:
                selected_city_id = team_form.team_city.data
                selected_city = City.query.get(selected_city_id)
                try:
                    profile_image = team_form.team_profile_image.data
                    if profile_image:
                        profile_image_filename = f'{FILENAME_PREFIX}_{secure_filename(profile_image.filename)}'
                        full_pic_path = os.path.join(TEAM_LOGO_DIR, profile_image_filename)
                        profile_image.save(full_pic_path)
                    else:
                        profile_image_filename = None

                    new_team = Team(
                        email=team_form.team_email.data,
                        password=bcrypt.generate_password_hash(team_form.team_password.data).decode('utf-8'),
                        company=team_form.team_company.data,
                        website=team_form.team_website.data,
                        telegram=team_form.team_telegram.data,
                        facebook=team_form.team_facebook.data,
                        instagram=team_form.team_instagram.data,
                        linkedin=team_form.team_linkedin.data,
                        phone=team_form.team_phone.data,
                        about=team_form.team_about.data,
                        user_type='team',
                        profile_image=profile_image_filename,
                        city=selected_city
                    )
                    db.session.add(new_team)
                    db.session.commit()
                    login_user(new_team)
                    session['user_type'] = 'team'
                    current_user.user_type = 'team'
                    return redirect(url_for('main_router.team_profile', team_id=new_team.id))
                except UploadNotAllowed:
                    flash('Invalid file type. Upload images or PDFs only.', 'danger')
    return render_template('registration.html', title='Registration', candidate_form=candidate_form,
                           team_form=team_form, cities=cities,
                           english_levels=english_levels,
                           specialisations=specialisations, experiences=experiences)
