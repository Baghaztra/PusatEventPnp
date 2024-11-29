from flask import Blueprint, request, jsonify, session, abort, redirect, current_app, render_template
from flask_mail import Mail, Message
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
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
from app import db, mail

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
        user = User(username=name, email=email, google_id=google_id, status="Active",
                    profile_picture=pfp, created_at=datetime.now())
        db.session.add(user)
        db.session.commit()

    access_token = create_access_token(
        identity={'user_id': user.id, 'username': user.username, 'role': user.role})
    # return jsonify({"message": "Login berhasil", "token": access_token}), 200
    return redirect(f"http://localhost:8080/home?token={access_token}")

# Normal way

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and user.verify_password(password):
        if user.status == "Active":
            access_token = create_access_token(
                identity={'user_id': user.id, 'username': user.username, "role":user.role})
            return jsonify({"message": "Login success", "token": access_token, "role":user.role}), 200
        else:
            return jsonify({"message": "The account is not active."}), 401
    else:
        return jsonify({"message": "Invalid email or password."}), 401

@login_bp.route('/eo-login', methods=['POST'])
def login_eo():
    data = request.get_json()
    email = data['email']
    password = data['password']

    eo = EventOrganizer.query.filter_by(email=email).first()

    if eo and eo.verify_password(password):
        if eo.status == "Active":
            access_token = create_access_token(
                identity={'user_id': eo.id, 'username': eo.username, 'role':"event organizer"})
            return jsonify({"message": "Login success", "token": access_token}), 200
        elif eo.status == "Waiting Admin":
            return jsonify({"message": "We still waiting admin to accept this account."}), 401
        else:
            return jsonify({"message": "The account is not active."}), 401
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

    # Periksa apakah emeail sudah pernah digunakan
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(username=name, password=password,
                    email=email, created_at=datetime.now())
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(
            identity={'user_id': user.id, 'username': user.username, 'role': 'user'})
        
        # Kirim email verifikasi
        msg_title = "Konfirmasi Akun Anda"
        sender = "noreply@app.com"
        verification_link = f"http://localhost:5000/verify/{access_token}"

        msg = Message(
            msg_title,
            sender=sender,
            recipients=[email]
        )
        msg_body = f"Halo {name},\n\nKlik link berikut untuk memverifikasi akun Anda:"
        data = {
            'app_name': "Pusat Event Politeknik",
            'title': msg_title,
            'body': msg_body,
            'link': verification_link
        }
        msg.html = render_template("email.html", data=data)

        try:
            mail.send(msg)
            return jsonify({
                "message": "Registration successful. Please check your email to verify your account.",
                "user_id": user.id,
                "role": "user"
            }), 201
        except Exception as e:
            print(e)
            return jsonify({"message": "Failed to send verification email."}), 500
    else:
        return jsonify({"message": "Email already registered."}), 400
    
@login_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        # Decode token
        user_identity = decode_token(token)['sub']
        user_id = user_identity['user_id']
        role = user_identity['role']
        
        # Aktifkan user
        if(role == 'user'):
            user = User.query.get(user_id)
            if user:
                user.status = "Active"
                db.session.commit()
                context = {
                    "status":200,
                    "goto":"http://127.0.0.1:8080/login",
                    "message":"Account verified successfully."
                }
                return render_template("redirect.html", **context)
            else:
                context = {
                    "status":498,
                    "goto":"",
                    "message":"Invalid or expired token."
                }
                return render_template("redirect.html", **context)
        elif(role == 'event organizer'):
            user = EventOrganizer.query.get(user_id)
            if user:
                user.status = "Waiting Admin"
                db.session.commit()
                context = {
                    "status":200,
                    "goto":"http://127.0.0.1:8080/eo-login",
                    "message":"Email verified successfully. Wait for confirmation by admin."
                }
                return render_template("redirect.html", **context)
            else:
                context = {
                    "status":489,
                    "goto":"",
                    "message":"Invalid or expired token."
                }
                return render_template("redirect.html", **context)
    except Exception as e:
        print(e)
        context = {
            "status":404,
            "goto":"",
            "message": e
        }
        return render_template("redirect.html", **context)

@login_bp.route('/profile', methods=['GET'])
@jwt_required() 
def get_profile():
    identity = get_jwt_identity()
    user_id = identity.get('user_id')
    role = identity.get('role')

    if not user_id:
        return jsonify({"message": "User ID not found in token."}), 400
    if role == 'event organizer':
        user = EventOrganizer.query.get(user_id)
    else:
        user = User.query.get(user_id)

    if user:
        return jsonify({
            "user_id": user.id,
            "username": user.username,
            "profile_picture": user.profile_picture,
            "role": role 
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404

@login_bp.route('/resend', methods=['POST'])
def resend():
    data = request.get_json()
    user_id = data['user_id']
    role = data['role']
    
    if(role == 'user'):
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 400
    elif(role == 'event organizer'):
        user = EventOrganizer.query.get(user_id)
        if not user:
            return jsonify({"message": "Event organizer not found"}), 400
    
    access_token = create_access_token(
            identity={'user_id': user_id, 'username': user.username, 'role': role})
    
    msg_title = "Konfirmasi Akun Anda"
    sender = "noreply@app.com"
    verification_link = f"http://localhost:5000/verify/{access_token}"

    msg = Message(
        msg_title,
        sender=sender,
        recipients=[user.email]
    )
    msg_body = f"Halo {user.username},\n\nKlik link berikut untuk memverifikasi akun Anda:"
    data = {
        'app_name': "Pusat Event Politeknik",
        'title': msg_title,
        'body': msg_body,
        'link': verification_link
    }
    msg.html = render_template("email.html", data=data)

    try:
        mail.send(msg)
        return jsonify({"message": "Registration successful. Please check your email to verify your account."}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to send verification email."}), 500