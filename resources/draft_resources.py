from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import draft_blueprint
from database import Session
from model.models import *
from datetime import datetime

@draft_blueprint.route('/drafts', methods=['GET'])
# @jwt_required()
def get_drafts():
    session = Session()
    drafts = session.query(Draft).all()
    return jsonify([draft.to_dict() for draft in drafts])

@draft_blueprint.route('/unique_drafts', methods=['GET'])
# @jwt_required()
def get_unique_drafts():
    session = Session()
    distinct_drafts = session.query(Draft.edition, Draft.game).distinct().all()
    distinct_drafts_dict = [{'edition': edition, 'game': game} for edition, game in distinct_drafts]
    return jsonify(distinct_drafts_dict)

@draft_blueprint.route('/unique_completed_drafts', methods=['GET'])
# @jwt_required()
def get_unique_completed_drafts():
    session = Session()
    distinct_drafts = session.query(Draft.edition, Draft.game).filter(Draft.isActive == 0).distinct().all()
    distinct_drafts_dict = [{'edition': edition, 'game': game} for edition, game in distinct_drafts]
    return jsonify(distinct_drafts_dict)

@draft_blueprint.route('/unique_active_drafts', methods=['GET'])
# @jwt_required()
def get_unique_active_drafts():
    session = Session()
    distinct_drafts = session.query(Draft.edition, Draft.game).filter(Draft.isActive == 1).distinct().all()
    distinct_drafts_dict = [{'edition': edition, 'game': game} for edition, game in distinct_drafts]
    return jsonify(distinct_drafts_dict)

@draft_blueprint.route('/draft/<int:draft_id>', methods=['GET'])
# @jwt_required()
def get_draft_by_id(draft_id):
    session = Session()
    draft = session.query(Draft).filter_by(iddraft=draft_id).first()
    if not draft:
        return jsonify({'message': 'Draft não encontrado'}), 404
    return draft.to_dict()

@draft_blueprint.route('/drafts_by_edition/<int:draft_edition>', methods=['GET'])
# @jwt_required()
def get_drafts_by_edition(draft_edition):
    session = Session()
    drafts = session.query(Draft).filter_by(edition=draft_edition).all()
    if not drafts:
        return jsonify({'message': 'Draft não encontrado'}), 404
    return jsonify([draft.to_dict() for draft in drafts])

@draft_blueprint.route('/draft_by_edition/<int:draft_edition>', methods=['GET'])
# @jwt_required()
def get_draft_by_edition(draft_edition):
    session = Session()
    draft = session.query(Draft).filter_by(edition=draft_edition).first()
    if not draft:
        return jsonify({'message': 'Draft não encontrado'}), 404
    return draft.to_dict()

@draft_blueprint.route('/draft', methods=['POST'])
# @jwt_required()
def create_draft():
    data = request.json
    player_id = data.get('player_id')
    team_id = data.get('team_id')
    edicao = data.get('edition')
    game = data.get('game')
    draftdate = data.get('draftdate')
    finaldate = data.get('finaldate')
    teamsQuantity = data.get('teamsQuantity')
    playersPerTeam = data.get('playersPerTeam')

    try:
        new_draft = Draft(
            player_idplayer=player_id,
            team_idteam=team_id,
            edicao=edicao,
            game=game,
            draftdate=draftdate,
            finaldate=finaldate
        )

        session = Session()
        session.add(new_draft)
        session.commit()

        return jsonify(new_draft.to_dict()), 201

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()

