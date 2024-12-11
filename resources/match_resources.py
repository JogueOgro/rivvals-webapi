from flask import request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from sqlalchemy.dialects.mysql import insert
import pytz
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
                Match.isScheduled == 1,
                or_(Match.team_idteam1 == idteam, Match.team_idteam2 == idteam)
            )
            .all()
        )
        matches_dicts = [match.to_dict() for match in matches]
        return jsonify(matches_dicts)
    except Exception as e:
        return jsonify({'message': 'Erro no servidor', 'error': str(e)}), 500
    finally:
        session.close()


from sqlalchemy.orm import joinedload

@match_blueprint.route('/match/<int:match_id>', methods=['GET'])
@jwt_required()
def get_match_by_id(match_id):
    session = Session()
    try:
        match = (
            session.query(Match)
            .options(joinedload(Match.team1), joinedload(Match.team2))
            .filter_by(idmatch=match_id)
            .first()
        )
        if not match:
            return jsonify({'message': 'Partida não encontrada'}), 404
        return jsonify(match.to_dict())
    except Exception as e:
        return jsonify({'message': 'Erro interno do servidor', 'error': str(e)}), 500
    finally:
        session.close()



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
            existing_match = session.query(Match).filter(
                Match.team_idteam1 == match_data.get('team1').get('id'),
                Match.team_idteam2 == match_data.get('team2').get('id'),
                Match.draftEdition == match_data.get('draftEdition'),
            ).first()

            if existing_match:
                existing_match.phase = match_data.get('phase')
                existing_match.group = match_data.get('group')
                existing_match.format = match_data.get('format')
                existing_match.isDone = match_data.get('isDone')
                existing_match.isScheduled = match_data.get('isScheduled')
                existing_match.scheduledDate = match_data.get('scheduledDate')
                existing_match.winner = match_data.get('winner')
                existing_match.scoreTeam1 = match_data.get('scoreTeam1')
                existing_match.scoreTeam2 = match_data.get('scoreTeam2')
                existing_match.freeSchedule = str(match_data.get('freeSchedule'))
                existing_match.confirmation = str(match_data.get('confirmation'))
                existing_match.conclusionDate = match_data.get('conclusionDate')
            else:
                new_match = Match(
                    team_idteam1=match_data.get('team1').get('id'),
                    team_idteam2=match_data.get('team2').get('id'),
                    draftEdition=match_data.get('draftEdition'),
                    phase=match_data.get('phase'),
                    group=match_data.get('group'),
                    format=match_data.get('format'),
                    isDone=match_data.get('isDone'),
                    isScheduled=match_data.get('isScheduled'),
                    scheduledDate=match_data.get('scheduledDate'),
                    winner=match_data.get('winner'),
                    scoreTeam1=match_data.get('scoreTeam1'),
                    scoreTeam2=match_data.get('scoreTeam2'),
                    freeSchedule=str(match_data.get('freeSchedule')),
                    confirmation=str(match_data.get('confirmation')),
                    conclusionDate=match_data.get('conclusionDate'),
                )
                session.add(new_match)

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
    
    def parse_date(date_string):
        if not date_string:
            return None
        try:
            parsed_date = datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S GMT")
            return parsed_date.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return date_string

    try:
        match = session.query(Match).filter_by(idmatch=match_id).first()
        if not match:
            return jsonify({'error': 'Match not found'}), 404

        data = request.json
        allowed_fields = [
            'team_idteam1', 'team_idteam2', 'draftEdition', 'phase', 'group', 
            'format', 'isDone', 'isScheduled', 'scheduledDate', 'winner', 
            'scoreTeam1', 'scoreTeam2', 'freeSchedule', 'reschedule', 'confirmation', 'conclusionDate'
        ]

        def parse_date(date_str):
            if isinstance(date_str, str):
                date_obj = datetime.fromisoformat(date_str)
                return date_obj.astimezone(pytz.utc)
            elif isinstance(date_str, datetime):
                if date_str.tzinfo is None:
                    return date_str.replace(tzinfo=pytz.utc)
                return date_str.astimezone(pytz.utc)
            return date_str

        for key in allowed_fields:
            if key in data:
                if key == 'freeSchedule' and isinstance(data[key], list):
                    setattr(match, key, json.dumps(data[key]))
                if key == 'confirmation' and isinstance(data[key], dict):
                    setattr(match, key, json.dumps(data[key]))
                elif key == 'scheduledDate' or key == 'conclusionDate':
                    setattr(match, key, parse_date(data[key]))
                else:
                    setattr(match, key, data[key])

        session.commit()
        return jsonify({'message': 'Partida Atualizada'}), 200

    except Exception as e:
        session.rollback()
        return jsonify({'error': f'Server error: {str(e)}'}), 500

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




