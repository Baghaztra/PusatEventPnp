from flask import Flask,request,jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from models import *

def register_route(app, db):
    @app.route('/')
    def index():
        return "Bisa, bang :D"
    
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        user = User.query.filter_by(email=email).first()
        
        # jika ada user yang dicari, dan passwornya benar
        if user and user.verify_password(password):
            # Buat JWT token dengan informasi user_id
            access_token = create_access_token(identity={'user_id': user.id, 'username': user.username})
            return jsonify({"message": "Invalid email or password.", "token":access_token}), 200
        else:
            return jsonify({"message": "Invalid email or password."}), 401
    
    @app.route('/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return jsonify({"access_token": new_access_token}), 200
    
    @app.route('/event-latest')
    def event_latest():
        # Mendapatkan parameter halaman (page) dari query string, default 1 jika tidak ada
        page = request.args.get('page', 1, type=int)
        # Mendapatkan parameter jumlah item per halaman (per_page) dari query string, default 5
        per_page = request.args.get('per_page', 5, type=int)

        # Mengambil data event secara paginated
        events = Event.query.order_by(Event.created_at.desc()).paginate(page=page, per_page=per_page)

        # Mengonversi data event ke dalam list dictionary
        events_list = [
            {
                "id": event.id,
                "title": event.title,
                "images": [image.path for image in event.images],
                "description": event.description,
                "event_date": event.start_date,
                "created_at": event.created_at
            }
            for event in events.items
        ]

        # Mengembalikan JSON dengan informasi data event serta info pagination
        return jsonify({
            "total": events.total,  # Total semua data yang ada di database
            "pages": events.pages,  # Total halaman yang tersedia
            "current_page": events.page,  # Halaman saat ini
            "per_page": events.per_page,  # Jumlah item per halaman
            "has_next": events.has_next,  # Apakah ada halaman berikutnya
            "has_prev": events.has_prev,  # Apakah ada halaman sebelumnya
            "events": events_list  # Data event pada halaman saat ini
        }), 200
