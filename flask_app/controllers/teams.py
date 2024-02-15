from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.team import Team
from flask import flash


@app.route('/teams')
def welcome():
    if 'user_id' not in session:
        return redirect('/')

    user = User.get_by_id(session['user_id'])
    teams = Team.getAllTeams()
    print("user info----------------------->", user)
    return render_template('all_teams.html', user=user, teams=teams)


@app.route('/create_team')
def createTeam():
    user = User.get_by_id(session['user_id'])
    return render_template('create_team.html', user=user)


@app.route('/new_team', methods=["POST"])
def addTeam():
    print("Team INFO: ", request.form)
    if not Team.validateTeam(request.form):
        return redirect('/create_team')
    id = Team.addTeam(request.form)
    return redirect('/teams')


@app.route('/delete_team/<int:id>/delete')
def deleteTeam(id):
    Team.delete(id)
    return redirect('/teams')


@app.route('/teams/<int:id>/edit')
def editTeam(id):
    team = Team.getTeam(id)
    user = User.get_by_id(team.user_id)

    return render_template('edit_team.html', team=team, user=user)


@app.route('/teams/update', methods=["POST"])
def updateTeams():
    print(request.form)
    if not Team.validateTeam(request.form):
        print("Team invalid")
        return redirect(f'/teams/{request.form["id"]}/edit')
    Team.update(request.form)
    return redirect('/teams')


@app.route('/teams/<int:id>/view')
def viewTeam(id):
    team = Team.getTeam(id)
    user = User.get_by_id(session["user_id"])

    return render_template('view_team.html', team=team, user=user)
