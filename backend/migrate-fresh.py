from app import db, create_app
from flask_migrate import upgrade

app = create_app()

def reset_database():
    with app.app_context():
        # db telah diimport dari app.py
        db.drop_all() 
        db.create_all()  
        upgrade()  

if __name__ == '__main__':
    reset_database()
    print("Database dah ke-reset, bang :D.")
