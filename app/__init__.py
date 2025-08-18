from flask import Flask
from .models import db
from .extensions import ma
from .blueprints.mechanic import mechanic_bp

def create_app(config_name):
    app = Flask(__name__) #creating base app
    app.config.from_object(f'config.{config_name}')

    #initialize extensions
    db.init_app(app) #adding the db to the app
    ma.init_app(app)

    #register blueprints
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    return app

