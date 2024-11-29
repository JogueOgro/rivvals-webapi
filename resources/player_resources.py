from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import player_blueprint
from model.models import *
from database import Session
from datetime import datetime
from email_validator import validate_email, EmailNotValidError

@player_blueprint.route('/players', methods=['GET'])
@jwt_required()
def get_players():
    session = Session()
    players = session.query(Player).all()
    return jsonify([player.to_dict() for player in players])

@player_blueprint.route('/player/<int:idplayer>', methods=['GET'])
@jwt_required()
def get_player_by_id(idplayer):
    session = Session()
    player = session.query(Player).filter_by(idplayer=idplayer).first()
    if player:
        return jsonify(player.to_dict())
    else:
        return jsonify({'message': 'Jogador não encontrado'}), 404
    


@player_blueprint.route('/player/email/<string:email>', methods=['GET'])
@jwt_required()
def get_player_by_email(email):
    try:
        # Valida o formato do e-mail
        validate_email(email)
    except EmailNotValidError as e:
        return jsonify({'message': 'Email inválido', 'error': str(e)}), 400

    session = Session()
    try:
        player = session.query(Player).filter_by(email=email).first()
        if player:
            return jsonify(player.to_dict())
        else:
            return jsonify({'message': 'Jogador não encontrado'}), 404
    finally:
        session.close()

@player_blueprint.route('/player', methods=['POST'])
@jwt_required()
def create_player():

    data = request.form

    new_player = Player(
        name=data.get('name'),
        nick=data.get('nick'),
        twitch=data.get('twitch'),
        email=data.get('email'),
        schedule=data.get('schedule'),
        coins=data.get('coins'),
        stars=data.get('stars'),
        medal=data.get('medal'),
        wins=data.get('wins'),
        tags=data.get('tags'),
        isCaptain=data.get('isCaptain'),
        isBackup=data.get('isBackup'),
        riot=data.get('riot'),
        steam=data.get('steam'),
        epic=data.get('epic'),
        xbox=data.get('xbox'),
        psn=data.get('psn'),
        score_cs=data.get('score_cs'),
        score_valorant=data.get('score_valorant'),
        score_lol = data.get('score_lol'),
        score_rocketleague = data.get('score_rocketleague'),
        score_fallguys = data.get('score_fallguys'),
    )

    session = Session()
    try:
        session.add(new_player)
        session.commit()
        session.refresh(new_player)  # Refresh na instancia para evitar erros
        return new_player.to_dict()
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@player_blueprint.route('/subscribe_player', methods=['POST'])
@jwt_required()
def subscribe_player():

    player = request.json['player'] 
    config = request.json['config']

    session = Session()
    existing_player = session.query(Player).filter_by(email=player.get('email')).first()
    if existing_player:
        new_player = existing_player
        existing_draft = session.query(Draft).filter_by(edition=config.get('edition'), player_idplayer=existing_player.idplayer).first()
        if existing_draft:
            return jsonify({'message': 'Player já registrado neste draft'}), 406
    else:
        new_player = Player(
        name=player.get('name'),
        nick=player.get('nick'),
        twitch=player.get('twitch'),
        email=player.get('email'),
        schedule=player.get('schedule'),
        coins=player.get('coins'),
        stars=player.get('stars'),
        medal=player.get('medal'),
        wins=player.get('wins'),
        tags=player.get('tags'),
        isCaptain=player.get('isCaptain'),
        isBackup=player.get('isBackup'),
        riot=player.get('riot'),
        steam=player.get('steam'),
        epic=player.get('epic'),
        xbox=player.get('xbox'),
        psn=player.get('psn'),
        score_cs=player.get('score_cs'),
        score_valorant=player.get('score_valorant'),
        score_lol = player.get('score_lol'),
        score_rocketleague = player.get('score_rocketleague'),
        score_fallguys = player.get('score_fallguys'),
    )
        session.add(new_player)
        session.flush()
        session.refresh(new_player)

    draft = Draft(
    player_idplayer = new_player.idplayer,
    edition = config.get('edition'),
    game = config.get('game'),
    draftDate =  datetime.now(),
    isActive = 1,
    )
    
    try:
        session.add(draft)
        session.commit()
        return new_player.to_dict()
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@player_blueprint.route('/player/<int:idplayer>', methods=['PUT'])
@jwt_required()
def update_player(idplayer):
    session = Session()
    player = session.query(Player).filter_by(idplayer=idplayer).first()
    if not player:
        return jsonify({'message': 'Jogador não encontrado'}), 404

    data = request.json

    player.name = data.get('name')
    player.nick = data.get('nick')
    player.twitch = data.get('twitch')
    player.email = data.get('email')
    player.schedule = data.get('schedule')
    player.coins = data.get('coins')
    player.stars = data.get('stars')
    player.medal = data.get('medal')
    player.wins = data.get('wins')
    player.tags = data.get('tags')
    player.photo = data.get('photo')

    session.commit()

    return jsonify(player.to_dict())

@player_blueprint.route('/player/pingpong/<int:idplayer>/<int:score>', methods=['PUT'])
@jwt_required()
def update_pingpong_score(idplayer, score):
    session = Session()
    try:
        player = session.query(Player).filter_by(idplayer=idplayer).first()
        if not player:
            return jsonify({'message': 'Jogador não encontrado'}), 404

        player.score_pingpong = score
        session.commit()

        return jsonify({'message': 'Score atualizado com sucesso'})
    except Exception as e:
        session.rollback()
        return jsonify({'message': 'Erro ao atualizar score', 'error': str(e)}), 500
    finally:
        session.close()
