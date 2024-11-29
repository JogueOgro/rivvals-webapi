from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import team_blueprint
from database import Session
from model.models import *
import json

@team_blueprint.route('/teams', methods=['GET'])
@jwt_required()
def get_teams():
    session = Session()
    teams = session.query(Team).all()
    teams_dicts = [team.to_dict() for team in teams]
    return teams_dicts

@team_blueprint.route('/team/<int:team_id>', methods=['GET'])
@jwt_required()
def get_team_by_id(team_id):
    session = Session()
    team = session.query(Team).filter_by(idteam=team_id).first()
    session.close()
    if not team:
      return jsonify({'message': 'Time não encontrado'}), 404
    return team.to_dict()

@team_blueprint.route('/team', methods=['POST'])
@jwt_required()
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
@jwt_required()
def update_team(team_id):
    session = Session()
    team = session.query(Team).filter_by(idteam=team_id).first()
    if not team:
        return jsonify({'message': 'Time não encontrado'}), 404

    data = request.json
    new_team = Team(
        name=data.get('name'),
        logo=data.get('logo'),
        wins=data.get('wins'),
        number=data.get('number'),
        group=data.get('group'),
    )
    return team.to_dict()

@team_blueprint.route('/teams', methods=['PUT'])
@jwt_required()
def update_all_teams():
    try:
        session = Session()

        teams_data = request.json
        for team_data in teams_data:
            team_id = team_data.get('id')
            if not team_id:
                return jsonify({'error': 'Cada time precisa ter um "id".'}), 400

            update_data = {
                'name': team_data.get('name'),
                'logo': team_data.get('logo'),
                'wins': team_data.get('wins'),
                'number': team_data.get('number'),
                'group': team_data.get('group'),
            }
            filtered_data = {key: value for key, value in update_data.items() if value is not None}

            if filtered_data:
                session.query(Team).filter_by(idteam=team_id).update(filtered_data, synchronize_session=False)

        session.commit()

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()

    return jsonify({'message': 'Teams atualizados!'}), 200



