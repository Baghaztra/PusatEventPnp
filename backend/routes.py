from flask import Flask,request,jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import *

def register_route(app, db):
    @app.route('/')
    def index():
        return "Bisa, bang :D"
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        user = User.query.filter_by(email=email).first()
        
        # jika ada user yang dicari, dan passwornya benar
        if user and user.verify_password(password):
            # Buat JWT token dengan informasi user_id
            access_token = create_access_token(identity={'user_id': user.id, 'username': user.username})
            return jsonify({"message": "Invalid email or password.", "token":access_token}), 200
        else:
            return jsonify({"message": "Invalid email or password."}), 401

    
    @app.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify({"access_token": new_access_token}), 200

