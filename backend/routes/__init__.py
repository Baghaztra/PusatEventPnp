from routes.login import login_bp
from routes.admin import admin_bp
from routes.data import data_bp
from routes.eo import eo_bp
from flask import send_from_directory, current_app
import os

def register_route(app):
    @app.route('/')
    def index():
        return "Running abangkuh"

    @app.route('/uploads/<foldername>/<filename>')
    def uploaded_file(filename, foldername):
        return send_from_directory(os.path.join(current_app.config['UPLOAD_FOLDER'], foldername), filename)
    
    app.register_blueprint(login_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(eo_bp)