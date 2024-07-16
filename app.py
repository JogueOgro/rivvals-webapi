from flask import Flask
from flask_cors import CORS
from resources.draft_resources import draft_blueprint
from resources.player_resources import player_blueprint
from resources.team_resources import team_blueprint
from resources.coin_resources import coin_blueprint
from resources.user_resources import user_blueprint

app = Flask(__name__)
app.register_blueprint(draft_blueprint)
app.register_blueprint(player_blueprint)
app.register_blueprint(team_blueprint)
app.register_blueprint(coin_blueprint)
app.register_blueprint(user_blueprint)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
