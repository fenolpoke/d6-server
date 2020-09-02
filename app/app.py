

def create_app(app_name='NewsAPI'):
    from flask import Flask
    from flask_cors import CORS

    from app.api import api
    from app.models import db
    
    app = Flask(app_name)
    app.config.from_object('app.config.Config')

    cors = CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:3000", "methods": "GET,PUT,POST,DELETE"}})

    app.register_blueprint(api, url_prefix="/api")

    db.init_app(app)

    return app
