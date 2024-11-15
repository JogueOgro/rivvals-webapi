from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import match_blueprint
from database import Session
from datetime import datetime
from model.models import *
import json

@match_blueprint.route('/matches', methods=['GET'])
@jwt_required()
def get_matches():
    session = Session()
    matches = session.query(Match).all()
    matches_dicts = [match.to_dict() for match in matches]
    return matches_dicts

@match_blueprint.route('/match/<int:match_id>', methods=['GET'])
@jwt_required()
def get_match_by_id(match_id):
    session = Session()
    match = session.query(match).filter_by(idmatch=match_id).first()
    session.close()
    if not match:
      return jsonify({'message': 'Time não encontrado'}), 404
    return match.to_dict()

@match_blueprint.route('/match', methods=['POST'])
@jwt_required()
def create_match():

    data = request.json

    new_match = match(
        name=data.get('name'),
        logo=data.get('logo'),
        wins=data.get('wins'),
        number=data.get('number'),
        group=data.get('group'),
    )

    session = Session()
    session.add(new_match)
    session.commit()
    return new_match.to_dict()

@match_blueprint.route('/matches', methods=['POST'])
@jwt_required()
def create_all_match():

    data = request.json
    
    session = Session()
    
    new_matches = []
    
    for match_data in data:
        new_match = Match(
            team_idteam1=match_data.get('team1').get('id'),
            team_idteam2=match_data.get('team2').get('id'),
            draftEdition=match_data.get('edition'),
            phase=match_data.get('phase'),
            group=match_data.get('group'),
            format=match_data.get('format'),
            day=match_data.get('day'),
            hour=match_data.get('hour'),
            isDone=match_data.get('isDone'),
            isScheduled=match_data.get('isScheduled'),
            score=match_data.get('score'),
            freeSchedule=str(match_data.get('freeSchedule'))
        )
        new_matches.append(new_match)
    
    session.add_all(new_matches)
    session.commit()

    return [match.to_dict() for match in new_matches]

@match_blueprint.route('/match/<int:match_id>', methods=['PUT'])
@jwt_required()
def update_match(match_id):
    session = Session()
    match = session.query(Match).filter_by(idmatch=match_id).first()
    if not match:
        return jsonify({'message': 'Time não encontrado'}), 404

    data = request.json
    new_match = match(
        name=data.get('name'),
        logo=data.get('logo'),
        wins=data.get('wins'),
        number=data.get('number'),
        group=data.get('group'),
    )
    return match.to_dict()

@match_blueprint.route('/matches', methods=['PUT'])
@jwt_required()
def update_all_matches():
    try:
        session = Session()

        matches_data = request.json
        for match_data in matches_data:
            match_id = match_data.get('id')
            if not match_id:
                return jsonify({'error': 'Cada time precisa ter um "id".'}), 400

            update_data = {
                'name': match_data.get('name'),
                'logo': match_data.get('logo'),
                'wins': match_data.get('wins'),
                'number': match_data.get('number'),
                'group': match_data.get('group'),
            }
            filtered_data = {key: value for key, value in update_data.items() if value is not None}

            if filtered_data:
                session.query(match).filter_by(idmatch=match_id).update(filtered_data, synchronize_session=False)

        session.commit()

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()

    return jsonify({'message': 'matches atualizados!'}), 200

@match_blueprint.route('/match/<int:match_id>', methods=['DELETE'])
@jwt_required()
def delete_match(match_id):
    session = Session()
    match = session.query(match).filter_by(idmatch=match_id).first()
    if not match:
      return jsonify({'message': 'Time não encontrado'}), 404
    else:
        session.delete(match)
        session.commit()
    return match.to_dict()



