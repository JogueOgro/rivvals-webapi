from flask import request, jsonify, Blueprint
from database import Session
from model.models import *
import json

team_blueprint = Blueprint('team', __name__)

@team_blueprint.route('/teams', methods=['GET'])
def get_teams():
    session = Session()
    teams = session.query(Team).all()
    teams_dicts = [team.to_dict() for team in teams]
    return teams_dicts

@team_blueprint.route('/team/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id):
    session = Session()
    team = session.query(Team).filter_by(idteam=team_id).first()
    session.close()
    if not team:
      return jsonify({'message': 'Time não encontrado'}), 404
    return team.to_dict()

@team_blueprint.route('/team', methods=['POST'])
def create_team():

    data = request.json

    new_team = Team(
        name=data.get('name'),
        logo=data.get('logo'),
        wins=data.get('wins'),
        number=data.get('number'),
        group=data.get('group'),
    )

    session = Session()
    session.add(new_team)
    session.commit()
    return new_team.to_dict()

@team_blueprint.route('/team/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    session = Session()
    team = session.query(Team).filter_by(idteam=team_id).first()
    if not team:
        return jsonify({'message': 'Time não encontrado'}), 404

    data = request.json
    if team:
        team.name = data.get('name'),
        team.logo = data.get('logo'),
        team.wins = data.get('wins'),
        team.number = data.get('number'),
        team.group = data.get('group'),
        session.commit()
    return team.to_dict()

@team_blueprint.route('/team/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    session = Session()
    team = session.query(Team).filter_by(idteam=team_id).first()
    if not team:
      return jsonify({'message': 'Time não encontrado'}), 404
    else:
        session.delete(team)
        session.commit()
    return team.to_dict()



