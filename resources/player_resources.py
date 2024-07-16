from flask import request, jsonify, Blueprint
from model.models import *
from database import Session
import json

player_blueprint = Blueprint('player', __name__)

@player_blueprint.route('/players', methods=['GET'])
def get_players():
    session = Session()
    players = session.query(Player).all()
    return jsonify([player.to_dict() for player in players])

@player_blueprint.route('/player/<int:idplayer>', methods=['GET'])
def get_playe_by_id(idplayer):
    session = Session()
    player = session.query(Player).filter_by(idplayer=idplayer).first()
    if player:
        return jsonify(player.to_dict())
    else:
        return jsonify({'message': 'Jogador não encontrado'}), 404

@player_blueprint.route('/player', methods=['POST'])
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
        photo=data.get('photo')
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


@player_blueprint.route('/player/<int:idplayer>', methods=['PUT'])
def update_player(idplayer):
    session = Session()
    player = session.query(Player).filter_by(idplayer=idplayer).first()
    if not player:
        return jsonify({'message': 'Jogador não encontrado'}), 404

    data = request.json

    player.name = data['name']
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

@player_blueprint.route('/player/<int:idplayer>', methods=['DELETE'])
def delete_player(idplayer):
    session = Session()
    player = session.query(Player).filter_by(idplayer=idplayer).first()
    if not player:
        return jsonify({'message': 'Jogador não encontrado'}), 404

    session.delete(player)
    session.commit()

    return jsonify(player.to_dict())
