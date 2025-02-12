# database/seed.py
from database import db
from database.models import User

def seed_data():
    user1 = User(username='player1', coins=100, level=5)
    user2 = User(username='player2', coins=200, level=10)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()
