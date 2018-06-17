#../models.py

from project import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text)

    def __init__(self, email ):
        self.email = email
        