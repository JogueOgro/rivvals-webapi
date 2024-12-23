from flask import Blueprint

draft_blueprint = Blueprint('draft', __name__)
info_blueprint = Blueprint('info', __name__)
player_blueprint = Blueprint('player', __name__)
team_blueprint = Blueprint('team', __name__)
match_blueprint = Blueprint('match', __name__)
coin_blueprint = Blueprint('coin', __name__)
user_blueprint = Blueprint('user', __name__)
util_blueprint = Blueprint('util', __name__)

def register_blueprints(app):
    from .draft_resources import draft_blueprint
    from .info_resources import info_blueprint
    from .player_resources import player_blueprint
    from .team_resources import team_blueprint
    from .match_resources import match_blueprint
    from .coin_resources import coin_blueprint
    from .user_resources import user_blueprint
    from .util_resources import util_blueprint
    
    app.register_blueprint(draft_blueprint)
    app.register_blueprint(info_blueprint)
    app.register_blueprint(player_blueprint)
    app.register_blueprint(team_blueprint)
    app.register_blueprint(match_blueprint)
    app.register_blueprint(coin_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(util_blueprint)