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
        'body': msg_body,
        'link': verification_link
    }
    msg.html = render_template("email.html", data=data)

    try:
        mail.send(msg)
        return jsonify({
            "message": "Registration successful. Please check your email to verify your account.",
            "user_id": eo.id,
            "role": "event organizer"
        }), 201
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
        
        if(role=='admin' or (user_id == event.eo_id and role == 'event organizer')):
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

@eo_bp.route('/update/poster', methods=['PATCH'])
@jwt_required()
def poster_update():
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')
        role = identity.get('role')
        
        if 'poster' in request.files:
            event_id = request.form.get('id')
            event = Event.query.get(event_id)
            if not event:
                return jsonify({'message': 'Event not found'}), 404
            
            if event.poster and os.path.exists(event.poster.replace('http://localhost:5000/', '')):
                os.remove(event.poster.replace('http://localhost:5000/', ''))
            
            file = request.files['poster']
            filename = secure_filename(file.filename)

            upload_path = os.path.join(f'uploads\\events\\{event_id}', filename)
            file.save(upload_path)

            poster_url = f'http://localhost:5000/uploads/events/{event_id}/{filename}'
            event.poster = poster_url
            db.session.commit()

            return jsonify({'message': 'Poster updated successfully'}), 200

        else:
            return jsonify({'message': 'No file provided'}), 400
        
    except Exception as e:
        print("error deleting event",e)
        return jsonify({'message': str(e)}), 500

@eo_bp.route('/update/event', methods=['PATCH'])
@jwt_required()
def event_update():
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')
        role = identity.get('role')
        
        event_id = request.json.get('id')
        key = request.json.get('key')
        value = request.json.get('value')
        
        event = Event.query.get(event_id)
        if (not event):
            return jsonify({'message': "Event not found"}), 404
        
        if(user_id == event.eo_id and role == 'event organizer'):
            if hasattr(event, key): 
                setattr(event, key, value) 
                db.session.commit() 
                return jsonify({'message': "Event has been updated."}), 200
            else:
                return jsonify({'message': f"Invalid field: {key}"}), 400
        else:    
            return jsonify({'message': "Only creator can update this"}), 401
    except Exception as e:
        print("error updating event",e)
        return jsonify({'message': str(e)}), 500
    
@eo_bp.route('/update/profile', methods=['PATCH'])
@jwt_required()
def profile_update():
    try:
        identity = get_jwt_identity()
        
        role = identity.get('role')
        if (role != 'event organizer'):
            return jsonify({'message': "User is not an eo"}), 401
        
        user_id = identity.get('user_id')
        eo = EventOrganizer.query.get(user_id)
        if (not eo):
            return jsonify({'message': "Eo not found"}), 404
        
        key = request.json.get('key')
        value = request.json.get('value')
        if hasattr(eo, key): 
            setattr(eo, key, value) 
            db.session.commit() 
            return jsonify({'message': "Profile updated."}), 200
        else:
            return jsonify({'message': f"Invalid field: {key}"}), 400
        
    except Exception as e:
        print("error updating profile",e)
        return jsonify({'message': str(e)}), 500
    
@eo_bp.route('/file/update-profile-picture', methods=['PATCH'])
@jwt_required()
def update_pfp():
    try:
        # Mendapatkan identitas pengguna dari JWT
        identity = get_jwt_identity()
        user_id = identity.get('user_id')
        user = EventOrganizer.query.get(user_id)

        # Pastikan pengguna ada di database
        if not user:
            return jsonify({'message': 'EO not found'}), 404

        # Pastikan file dikirimkan dalam request
        if 'profile_picture' not in request.files:
            return jsonify({'message': 'No file provided'}), 400

        file = request.files['profile_picture']

        # Validasi nama file
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        # Validasi format file (misalnya hanya menerima gambar)
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'message': 'Invalid file type. Only images are allowed.'}), 400

        # Hapus gambar lama jika ada
        if user.profile_picture and os.path.exists(user.profile_picture.replace('http://localhost:5000/', '')):
            os.remove(user.profile_picture.replace('http://localhost:5000/', ''))

        # Simpan file dengan nama aman
        filename = secure_filename(file.filename)
        upload_path = os.path.join('uploads', 'eo_pfp', filename)

        # Pastikan direktori tujuan ada
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        file.save(upload_path)

        # Update URL di database
        pfp_url = f'http://localhost:5000/uploads/eo_pfp/{filename}'
        user.profile_picture = pfp_url
        db.session.commit()

        return jsonify({'message': 'Profile picture updated successfully', 'profile_picture_url': pfp_url}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500
    
@eo_bp.route('/file/upload/<id>', methods=['POST'])
def event_file_upload(id):
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(f"uploads\\events\\{id}", filename)
        file.save(filepath)

        new_image = Image(
            event_id=id,
            path = f'http://localhost:5000/uploads/events/{id}/{filename}',
            created_at=datetime.now()
        )
        db.session.add(new_image)
        db.session.commit()

        return jsonify({'message': 'File uploaded successfully', 'image_id': new_image.id}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    
@eo_bp.route('/file/delete/<id>', methods=['DELETE'])
def event_file_delete(id):
    try:
        print(f"try to deleting {id}")
        if not id:
            return jsonify({'error': 'Image ID is required'}), 400

        image = Image.query.filter_by(id=id).first()
        if not image:
            return jsonify({'error': 'File not found'}), 404

        if os.path.exists(image.path.replace('http://localhost:5000/', '')):
            os.remove(image.path.replace('http://localhost:5000/', ''))

        db.session.delete(image)
        db.session.commit()

        return jsonify({'message': 'File deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@eo_bp.route('/send-email-event', methods=['POST'])
@jwt_required()
def sendEmailEvent():
    try:
        identity = get_jwt_identity()
        user_id = identity.get('user_id')
        user = EventOrganizer.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 400
        
        data = request.get_json()
        event_id = data.get('id')
        message = data.get('message')
        if not event_id or not message:
            return jsonify({"error": "Missing required fields"}), 400
        
        recipients = [follow.follower.email for follow in user.followers]
        print(recipients)
        msg = Message(
            user.username,
            sender="noreply@app.com",
            recipients=recipients
        )
        data = {
            'title': "New Event Announced",
            'message': message,
            'goto': f"http://127.0.0.1:8080/event/{event_id}",
            'goto_msg': "Go to event",
        }

        msg.html = render_template("info.html", **data)

        try:
            mail.send(msg)
            return {"message": f"Email sent successfully to your followers"}
        except Exception as e:
            print(f"Email Error: {e}")
            raise

    except Exception as e:
        print("error deleting event",e)
        return jsonify({'message': str(e)}), 500
