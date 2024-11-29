from flask import Blueprint, request, jsonify
from datetime import datetime
from models import *
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

data_bp = Blueprint('data', __name__)

@data_bp.route('/event-latest')
def event_latest():
    events = Event.query.order_by(Event.start_date.desc())

    events_list = [
        {
            "id": event.id,
            "title": event.title,
            "eo": event.event_organizer.username,
            "eo_id": event.event_organizer.id,
            "eo_status": event.event_organizer.status,
            "likes": [like.user_id for like in event.likes],
            "poster": event.poster,
            "registration_url": event.registration_url,
            "event_date": event.start_date,
            "event_date_end": event.end_date
        }
        for event in events if event.event_organizer.status == 'Active'
    ]

    return jsonify(events_list), 200

@data_bp.route('/event/<id>')
def event_details(id):
    event = Event.query.get(id)
    if event:
        return jsonify({
            "id": event.id,
            "title": event.title,
            "eo": event.event_organizer.username,
            "eo_id": event.event_organizer.id,
            "eo_status": event.event_organizer.status,
            "images": [
                {
                    'id':image.id,
                    'path':image.path 
                } for image in event.images],
            "likes": [like.user_id for like in event.likes],
            "comments": [
                    {
                        "id":comment.id,
                        "user_id":comment.user.id,
                        "username":comment.user.username,
                        "pfp":comment.user.profile_picture,
                        "text":comment.content,
                        "created_at":comment.created_at,
                    } for comment in reversed(event.comments)
                ],
            "description": event.description,
            "poster": event.poster,
            "registration_url": event.registration_url,
            "event_date": event.start_date,
            "event_date_end": event.end_date,
            "created_at": event.created_at
        }), 200
    
    return jsonify({"message": "User not found."}), 404

@data_bp.route('/event', methods=['POST'])
@jwt_required() 
def create_event():
    identity = get_jwt_identity()
    
    if(identity.get('role') != "event organizer"):
        return jsonify({"message": "Only EO can create event"}), 401
    
    eo_id = identity.get('user_id')
    title = request.form.get('title')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    description = request.form.get('description')

    poster = request.files.get('poster')

    new_event = Event(
        eo_id = eo_id,
        title = title,
        poster = "not yet",
        description = description,
        start_date = start_date,
        end_date = end_date,
        created_at = datetime.now()
    )
        
    db.session.add(new_event)
    db.session.commit()
    
    if poster:
        upload_folder = f'uploads/events/{new_event.id}/'
        os.makedirs(upload_folder, exist_ok=True) 
        file_path = os.path.join(upload_folder, poster.filename)
        poster.save(file_path)
        poster_url = "http://localhost:5000/" + file_path
        
        new_event.poster = poster_url
        db.session.add(new_event)
        db.session.commit()
        
    # Pindahkan TemporaryImage ke Image
    temporary_images = TemporaryImage.query.filter_by(eo_id=eo_id).all()

    if temporary_images:
        upload_folder = f'uploads/events/{new_event.id}/'
        os.makedirs(upload_folder, exist_ok=True)

        for temp_image in temporary_images:
            # Pindahkan file fisik
            old_path = temp_image.path
            new_path = os.path.join(upload_folder, os.path.basename(temp_image.path))
            if os.path.exists(old_path):
                os.rename(old_path, new_path)

            # Buat entri baru di tabel Image
            new_image = Image(
                event_id=new_event.id,
                path=f"http://localhost:5000/{new_path}",  # URL baru untuk gambar
                created_at=datetime.now()
            )
            db.session.add(new_image)
            if os.path.exists(temp_image.path):
                os.remove(temp_image.path)
            # Hapus entri TemporaryImage
            db.session.delete(temp_image)

        db.session.commit()

    
    data = {
        "id": new_event.id,
        "eo_id": new_event.eo_id,
        "eo_name": new_event.event_organizer.username,
        "title": new_event.title,
        "start_date": new_event.start_date,
        "end_date": new_event.end_date,
        "description": new_event.description,
        "poster": new_event.poster,
    }
    return jsonify(data)

