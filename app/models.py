from app import db, bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String)
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    authenticated = db.Column(db.Boolean, default=False)
    def get_id(self):
        return self.id
    def is_authenticated(self):
        return self.authenticated

