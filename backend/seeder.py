from faker import Faker
from app import db, create_app
from models import User, EventOrganizer, Event, Like, Comment, Follow, Image, TemporaryImage, Report
from datetime import datetime
import random

app = create_app()
faker = Faker()

def seed_users(n=10):
    print(f"Seeding {n} users...")
    for _ in range(n):
        user = User(
            username=faker.user_name(),
            email=faker.email(),
            password='password',
            status='Active',
            profile_picture=faker.image_url(),
            role=random.choice(['user', 'admin']),
            created_at=datetime.now()
        )
        db.session.add(user)
    db.session.commit()

def seed_event_organizers(n=5):
    print(f"Seeding {n} event organizers...")
    for _ in range(n):
        eo = EventOrganizer(
            username=faker.user_name(),
            email=faker.email(),
            password=faker.password(),
            status='Active',
            profile_picture=faker.image_url(),
            bio=faker.text(),
            created_at=datetime.now()
        )
        db.session.add(eo)
    db.session.commit()

def seed_events(n=10):
    print(f"Seeding {n} events...")
    eos = EventOrganizer.query.all()
    for _ in range(n):
        event = Event(
            eo_id=random.choice(eos).id,
            title=faker.catch_phrase(),
            description=faker.text(),
            start_date=faker.date_time_this_year(),
            end_date=faker.date_time_this_year(),
            created_at=datetime.now()
        )
        db.session.add(event)
    db.session.commit()

def seed_likes(n=20):
    print(f"Seeding {n} likes...")
    users = User.query.all()
    events = Event.query.all()
    for _ in range(n):
        like = Like(
            user_id=random.choice(users).id,
            event_id=random.choice(events).id,
            created_at=datetime.now()
        )
        db.session.add(like)
    db.session.commit()

def seed_comments(n=20):
    print(f"Seeding {n} comments...")
    users = User.query.all()
    events = Event.query.all()
    for _ in range(n):
        comment = Comment(
            user_id=random.choice(users).id,
            event_id=random.choice(events).id,
            content=faker.sentence(),
            created_at=datetime.now()
        )
        db.session.add(comment)
    db.session.commit()

def run_seeders():
    with app.app_context():
        seed_users()
        seed_event_organizers()
        seed_events()
        seed_likes()
        seed_comments()
        print("Seeding complete.")

if __name__ == '__main__':
    run_seeders()
