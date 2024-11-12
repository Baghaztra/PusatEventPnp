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
    
    if 'pfp' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pfp']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

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

    if request.method == 'OPTIONS':
        # Merespons preflight dengan 200
        return jsonify({"message": "CORS preflight successful"}), 200
    response = {
        "message": "Registrasi berhasil! Tunggu konfirmasi dari admin!",
    }
    
    return jsonify(response), 200
