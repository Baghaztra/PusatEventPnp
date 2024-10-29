from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # JWT
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/pusat_event'
    app.config['SECRET_KEY'] = 'pusatevent_asik' 
    app.config['JWT_SECRET_KEY'] = 'jawet' 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    jwt = JWTManager(app)

    app.secret_key = 'pusatevent_asik'
    CORS(app)
    db.init_app(app)

    from routes import register_route
    register_route(app, db)

    migrate = Migrate(app, db)

    return app