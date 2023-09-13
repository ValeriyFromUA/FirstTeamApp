import os
from datetime import datetime
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS, UploadNotAllowed
from werkzeug.utils import secure_filename

from FTApp import db, bcrypt, login_manager
from FTApp.constants import CANDIDATE_PIC_DIR, CV_DIR, TEAM_LOGO_DIR, FILENAME_PREFIX
from FTApp.forms import CandidateRegistrationForm, TeamRegistrationForm, CandidateEditForm, CandidateLoginForm, \
    TeamLoginForm, OpportunityForm
from FTApp.models import Candidate, Team, Opportunity, City, English, Experience, Specialisation, Administrator
from FTApp.security import team_required

core = Blueprint('core', __name__)


@login_manager.user_loader
def load_user(user_id):
    user = None
    user_type = session.get('user_type', None)  # Отримуємо user_type з сесії

    if user_type == 'candidate':
        user = Candidate.query.get(int(user_id))
    elif user_type == 'team':
        user = Team.query.get(int(user_id))
    elif user_type == 'admin':
        user = Administrator.query.get(int(user_id))

    return user


# @login_manager.user_loader
# def load_admin_user(admin_id):
#     return Admin.query.get(int(admin_id))

@core.route('/')
@core.route('/main')
def main():
    return render_template('main.html', title='Main')


@core.route('/logout')
def logout():
    logout_user()
    flash('You have logged out now.', category='info')
    return redirect(url_for('core.login'))


@core.route('/login', methods=('GET', 'POST'))
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
                return redirect(url_for('core.candidate_profile', candidate_id=candidate.id))
            else:
                flash('Невірна електронна пошта або пароль', 'danger')

        if team_login_form.validate_on_submit():
            # Обробіть вхід для команди, аналогічно кандидату
            email = team_login_form.team_email.data
            password = team_login_form.team_password.data

            team = Team.query.filter_by(email=email).first()
            if team and bcrypt.check_password_hash(team.password, password):
                login_user(team)
                session['user_type'] = 'team'
                current_user.user_type = 'team'
                flash('Ви увійшли як команда', 'success')
                return redirect(url_for('core.team_profile', team_id=team.id))
            else:
                flash('Невірна електронна пошта або пароль', 'danger')

    return render_template('login.html', title='Login', candidate_login_form=candidate_login_form,
                           team_login_form=team_login_form, current_user=current_user)


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
                        show_me=candidate_form.show_me.data,
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

                    return redirect(url_for('core.candidate_profile', candidate_id=new_user.id))

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
                    return redirect(url_for('core.team_profile', team_id=new_team.id))
                except UploadNotAllowed:
                    flash('Invalid file type. Upload images or PDFs only.', 'danger')
    return render_template('registration.html', title='Registration', candidate_form=candidate_form,
                           team_form=team_form, cities=cities,
                           english_levels=english_levels,
                           specialisations=specialisations, experiences=experiences)


@core.route('/candidates')
@team_required
def candidates():
    all_candidates = Candidate.query.filter_by(show_me=True).all()
    return render_template('candidates.html', title='Всі кандидати', candidates=all_candidates)


@core.route('/candidates/<int:candidate_id>', methods=('GET', 'POST'))
def candidate_profile(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return render_template('404.html', title='Not found')

    # if current_user.is_authenticated and current_user.id == candidate.id:
    candidate_form = CandidateEditForm(obj=candidate)
    if request.method == 'POST':
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
        candidate.first_name = request.form['first_name']
        candidate.last_name = request.form['last_name']
        candidate.telegram = request.form['telegram']
        candidate.facebook = request.form['facebook']
        candidate.instagram = request.form['instagram']
        candidate.linkedin = request.form['linkedin']
        candidate.github = request.form['github']
        candidate.about = request.form['about']
        candidate.profile_image = (
            profile_image_filename if profile_image else candidate.profile_image)
        candidate.cv = cv_filename if cv else candidate.cv
        db.session.commit()
        flash('Профіль оновлено', 'success')
        return redirect(url_for('core.candidate_profile', candidate_id=candidate.id))
    return render_template('candidate_profile.html', title='Profile', candidate=candidate,
                           candidate_form=candidate_form)
    # else:
    #     return render_template('403.html', title='Access Denied')


@core.route('/teams/<int:team_id>', methods=('GET', 'POST'))
def team_profile(team_id):
    team = Team.query.get(team_id)
    # is_owner = current_user.is_authenticated and current_user.id == team.id if team else False
    if team:
        return render_template('team_profile.html', title=team.company, team=team)
    return render_template('404.html', title='Not found')


@core.route('/opportunities', methods=('GET', 'POST'))
def opportunities():
    cities = [(city.id, city.name) for city in City.query.all()]
    english_levels = [(english.id, english.level) for english in English.query.all()]
    specialisations = [(specialisation.id, specialisation.name) for specialisation in
                       Specialisation.query.all()]
    experiences = [(experience.id, experience.name) for experience in Experience.query.all()]
    opportunity_form = OpportunityForm()
    all_opportunities = Opportunity.query.all()

    city_filter = request.args.get('city')
    specialisation_filter = request.args.get('specialisation')
    english_filter = request.args.get('english')

    filtered_opportunities = all_opportunities

    if city_filter:
        filtered_opportunities = [opp for opp in filtered_opportunities if opp.city.name == city_filter]
    if specialisation_filter:
        filtered_opportunities = [opp for opp in filtered_opportunities if
                                  opp.specialisation.name == specialisation_filter]
    if english_filter:
        filtered_opportunities = [opp for opp in filtered_opportunities if opp.english.level == english_filter]

    filtered_opportunities = sorted(filtered_opportunities, key=lambda opp: opp.id, reverse=True)

    if request.method == 'POST':
        if opportunity_form.validate_on_submit():
            selected_city_id = opportunity_form.op_city.data
            selected_city = City.query.get(selected_city_id)

            selected_english_id = opportunity_form.op_english.data
            selected_english = English.query.get(selected_english_id)

            selected_specialisation_id = opportunity_form.op_specialisation.data
            selected_specialisation = Specialisation.query.get(
                selected_specialisation_id)

            selected_experience_id = opportunity_form.op_experience.data
            selected_experience = Experience.query.get(selected_experience_id)

            new_opportunity = Opportunity(
                title=opportunity_form.op_title.data,
                english=selected_english,
                specialisation=selected_specialisation,
                experience=selected_experience,
                city=selected_city,
                description=opportunity_form.op_description.data,
                salary=opportunity_form.op_salary.data,
                team=Team.query.get(current_user.id)

            )
            db.session.add(new_opportunity)
            db.session.commit()

            return redirect(url_for('core.opportunity', opp_id=new_opportunity.id))

    return render_template('opportunities.html', title='Вакансії', opportunities=filtered_opportunities,
                           opportunity_form=opportunity_form, cities=cities,
                           english_levels=english_levels,
                           specialisations=specialisations, experiences=experiences)


@core.route('/opportunities/<int:opp_id>')
def opportunity(opp_id=None):
    selected_opportunity = Opportunity.query.get(opp_id)
    return render_template('opportunity.html', title=selected_opportunity.title, opportunity=selected_opportunity)
