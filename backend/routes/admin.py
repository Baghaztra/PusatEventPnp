from flask import Blueprint, request, jsonify, render_template
from flask_mail import Message
from models import EventOrganizer, User, Report, Event
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
            "username": eo.username, 
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
        message = message = request.json.get('message') or f"{user.username} is {user.status}"
        db.session.commit()

        sendEmail([user.email], message, role, user.status)
        return jsonify({"message": message}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro: {e}")
        return jsonify({"message": "Failed to"}), 500

@admin_bp.route('/role-admin', methods=['PATCH'])
def role_admin():
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"message": "Valid ID is required"}), 404
    
    user = User.query.get(user_id) 
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    try:
        if user.role == 'admin':
            user.role = 'user'
        else:
            user.role = 'admin'
        msg =  f"{user.username} is now {user.role} of Pusat Event"
        db.session.commit()

        sendEmail([user.email], msg, user.role, user.status)
        return jsonify({"message": msg}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erro: {e}")
        return jsonify({"message": "Failed to"}), 500

@admin_bp.route('/reports', methods=['GET', 'DELETE'])
def reports():
    if request.method == 'GET':
        reports = Report.query.order_by(Report.created_at)
        
        reportList = []
        for report in reports:
            reported_by = User.query.get(report.reported_by_id)

            valid = True
            if report.reported_type == 'eo':
                reported = EventOrganizer.query.get(report.reported_id)
                reported_data = {
                    "id": reported.id,
                    "name": reported.username,
                    "email": reported.email
                } if reported else None
            elif report.reported_type == 'user':
                reported = User.query.get(report.reported_id)
                reported_data = {
                    "id": reported.id,
                    "name": reported.username,
                    "email": reported.email
                } if reported else None
            elif report.reported_type == 'event':
                reported = Event.query.get(report.reported_id)
                reported_data = {
                    "id": reported.id,
                    "name": reported.title,
                    "email": ""
                } if reported else None
            else:
                reported_data = None

            data = {
                "id": report.id,
                "reported_by": {
                    "id": reported_by.id,
                    "username": reported_by.username,
                    "email": reported_by.email
                } if reported_by else None,
                "reported": reported_data,
                "reported_type": report.reported_type,
                "message": report.reason,
                "created_at": report.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            if data["reported_by"] == None:
                valid = False
            if reported_data != None and valid :
                reportList.append(data)

        return jsonify(reportList), 200

    
    elif request.method == 'DELETE' and 'id' in request.args:
        report = Report.query.get(request.args['id'])
        if report:
            similar_reports = Report.query.filter_by(
                reported_id=report.reported_id,
                reported_type=report.reported_type
            ).all()
            
            for similar_report in similar_reports:
                db.session.delete(similar_report)
            db.session.commit()
            return jsonify({"message": "Report deleted successfully."}), 200
        return jsonify({"message": "Report not found."}), 404

    return jsonify({"message": "Something went wrong :("}), 404