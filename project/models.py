#../models.py

from project import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)

    def __init__(self, name, email ):
        self.name = name
        self.email = email
        
class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    item_decription = db.Column(db.Text)

    def __init__(self, item_name, item_description ):
        self.item_name = name
        self.item_decription = email

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    

    def __init__(self,category ):
        self.name = category
       
                        