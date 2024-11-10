from flask import Blueprint, request, jsonify, session, abort, redirect
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import *
from datetime import datetime
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import google.auth.transport.requests
import cachecontrol
from dotenv import load_dotenv
import requests as req
import pathlib
import os
from app import db

# Membuat blueprint untuk login
login_bp = Blueprint('login', __name__)

load_dotenv()

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = os.getenv(
    "OAUTHLIB_INSECURE_TRANSPORT")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "../client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

# Google way

@login_bp.route('/google-login')
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@login_bp.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = req.Session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    google_id = id_info.get("sub")
    email = id_info.get("email")
    name = id_info.get("name")
    pfp = id_info.get("picture")

    # Cari user berdasarkan email atau buat user baru jika belum ada
    user = User.query.filter_by(email=email).first()

    if not user:
        # Simpan user baru jika belum ada
        user = User(username=name, email=email, google_id=google_id,
                    profile_picture=pfp, created_at=datetime.now())
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(
        identity={'user_id': user.id, 'username': user.username})
    # return jsonify({"message": "Login berhasil", "token": access_token}), 200
    return redirect(f"http://localhost:8080/home?token={access_token}")

# Normal way

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    # jika ada user yang dicari, dan passwornya benar
    if user and user.verify_password(password):
        # Buat JWT token dengan informasi user_id
        access_token = create_access_token(
            identity={'user_id': user.id, 'username': user.username})
        return jsonify({"message": "Login success", "token": access_token}), 200
    else:
        return jsonify({"message": "Invalid email or password."}), 401


@login_bp.route('/logout')
def logout():
    session.clear()
    return jsonify({"message": "Logout berhasil"}), 200


@login_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Periksa apakah user sudah ada
    user = User.query.filter_by(email=email).first()

    if not user:
        # Jika belum ada, buat user baru dengan password yang di-hash
        user = User(username=name, password=password,
                    email=email, created_at=datetime.now())
        db.session.add(user)
        db.session.commit()

        # Buat JWT token untuk user baru
        access_token = create_access_token(
            identity={'user_id': user.id, 'username': user.username})
        return jsonify({"message": "User registered successfully", "token": access_token}), 201
    else:
        return jsonify({"message": "Email already registered."}), 400


@login_bp.route('/profile', methods=['GET'])
@jwt_required()  # endpoint ini membutuhkan token untuk mengakses
def get_profile():
     # Ambil user_id dari token JWT
    identity = get_jwt_identity()
    user_id = identity.get('user_id')

    # Periksa apakah user_id ada
    if not user_id:
        return jsonify({"message": "User ID not found in token."}), 400

        # Cari user di database berdasarkan user_id
    user = User.query.get(user_id)

        # Jika user ditemukan, kembalikan data profilnya
    if user:
        return jsonify({
            "username": user.username,
            "profile_picture": user.profile_picture  # pastikan field ini ada di model User
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404
