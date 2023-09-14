import os

# export DATABASE_URL=postgresql://postgres:docker@localhost:5432/olympiad
# set export DATABASE_URL='sqlite:///database.db'
class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(36)