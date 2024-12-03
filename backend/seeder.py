from faker import Faker
from app import db, create_app
from models import *
from datetime import datetime
import random

app = create_app()
faker = Faker()

def seed_test_user():
    print(f"Seeding test users...")
    user = User(
        username = "Admin",
        email = "admin@example.com",
        password = '1',
        status = 'Active',
        profile_picture = 'https://loremflickr.com/360/360',
        role = 'admin',
        created_at = datetime.now()
    )
    db.session.add(user)
    db.session.commit()
    
def seed_users(n=10):
    print(f"Seeding {n} users...")
    for _ in range(n):
        user = User(
            username=faker.user_name(),
            email=faker.email(),
            password='password',
            status='Active',
            profile_picture = 'https://loremflickr.com/360/360',
            # role=random.choice(['user', 'admin']),
            role='user',
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
            password='password',
            status='Active',
            profile_picture = "https://loremflickr.com/360/360",
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
            poster="https://loremflickr.com/640/360",
            registration_url=faker.url(),
            description=" ".join(faker.paragraphs(5)),
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

def seed_images(n=20):
    print(f"Seeding {n} images...")
    events = Event.query.all()
    for _ in range(n):
        image = Image(
            event_id=random.choice(events).id,
            path= "https://loremflickr.com/360/360",
            created_at=datetime.now()
        )
        db.session.add(image)
    db.session.commit()
    
def seed_follows(n=20):
    print(f"Seeding {n} follows...")
    users = User.query.all()
    eos = EventOrganizer.query.all()
    for _ in range(n):
        follow = Follow(
            follower_id	=random.choice(users).id,
            followed_eo_id=random.choice(eos).id,
            created_at=datetime.now()
        )
        db.session.add(follow)
    db.session.commit()

def run_seeders():
    with app.app_context():
        seed_test_user()
        seed_users()
        seed_event_organizers()
        seed_events()
        seed_likes(100)
        seed_follows(100)
        seed_comments(100)
        seed_images(50)
        print("Seeding complete.")

if __name__ == '__main__':
    run_seeders()
