from flask import Blueprint, request, jsonify
from datetime import datetime
from models import *
from app import db

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
            "images": [image.path for image in event.images],
            "likes": [like.user_id for like in event.likes],
            "description": event.description,
            "event_date": event.start_date,
            "event_date_end": event.end_date,
            "created_at": event.created_at
        }
        for event in events
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
            "images": [image.path for image in event.images],
            "likes": [like.user_id for like in event.likes],
            "comments": [
                    {
                        "username":comment.user.username,
                        "username":comment.user.profile_picture,
                        "text":comment.content,
                        "created_at":comment.created_at,
                    } for comment in event.comments
                ],
            "description": event.description,
            "event_date": event.start_date,
            "event_date_end": event.end_date,
            "created_at": event.created_at
        }), 200
    
    return jsonify({"message": "User not found."}), 404

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
            role=data.get('role')
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
                "status": "Active",
                "profile_picture": user.profile_picture,
                "role": "user",
                "created_at": datetime.now()
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
                "created_at": eo.created_at
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
