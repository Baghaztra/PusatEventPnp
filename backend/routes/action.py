from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import *
from datetime import datetime
from app import db

action_bp = Blueprint('action', __name__)

@action_bp.route('/like/<eid>', methods=['POST'])
@jwt_required() 
def like(eid):
    identity = get_jwt_identity()
    user_id = identity.get('user_id')
    
    if not user_id:
        return jsonify({"message": "User ID not found in token."}), 400
    
    user = User.query.get(user_id)    
    if not user:
        return jsonify({"message": "User not found."}), 404

    existing_like = Like.query.filter_by(user_id=user_id, event_id=eid).first()    
    if existing_like:
        db.session.delete(existing_like)
        message = "Like removed from user to event successfully"
    else:
        new_like = Like(
            user_id=user_id,
            event_id=eid,
            created_at=datetime.now()
        )
        db.session.add(new_like)
        message = "Like added from user to event successfully"

    db.session.commit()
    return jsonify({"msg": message}), 200

@action_bp.route('/comment', methods=['POST'])
@jwt_required() 
def comment():
    identity = get_jwt_identity()
    user_id = identity.get('user_id')
    
    if not user_id:
        return jsonify({"message": "User ID not found in token."}), 400
    
    user = User.query.get(user_id)    
    if user:
        data = request.get_json()
        comment = Comment(
            user_id=user_id,
            event_id=data['event_id'],
            content=data['message'],
            created_at=datetime.now()
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify({
            "msg": "comment from user to event successfully"
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404

@action_bp.route('/subscribe/<eid>', methods=['POST'])
@jwt_required() 
def subscribe(eid):
    identity = get_jwt_identity()
    user_id = identity.get('user_id')
    
    if not user_id:
        return jsonify({"message": "User ID not found in token."}), 400
    
    user = User.query.get(user_id)    
    if user:
        follow = Follow(
            user_id=user_id,
            event_id=eid,
            created_at=datetime.now()
        )
        db.session.add(follow)
        db.session.commit()
        return jsonify({
            "msg": "follow from user to event organizer added successfully"
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404

@action_bp.route('/report/<role>/<id>/<why>', methods=['POST'])
@jwt_required() 
def report(role, uid, why):
    identity = get_jwt_identity()
    user_id = identity.get('user_id')
    
    if not user_id:
        return jsonify({"message": "User ID not found in token."}), 400
    
    user = User.query.get(user_id)    
    if user:
        report = Report(
            reported_by_id=user_id,
            reported_id=uid,
            reported_type=role,
            reason=why,
            created_at=datetime.now()
        )
        db.session.add(report)
        db.session.commit()
        return jsonify({
            "msg": "reported successfully"
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404
