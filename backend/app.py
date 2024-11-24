from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    # Muat variabel lingkungan dari file .env
    load_dotenv()
    
    app = Flask(__name__)

    # Konfigurasi
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES')))
    app.config['UPLOAD_FOLDER'] = "uploads"
    
    app.config['MAIL_SERVER'] = "smtp.googlemail.com"
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
    app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
    jwt = JWTManager(app)

    CORS(app)

    db.init_app(app)
    mail.init_app(app)

    from routes import register_route
    register_route(app)

    migrate = Migrate(app, db)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)