from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/pusat_event'
    app.config['SECRET_KEY'] = 'pusatevent_asik'  # Ganti dengan kunci rahasia yang aman
    app.config['JWT_SECRET_KEY'] = 'jawet'  # Kunci ini digunakan untuk JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # Token kedaluwarsa dalam 1 jam

    jwt = JWTManager(app)

    db.init_app(app)

    from routes import register_route
    register_route(app, db)

    migrate = Migrate(app, db)

    return app