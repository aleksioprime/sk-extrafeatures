from app import db

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    last_name = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    authenticated = db.Column(db.Boolean, default=False)
    def get_id(self):
        return self.username
    def is_authenticated(self):
        return self.authenticated

