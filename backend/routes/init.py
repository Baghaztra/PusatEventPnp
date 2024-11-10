from routes.login import login_bp
from routes.data import data_bp

def register_route(app):
    app.register_blueprint(login_bp)
    app.register_blueprint(data_bp)