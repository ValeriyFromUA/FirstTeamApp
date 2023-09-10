from flask import Blueprint, render_template
from flask_login import current_user

from FTApp.models import Candidate, Team, Opportunity

core = Blueprint('core', __name__)


@core.route('/')
@core.route('/main')
def main():
    return render_template('main.html', title='Main')


@core.route('/login')
def login():
    return render_template('login.html', title='Main')


@core.route('/registration', methods=('GET', 'POST'))
def registration():
    return render_template('registration.html', title='Registration')


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
