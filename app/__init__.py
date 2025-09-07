from flask import Flask
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.mechanic import mechanic_bp
from .blueprints.service_ticket import service_ticket_bp
from .blueprints.inventory import inventories_bp
from .blueprints.customer import customers_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' #Url for exposing my swagger ui
API_URL = '/static/swagger.yaml'

swagger_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'Mechanic Management API'} )

def create_app(config_name):
    app = Flask(__name__) #creating base app
    app.config.from_object(f'config.{config_name}')

    #initialize extensions
    db.init_app(app) #adding the db to the app
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    #register blueprints
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service_tickets')
    app.register_blueprint(inventories_bp, url_prefix='/parts')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
    return app

