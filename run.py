from app import create_app
from resources import register_blueprints

app = create_app()
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)