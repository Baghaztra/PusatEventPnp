from flask import Blueprint, request, jsonify, render_template
from flask_mail import Message
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from werkzeug.utils import secure_filename
from datetime import datetime
from models import EventOrganizer, TemporaryImage, Event, Like, Comment, Image
from app import db, mail
import os

eo_bp = Blueprint('eo', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

UPLOAD_FOLDER = 'uploads\\temporary_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

@eo_bp.route('/file/upload', methods=['POST'])
@jwt_required()
def file_upload():
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')

        if 'test' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400

        file = request.files['test']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        new_image = TemporaryImage(
            eo_id=user_id,
            path=filepath,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(new_image)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'image_id': new_image.id}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
@eo_bp.route('/file/delete', methods=['DELETE'])
@jwt_required()
def file_delete():
    # print("Request method:", request.method)
    # print("Request args:", request.args)
    # print("Request form:", request.form)
    # print("Request data:", request.data)
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')

        image_id = request.data.decode('utf-8')
        if not image_id:
            return jsonify({'error': 'Image ID is required'}), 400

        image = TemporaryImage.query.filter_by(id=image_id, eo_id=user_id).first()
        if not image:
            return jsonify({'error': 'File not found or not authorized to delete'}), 404

        if os.path.exists(image.path):
            os.remove(image.path)

        db.session.delete(image)
        db.session.commit()

        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@eo_bp.route('/delete/event', methods=['DELETE'])
@jwt_required()
def event_delete():
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')
        role = identity.get('role')
        event_id = request.args['id']
        
        event = Event.query.get(event_id)
        if (not event):
            return jsonify({'message': "Event not found"}), 404
        
        if(user_id == event.eo_id and role == 'event organizer'):
            likes = Like.query.filter_by(event_id=event_id)
            comments = Comment.query.filter_by(event_id=event_id)
            images = Image.query.filter_by(event_id=event_id)
            
            for image in images:
                if image.path and os.path.exists(image.path.replace('http://localhost:5000/', '')):
                    os.remove(image.path.replace('http://localhost:5000/', ''))
            
            if event.poster and os.path.exists(event.poster.replace('http://localhost:5000/', '')):
                os.remove(event.poster.replace('http://localhost:5000/', ''))
                
            likes.delete() 
            comments.delete()
            images.delete()
            db.session.delete(event)
            db.session.commit()
            
            return jsonify({'message': "Event has been deleted."}), 200
        else:    
            return jsonify({'message': "Only creator can delete this"}), 401
    except Exception as e:
        print("error deleting event",e)
        return jsonify({'message': str(e)}), 500
