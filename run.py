from app import create_app
from resources import register_blueprints

app = create_app()
register_blueprints(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
