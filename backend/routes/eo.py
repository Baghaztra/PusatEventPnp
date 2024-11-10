import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from datetime import datetime
from models import EventOrganizer
from app import db

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

    profile_picture_url = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        profile_picture_url = f"/{file_path}" 
    
    eo = EventOrganizer(
        username=name,
        email=email,
        password=password,
        bio=bio,
        status="Waiting",
        profile_picture=profile_picture_url,
        created_at=datetime.now()
    )
    
    db.session.add(eo)
    db.session.commit()

    response = {
        "message": "Registrasi berhasil! Tunggu konfirmasi dari admin!",
    }
    
    return jsonify(response), 200
