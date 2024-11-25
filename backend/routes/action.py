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
    return jsonify({"message": message}), 200

@action_bp.route('/anu')
@jwt_required() 
def anu():
    identity = get_jwt_identity()
    user_id = identity.get('user_id')
    return user_id

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
            "message": "comment from user to event successfully"
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404

@action_bp.route('/comment', methods=['DELETE'])
def delete_comment():
    try:
        data = request.get_json()
        if 'comment_id' not in data:
            return jsonify({"message": "comment_id is required"}), 400

        comment_id = data['comment_id']
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return jsonify({"message": "Comment deleted successfully"}), 200
        else:
            return jsonify({"message": "Comment not found."}), 404
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@action_bp.route('/subscribe/<eid>', methods=['POST'])
@jwt_required() 
def subscribe(eid):
    identity = get_jwt_identity()
    user_id = identity.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID not found in token."}), 400
    
    event_organizer = EventOrganizer.query.get(eid)
    if not event_organizer:
        return jsonify({"message": f"Event Organizer with ID {eid} not found."}), 404
    
    user = User.query.get(user_id)    
    if user:
        existing_follow = Follow.query.filter_by(follower_id =user_id, followed_eo_id =eid).first()    
        if existing_follow:
            db.session.delete(existing_follow)
            message = "Follow removed from user to event successfully"
        else:
            follow = Follow(
                follower_id=user_id,
                followed_eo_id =eid,
                created_at=datetime.now()
            )
            db.session.add(follow)
            message = "follow from user to event organizer added successfully"
        db.session.commit()
        return jsonify({
            "message": message
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
            "message": "reported successfully"
        }), 200
    else:
        return jsonify({"message": "User not found."}), 404
