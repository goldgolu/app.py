# database/migrations.py
from database import db

def migrate():
    db.create_all()
