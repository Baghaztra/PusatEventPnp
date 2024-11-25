from flask import Blueprint, request, jsonify, render_template
from flask_mail import Message
from flask_jwt_extended import create_access_token
from werkzeug.utils import secure_filename
from datetime import datetime
from models import EventOrganizer
from app import db, mail

eo_bp = Blueprint('eo', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@eo_bp.route('/eo-register', methods=['POST'])
def eo_register():
    data = request.form
    file = request.files.get('pfp')

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    bio = data.get('bio')

    if not all([name, email, password, bio]):
        return jsonify({"message": "Lengkapi semua field!"}), 400
    
    user = EventOrganizer.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Email already registered."}), 400
    if 'pfp' not in request.files:
        return jsonify({'message': 'Error! No file part'}), 400

    file = request.files['pfp']
    if file.filename == '':
        return jsonify({'message': 'Error! No selected file'}), 400

    filename = "uploads/eo_pfp/" + secure_filename(file.filename)
    file.save(filename)
    file_path = "http://localhost:5000/" + filename
    
    eo = EventOrganizer(
        username=name,
        email=email,
        password=password,
        bio=bio,
        status="Waiting",
        profile_picture=file_path,
        created_at=datetime.now()
    )
    
    db.session.add(eo)
    db.session.commit()

    access_token = create_access_token(
        identity={'user_id': eo.id, 'username': eo.username, 'role': 'event organizer'})
        
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
        return jsonify({"message": "Registration successful. Please check your email to verify your account."}), 201
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to send verification email."}), 500
        
    except Exception as e:
        print(e)
        return jsonify({"message": "Failed to send verification email."}), 500