@draft_blueprint.route('/new_draft', methods=['POST'])
# @jwt_required()
def new_draft():
    with Session() as session:
        try:
            players = request.json['players']
            for player in players:
                new_player = session.query(Player).filter_by(name=player['name']).first()
                if new_player:
                    # Se o jogador já existir, atualize seus atributos
                    new_player.nick = player.get('nick')
                    new_player.twitch = player.get('twitch')
                    new_player.email = player.get('email')
                    new_player.schedule = str(player.get('schedule'))
                    new_player.coins = player.get('coins')
                    new_player.stars = player.get('stars')
                    new_player.medal = player.get('medal')
                    new_player.wins = player.get('wins')
                    new_player.tags = player.get('tags')
                    new_player.isCaptain = player.get('isCaptain')
                    new_player.riot = player.get('riot')
                    new_player.steam = player.get('steam')
                    new_player.epic = player.get('epic')
                    new_player.xbox = player.get('xbox')
                    new_player.psn = player.get('psn')
                    new_player.score_cs = player.get('score_cs')
                    new_player.score_valorant = player.get('score_valorant')
                    new_player.score_lol = player.get('score_lol')
                    new_player.score_rocketleague = player.get('score_rocketleague')
                    new_player.score_fallguys = player.get('score_fallguys')
                else:
                    # Se o jogador não existir, crie um novo jogador
                    new_player = Player(
                        name = player.get('name'),
                        nick = player.get('nick'),
                        twitch = player.get('twitch'),
                        email = player.get('email'),
                        schedule = str(player.get('schedule')),
                        coins = player.get('coins', 0),
                        stars = player.get('stars'),
                        medal = player.get('medal'),
                        wins = player.get('wins'),
                        tags = player.get('tags'),
                        photo = player.get('photo'),
                        isCaptain = player.get('isCaptain', 0),
                        riot = player.get('riot'),
                        steam = player.get('steam'),
                        epic = player.get('epic'),
                        xbox = player.get('xbox'),
                        psn = player.get('psn'),
                        score_cs = player.get('score_cs'),
                        score_valorant = player.get('score_valorant'),
                        score_lol = player.get('score_lol'),
                        score_rocketleague = player.get('score_rocketleague'),
                        score_fallguys = player.get('score_fallguys'),
                    )
                session.add(new_player)
                session.flush()
                session.refresh(new_player)
                    
                # Se uma entrada no draft ja existe ligando player e edição use, senão crie.
                edition = request.json['config']['edition']
                draft = session.query(Draft).filter_by(player_idplayer=new_player.idplayer, edition=edition).first()
                if draft:
                    draft.player_idplayer = new_player.get('idplayer')
                    draft.edition = edition
                    draft.game = request.json['config']['game']
                    draft.teamsQuantity = request.json['config']['teamsQuantity']
                    draft.playersPerTeam = request.json['config']['teamPlayersQuantity']
                    draft.draftdate = datetime.now()
                    draft.isActive = 1
                else:
                    draft = Draft(
                        player_idplayer = new_player.idplayer,
                        edition = edition,
                        game = request.json['config']['game'],
                        teamsQuantity =  request.json['config']['teamsQuantity'],
                        playersPerTeam = request.json['config']['teamPlayersQuantity'],
                        draftdate =  datetime.now(),
                        isActive = 1
                    )
                    session.add(draft)

            session.commit()
            return jsonify({'message': 'Draft created successfully'}), 201

        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()

