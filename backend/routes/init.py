from routes.login import login_bp
from routes.data import data_bp
from routes.eo import eo_bp

def register_route(app):
    @app.route('/')
    def index():
        return "Servernya dah jalan"
    
    app.register_blueprint(login_bp)
    app.register_blueprint(data_bp)
    app.register_blueprint(eo_bp)