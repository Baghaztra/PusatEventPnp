from app import db, create_app
from flask_migrate import downgrade, upgrade

app = create_app()

def reset_database():
    with app.app_context():
        downgrade(revision="base")
        upgrade()
        
if __name__ == '__main__':
    reset_database()
    print("Database dah ke-reset, bang :D.")