@draft_blueprint.route('/complete_draft', methods=['POST'])
# @jwt_required()
def create_complete_draft():
    with Session() as session:
        try:
            players = request.json['players']
            for player in players:
                new_player = session.query(Player).filter_by(name=player['name']).first()
                if new_player:
                    # Se o jogador já existir, atualize seus atributos
                    new_player.nick = player.get('nick')
                    new_player.twitch = player.get('twitch')
                    new_player.email = player.get('email')
                    new_player.schedule = str(player.get('schedule'))
                    new_player.coins = player.get('coins')
                    new_player.stars = player.get('stars')
                    new_player.medal = player.get('medal')
                    new_player.wins = player.get('wins')
                    new_player.tags = player.get('tags')
                    new_player.isCaptain = player.get('isCaptain')
                    new_player.riot = player.get('riot')
                    new_player.steam = player.get('steam')
                    new_player.epic = player.get('epic')
                    new_player.xbox = player.get('xbox')
                    new_player.psn = player.get('psn')
                    new_player.score_cs = player.get('score_cs')
                    new_player.score_valorant = player.get('score_valorant')
                    new_player.score_lol = player.get('score_lol')
                    new_player.score_rocketleague = player.get('score_rocketleague')
                    new_player.score_fallguys = player.get('score_fallguys')
                else:
                    # Se o jogador não existir, crie um novo jogador
                    new_player = Player(
                        name = player.get('name'),
                        nick = player.get('nick'),
                        twitch = player.get('twitch'),
                        email = player.get('email'),
                        schedule = str(player.get('schedule')),
                        coins = player.get('coins', 0),
                        stars = player.get('stars'),
                        medal = player.get('medal'),
                        wins = player.get('wins'),
                        tags = player.get('tags'),
                        photo = player.get('photo'),
                        isCaptain = player.get('isCaptain', 0),
                        riot = player.get('riot'),
                        steam = player.get('steam'),
                        epic = player.get('epic'),
                        xbox = player.get('xbox'),
                        psn = player.get('psn'),
                        score_cs = player.get('score_cs'),
                        score_valorant = player.get('score_valorant'),
                        score_lol = player.get('score_lol'),
                        score_rocketleague = player.get('score_rocketleague'),
                        score_fallguys = player.get('score_fallguys'),
                    )
                session.add(new_player)
                session.flush()
                session.refresh(new_player)

                # Se o time com este numero ja existir crie relacionamento senão crie um novo time
                team_number = player['team']
                team = session.query(Team).filter_by(number=player['team']).first()
                if not team:
                    team = Team(
                    name = 'Time '+str(team_number),
                    wins = 0,
                    number = team_number
                    )

                    session.add(team)
                    session.flush()
                    session.refresh(team)
                    
                # Se uma entrada no draft ja existe ligando player e time use, senão crie.
                edition = request.json['config']['edition']
                draft = session.query(Draft).filter_by(player_idplayer=new_player.idplayer, team_idteam=team.idteam).first()
                if draft:
                    draft.player_idplayer = new_player.get('idplayer')
                    draft.team_idteam = team.get('idteam')
                    draft.edition = edition
                    draft.game = request.json['config']['game']
                    draft.teamsQuantity = request.json['config']['teamsQuantity']
                    draft.playersPerTeam = request.json['config']['teamPlayersQuantity']
                    draft.draftdate = datetime.now()
                    draft.isActive = 0
                else:
                    draft = Draft(
                        player_idplayer = new_player.idplayer,
                        team_idteam = team.idteam,
                        edition = edition,
                        game = request.json['config']['game'],
                        teamsQuantity =  request.json['config']['teamsQuantity'],
                        playersPerTeam = request.json['config']['teamPlayersQuantity'],
                        draftdate =  datetime.now(),
                        isActive = 0
                    )
                    session.add(draft)

            session.commit()
            return jsonify({'message': 'Draft created successfully'}), 201

        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            session.close()

@draft_blueprint.route('/draft/<int:draft_id>', methods=['PUT'])
# @jwt_required()
def update_draft(draft_id):
    session = Session()
    draft = session.query(Draft).filter_by(iddraft=draft_id).first()
    if not draft:
        return jsonify({'message': 'Draft não encontrado'}), 404

    data = request.json
    draft.player_idplayer = data.get('player_id') or draft.player_idplayer
    draft.team_idteam = data.get('team_id') or draft.team_idteam
    draft.edicao = data.get('edicao') or draft.edicao
    draft.game = data.get('game') or draft.game
    draft.draftdate = data.get('draftdate') or draft.draftdate
    draft.finaldate = data.get('finaldate') or draft.finaldate

    try:
        session.commit()
        return jsonify(draft.to_dict())

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()

@draft_blueprint.route('/draft/<int:draft_id>', methods=['DELETE'])
@jwt_required()
def delete_draft(draft_id):
    session = Session()
    draft = session.query(Draft).filter_by(iddraft=draft_id).first()
    if not draft:
        return jsonify({'message': 'Draft não encontrado'}), 404

    try:
        session.delete(draft)
        session.commit()
        return jsonify({'message': 'Draft deleted successfully'})

    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        session.close()