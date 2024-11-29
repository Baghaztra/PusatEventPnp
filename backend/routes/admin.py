from flask import Blueprint, request, jsonify, render_template
from flask_mail import Message
from models import EventOrganizer, User
from app import db, mail

admin_bp = Blueprint('admin', __name__)

def sendEmail(recipients, msg_body, role, status='Active'):
    msg = Message(
        "No Reply",
        sender="noreply@app.com",
        recipients=recipients
    )
    data = {
        'title': "Pusat Event Politeknik",
        'message': msg_body,
        'goto': "",
        'goto_msg': "Login",
    }
    if status == 'Active':
        if role == 'event organizer':
            data['goto'] = 'http://localhost:8080/eo-login'
        else:
            data['goto'] = 'http://localhost:8080/login'

    # Kirim data sebagai variabel template
    msg.html = render_template("info.html", **data)

    try:
        mail.send(msg)
        return {"message": "Email sent successfully."}
    except Exception as e:
        print(f"Email Error: {e}")
        raise

@admin_bp.route('/eo-requested', methods=['GET'])
def requested_eo():
    waiting_eos = EventOrganizer.query.filter_by(status='Waiting Admin').order_by(EventOrganizer.created_at.desc()).all()
    
    eo_list = [
        {
            "id": eo.id, 
            "name": eo.name, 
            "logo": eo.profile_picture, 
            "bio": eo.bio, 
            "created_at": eo.created_at
        } for eo in waiting_eos
    ]
    return jsonify(eo_list), 200

@admin_bp.route('/eo-approve', methods=['PATCH'])
def approve_eo():
    eo_id = request.json.get('id')
    if not eo_id:
        return jsonify({"error": "Valid ID is required"}), 400
    
    eo = EventOrganizer.query.get(eo_id)
    if not eo:
        return jsonify({"error": "EventOrganizer not found"}), 404

    try:
        eo.status = 'Active'
        db.session.commit()

        sendEmail([eo.email], "Your Account Has Been Approved", 'event organizer')
        return jsonify({"message": f"{eo.username} has been approved"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Approval Error: {e}")
        return jsonify({"message": "Failed to approve EO"}), 500

@admin_bp.route('/ban', methods=['PATCH'])
def ban():
    user_id = request.json.get('user_id')
    role = request.json.get('role')
    
    if not user_id:
        return jsonify({"message": "Valid ID is required"}), 404
    
    if role == "event organizer":
        user = EventOrganizer.query.get(user_id)
    else:
        user = User.query.get(user_id)
        
    if not user:
        return jsonify({"message": "User not found"}), 404
    try:
        if user.status == 'Banned':
            user.status = 'Active'
        else:
            user.status = 'Banned'
        msg =  f"{user.username} has been {user.status}"
        db.session.commit()

        sendEmail([user.email], msg, role, user.status)
        return jsonify({"message": msg}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro: {e}")
        return jsonify({"message": "Failed to"}), 500