@data_bp.route('/users', methods=['GET', 'POST', 'DELETE', 'PUT'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        new_user = User(
            google_id=data.get('google_id'),
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            profile_picture=data.get('profile_picture'),
            role=data.get('role'),
            created_at= datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully."}), 201

    elif request.method == 'GET' and 'id' in request.args:
        user = User.query.get(request.args['id'])
        if user:
            return jsonify({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "status": user.status,
                "profile_picture": user.profile_picture,
                "role": user.role,
                "created_at": user.created_at
            }), 200
        return jsonify({"message": "User not found."}), 404

    elif request.method == 'GET':
        users = User.query.all()
        all_users = [{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "status": user.status,
            "profile_picture": user.profile_picture,
            "role": user.role,
            "created_at": datetime.now()
        } for user in users]
        return jsonify(all_users), 200

    elif request.method == 'PUT' and 'id' in request.args:
        user = User.query.get(request.args['id'])
        if user:
            data = request.get_json()
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            if 'password' in data:
                user.password = data['password']
            user.profile_picture = data.get('profile_picture', user.profile_picture)
            user.role = data.get('role', user.role)
            db.session.commit()
            return jsonify({"message": "User updated successfully."}), 200
        return jsonify({"message": "User not found."}), 404

    elif request.method == 'DELETE' and 'id' in request.args:
        user = User.query.get(request.args['id'])
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully."}), 200
        return jsonify({"message": "User not found."}), 404

    return jsonify({"message": "Something went wrong :("}), 404

@data_bp.route('/event_organizers', methods=['GET', 'POST', 'DELETE', 'PUT'])
def event_organizers():
    if request.method == 'POST':
        data = request.get_json()
        new_eo = EventOrganizer(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            status='waiting',
            profile_picture=data.get('profile_picture'),
            bio=data.get('bio'),
            created_at=datetime.now()
        )
        db.session.add(new_eo)
        db.session.commit()
        return jsonify({"message": "Account created successfully."}), 201

    elif request.method == 'GET' and 'id' in request.args:
        eo = EventOrganizer.query.get(request.args['id'])
        if eo:
            return jsonify({
                "id": eo.id,
                "username": eo.username,
                "email": eo.email,
                "status": eo.status,
                "profile_picture": eo.profile_picture,
                "bio": eo.bio,
                "created_at": eo.created_at,
                "subs": [follow.follower_id for follow in eo.followers],
                "events": [
                    {
                        "id": event.id,
                        "title": event.title,
                        "eo": event.event_organizer.username,
                        "eo_id": event.event_organizer.id,
                        "likes": [like.user_id for like in event.likes],
                        "description": event.description,
                        "poster": event.poster,
                        "registration_url": event.registration_url,
                        "event_date": event.start_date,
                        "event_date_end": event.end_date
                    }for event in reversed(eo.event)
                ]
            }), 200
        return jsonify({"message": "Account not found."}), 404

    elif request.method == 'GET':
        eos = EventOrganizer.query.all()
        return jsonify([{
            "id": eo.id,
            "username": eo.username,
            "email": eo.email,
            "status": eo.status,
            "profile_picture": eo.profile_picture,
            "bio": eo.bio,
            "created_at": eo.created_at
        } for eo in eos]), 200

    elif request.method == 'PUT' and 'id' in request.args:
        eo = EventOrganizer.query.get(request.args['id'])
        if eo:
            data = request.get_json()
            eo.username = data.get('username', eo.username)
            eo.email = data.get('email', eo.email)
            eo.status = data.get('status', eo.status)
            eo.profile_picture = data.get('profile_picture', eo.profile_picture)
            eo.bio = data.get('bio', eo.bio)
            if 'password' in data:
                eo.password = data['password']
            db.session.commit()
            return jsonify({"message": "Account updated successfully."}), 200
        return jsonify({"message": "Account not found."}), 404

    elif request.method == 'DELETE' and 'id' in request.args:
        eo = EventOrganizer.query.get(request.args['id'])
        if eo:
            db.session.delete(eo)
            db.session.commit()
            return jsonify({"message": "Account deleted successfully."}), 200
        return jsonify({"message": "Account not found."}), 404

    return jsonify({"message": "Something went wrong :("}), 404
