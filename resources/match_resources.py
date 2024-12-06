from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from sqlalchemy.dialects.mysql import insert
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


@match_blueprint.route('/matches/<int:edition_id>', methods=['GET'])
@jwt_required()
def get_matches_by_edition(edition_id):
    session = Session()
    matches = session.query(Match).options(joinedload(Match.team1),joinedload(Match.team2)).filter_by(draftEdition=edition_id).all()
    matches_dicts = [match.to_dict() for match in matches]
    return matches_dicts


@match_blueprint.route('/matches/scheduled/<int:edition_id>/<int:idteam>', methods=['GET'])
@jwt_required()
def get_scheduled_matches_by_edition_by_team(edition_id, idteam):
    session = Session()
    try:
        matches = (
            session.query(Match)
            .options(joinedload(Match.team1), joinedload(Match.team2))
            .filter(
                Match.draftEdition == edition_id,
                or_(Match.team_idteam1 == idteam, Match.team_idteam2 == idteam),
                Match.isScheduled == 1
            )
            .all()
        )
        
        matches_dicts = [match.to_dict() for match in matches]
        return jsonify(matches_dicts)
    except Exception as e:
        return jsonify({'message': 'Erro no servidor', 'error': str(e)}), 500
    finally:
        session.close()


@match_blueprint.route('/match/<int:match_id>', methods=['GET'])
@jwt_required()
def get_match_by_id(match_id):
    session = Session()
    match = session.query(Match).filter_by(idmatch=match_id).first()
    session.close()
    if not match:
      return jsonify({'message': 'Partida não encontrada'}), 404
    return match.to_dict()


@match_blueprint.route('/match', methods=['POST'])
@jwt_required()
def create_match():

    data = request.json

    new_match = Match(
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
def upsert_all_matches():
    data = request.json
    session = Session()

    try:
        for match_data in data:
            stmt = insert(Match).values(
                team_idteam1=match_data.get('team1').get('id'),
                team_idteam2=match_data.get('team2').get('id'),
                draftEdition=match_data.get('draftEdition'),
                phase=match_data.get('phase'),
                group=match_data.get('group'),
                format=match_data.get('format'),
                day=match_data.get('day'),
                hour=match_data.get('hour'),
                isDone=match_data.get('isDone'),
                isScheduled=match_data.get('isScheduled'),
                winner=match_data.get('winner'),
                scoreTeam1=match_data.get('scoreTeam1'),
                scoreTeam2=match_data.get('scoreTeam2'),
                freeSchedule=str(match_data.get('freeSchedule')),
            )
            update_fields = {
                'group': match_data.get('group'),
                'format': match_data.get('format'),
                'day': match_data.get('day'),
                'hour': match_data.get('hour'),
                'isDone': match_data.get('isDone'),
                'isScheduled': match_data.get('isScheduled'),
                'winner': match_data.get('winner'),
                'scoreTeam1': match_data.get('scoreTeam1'),
                'scoreTeam2': match_data.get('scoreTeam2'),
                'freeSchedule': str(match_data.get('freeSchedule')),
            }

            stmt = stmt.on_duplicate_key_update(update_fields)
            session.execute(stmt)

        session.commit()
        return jsonify({'message': 'Upsert concluído com sucesso'}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()


@match_blueprint.route('/match/<int:match_id>', methods=['PUT'])
@jwt_required()
def update_match(match_id):
    session = Session()
    try:
        match = session.query(Match).filter_by(id=match_id).first()
        if not match:
            return jsonify({'error': 'Match not found'}), 404

        data = request.json
        allowed_fields = [
            'team1', 'team2', 'draftEdition', 'phase', 'group', 'format', 
            'day', 'hour', 'isDone', 'isScheduled', 'score', 'freeSchedule'
        ]
        for key in allowed_fields:
            if key in data:
                setattr(match, key.lower() if key.lower() != key else key, data[key])

        session.commit()
        return jsonify({'message': 'Match updated successfully', 'match': match.id}), 200

    except e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()


@match_blueprint.route('/match/scores', methods=['POST'])
@jwt_required()
def update_scores():
    session = Session()
    
    try:
        data = request.json
        match_id = data.get('idMatch')
        match = session.query(Match).filter_by(idmatch=match_id).first()
        if not match:
            return jsonify({'error': 'Partida não encontrada'}), 404
        if 'scoreTeam1' in data:
            match.scoreTeam1 = data['scoreTeam1']
        if 'scoreTeam2' in data:
            match.scoreTeam2 = data['scoreTeam2']
        if 'winner' in data:
            match.winner = data['winner']
        if 'isDone' in data:
            match.isDone = data['isDone']
        if 'conclusionDate' in data:
            match.conclusionDate = data['conclusionDate']

        session.commit()
        return jsonify({'message': 'Placares atualizados!'}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()


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
                session.query(Match).filter_by(idmatch=match_id).update(filtered_data, synchronize_session=False)

        session.commit()

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()

    return jsonify({'message': 'matches atualizados!'}), 200




