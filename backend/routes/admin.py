from flask import Blueprint, request, jsonify
from models import EventOrganizer  # Pastikan model `EventOrganizer` sudah didefinisikan dengan atribut yang diperlukan
from app import db

admin_bp = Blueprint('admin', __name__)

# Endpoint untuk mendapatkan EO yang masih waiting
@admin_bp.route('/eo-requested', methods=['GET'])
def requested_eo():
    # Mengambil daftar EO dengan status 'waiting'
    waiting_eos = EventOrganizer.query.filter_by(status='Waiting').order_by(EventOrganizer.created_at.desc()).all()
    
    # Serialisasi hasil query ke dalam format JSON
    eo_list = [{"id": eo.id, "name": eo.name, "created_at": eo.created_at} for eo in waiting_eos]
    return jsonify(eo_list), 200

# Endpoint untuk menyetujui (approve) EO
@admin_bp.route('/eo-approve', methods=['PATCH'])
def approve_eo():
    # Mendapatkan ID dari permintaan
    eo_id = request.json.get('id')
    if not eo_id:
        return jsonify({"error": "ID is required"}), 400
    
    # Cari EO berdasarkan ID
    eo = EventOrganizer.query.get(eo_id)
    if not eo:
        return jsonify({"error": "EventOrganizer not found"}), 404
    
    # Ubah status menjadi "active"
    eo.status = 'Active'
    
    # Simpan perubahan ke database
    db.session.commit()
    return jsonify({"message": f"EventOrganizer {eo_id} has been approved"}), 200
