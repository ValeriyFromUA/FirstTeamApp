import os

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename

from FTApp import db
from FTApp.auth.models import Candidate, Team
from FTApp.auth.security import (auth_required, candidate_required,
                                 team_required)
from FTApp.config import CANDIDATE_PIC_DIR, CV_DIR, FILENAME_PREFIX
from FTApp.main.forms import CandidateEditForm, OpportunityForm
from FTApp.main.models import (City, English, Experience, Opportunity,
                               Specialisation)

main_router = Blueprint('main_router', __name__)


@main_router.route('/')
@main_router.route('/main')
def main():
    return render_template('main.html', title='Main')


@main_router.route('/candidates')
@team_required
def candidates():
    team_opportunities = Opportunity.query.filter_by(team_id=current_user.id).all()

    matching_candidates = Candidate.query.filter(
        Candidate.specialisation_id.in_([opp.specialisation_id for opp in team_opportunities]),
        Candidate.city_id.in_([opp.city_id for opp in team_opportunities])
    ).all()
    return render_template('candidates.html', title='Всі кандидати', candidates=matching_candidates)


@main_router.route('/candidates/<int:candidate_id>', methods=('GET', 'POST'))
@auth_required
def candidate_profile(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return render_template('404.html', title='Not found')
    candidate_form = CandidateEditForm(obj=candidate)
    if current_user.user_type == 'candidate' and current_user.id == candidate_id:

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
            return redirect(url_for('main_router.candidate_profile', candidate_id=candidate.id))
    return render_template('candidate_profile.html', title='Profile', candidate=candidate,
                           candidate_form=candidate_form)


@main_router.route('/teams/<int:team_id>', methods=('GET', 'POST'))
@auth_required
def team_profile(team_id):
    my_opportunities = Opportunity.query.filter_by(team_id=team_id).order_by(desc(Opportunity.id)).all()
    if current_user.user_type == 'candidate' or current_user.id != team_id:
        my_opportunities = [opportunity for opportunity in my_opportunities if opportunity.visible]

    cities = [(city.id, city.name) for city in City.query.all()]
    english_levels = [(english.id, english.level) for english in English.query.all()]
    specialisations = [(specialisation.id, specialisation.name) for specialisation in
                       Specialisation.query.all()]
    experiences = [(experience.id, experience.name) for experience in Experience.query.all()]
    opportunity_form = OpportunityForm()
    team = Team.query.get(team_id)
    if current_user.user_type == 'team' and current_user.id == team.id:
        if request.method == 'POST':
            if opportunity_form.validate_on_submit():
                selected_city_id = opportunity_form.city.data
                selected_city = City.query.get(selected_city_id)

                selected_english_id = opportunity_form.english.data
                selected_english = English.query.get(selected_english_id)

                selected_specialisation_id = opportunity_form.specialisation.data
                selected_specialisation = Specialisation.query.get(
                    selected_specialisation_id)

                selected_experience_id = opportunity_form.experience.data
                selected_experience = Experience.query.get(selected_experience_id)

                new_opportunity = Opportunity(
                    title=opportunity_form.title.data,
                    english=selected_english,
                    specialisation=selected_specialisation,
                    experience=selected_experience,
                    city=selected_city,
                    description=opportunity_form.description.data,
                    salary=opportunity_form.salary.data,
                    team=Team.query.get(current_user.id),
                    visible=True,

                )
                db.session.add(new_opportunity)
                db.session.commit()
                return redirect(url_for('main_router.opportunity', opp_id=new_opportunity.id))
    if team:
        return render_template('team_profile.html', title=team.company, team=team, opportunity_form=opportunity_form,
                               opportunities=my_opportunities, cities=cities,
                               english_levels=english_levels,
                               specialisations=specialisations, experiences=experiences)
    return render_template('404.html', title='Not found')


@main_router.route('/opportunities', methods=('GET', 'POST'))
@candidate_required
def opportunities():
    all_opportunities = Opportunity.query.filter(Opportunity.specialisation == current_user.specialisation,
                                                 Opportunity.visible == True)
    all_opportunities = all_opportunities.order_by(
        Opportunity.city != current_user.city,
        Opportunity.creation_date.desc()).all()

    return render_template('opportunities.html', title='Вакансії', opportunities=all_opportunities)


@main_router.route('/opportunities/<int:opp_id>', methods=['GET', 'POST'])
@auth_required
def opportunity(opp_id):
    selected_opportunity = Opportunity.query.get(opp_id)
    candidates_for_opportunity = Candidate.query.filter(
        (Candidate.city == selected_opportunity.city) &
        (Candidate.specialisation.has(name=selected_opportunity.specialisation.name)) &
        (Candidate.english_id >= selected_opportunity.english_id)
    ).all()
    if current_user.is_authenticated and current_user.id == selected_opportunity.team.id:
        if request.method == 'POST':

            if selected_opportunity:
                selected_opportunity.visible = False
                db.session.commit()
                return redirect(url_for('main_router.team_profile', team_id=selected_opportunity.team.id))
    return render_template('opportunity.html', title=selected_opportunity.title, opportunity=selected_opportunity,
                           candidates=candidates_for_opportunity)
