from flask import Blueprint

# Criação dos blueprints
draft_blueprint = Blueprint('draft', __name__)
player_blueprint = Blueprint('player', __name__)
team_blueprint = Blueprint('team', __name__)
coin_blueprint = Blueprint('coin', __name__)
user_blueprint = Blueprint('user', __name__)

def register_blueprints(app):
    from .draft_resources import draft_blueprint
    from .player_resources import player_blueprint
    from .team_resources import team_blueprint
    from .coin_resources import coin_blueprint
    from .user_resources import user_blueprint
    
    app.register_blueprint(draft_blueprint)
    app.register_blueprint(player_blueprint)
    app.register_blueprint(team_blueprint)
    app.register_blueprint(coin_blueprint)
    app.register_blueprint(user_blueprint)