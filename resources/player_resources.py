from flask import request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from . import player_blueprint
from model.models import *
from database import Session
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import os
import hashlib

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
    
@player_blueprint.route('/player/username/<string:username>', methods=['GET'])
@jwt_required()
def get_player_by_username(username):
    session = Session()
    
    try:
        player = session.query(Player).filter(Player.email.like(f"{username}.%")).first()
        if player:
            return jsonify(player.to_dict())
        else:
            return jsonify({'message': 'Jogador não encontrado'}), 404
    finally:
        session.close()

    
@player_blueprint.route('/player/email/<string:email>', methods=['GET'])
@jwt_required()
def get_player_by_email(email):
    try:
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

    data = request.json

    new_player = Player(
        name=data.get('name'),
        nick=data.get('nick'),
        twitch=data.get('twitch'),
        email=data.get('email'),
        schedule='[]',
        coins=0,
        stars=0,
        medal=0,
        wins=0,
        tags=data.get('tags'),
        isCaptain=0,
        isBackup=0,
    )

    session = Session()
    try:
        session.add(new_player)
        session.commit()
        session.refresh(new_player)
        return jsonify({'message': 'Player criado com sucesso'}), 200
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
        schedule=str(player.get('schedule')),
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
        return jsonify({'message': 'Player registrado com sucesso'}), 200
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
    player.mobile = data.get('mobile')
    player.favoriteGame = data.get('favoriteGame')
    player.riot = data.get('riot')
    player.steam = data.get('steam')
    player.epic = data.get('epic')
    player.xbox = data.get('xbox')
    player.psn = data.get('psn')

    session.commit()

    return jsonify({'message': 'Atualização realizada com sucesso'}), 200


@player_blueprint.route('/player/schedule/<int:idplayer>', methods=['PUT'])
@jwt_required()
def update_player_schedule(idplayer):
    session = Session()
    player = session.query(Player).filter_by(idplayer=idplayer).first()
    if not player:
        return jsonify({'message': 'Jogador não encontrado'}), 404

    data = request.json

    player.schedule = str(data.get('schedule'))
    session.commit()

    return jsonify({'message': 'Atualização realizada com sucesso'}), 200


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'pictures')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@player_blueprint.route('/pictures/<path:filename>')
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@player_blueprint.route('/player/picture/<int:idplayer>', methods=['PUT'])
@jwt_required()
def update_player_picture(idplayer):
    session = Session()
    player = session.query(Player).filter_by(idplayer=idplayer).first()
    if not player:
        return jsonify({'message': 'Jogador não encontrado'}), 404

    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'Nenhum arquivo selecionado'}), 400

    filename = secure_filename(file.filename)
    file_hash = hashlib.md5(filename.encode()).hexdigest()
    file_extension = os.path.splitext(filename)[1]
    new_filename = f"{file_hash}{file_extension}"

    file_path = os.path.join(UPLOAD_FOLDER, new_filename)

    try:
        file.save(file_path)
        player.photo = f"pictures/{new_filename}"
        session.commit()
        return jsonify({'message': 'Foto atualizada com sucesso'}), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao salvar o arquivo', 'error': str(e)}), 500
    finally:
        session.close()


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
