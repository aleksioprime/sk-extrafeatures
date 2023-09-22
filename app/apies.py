from flask import Flask, request
from flask_restful import Api, Resource
from app import app, db, ma, api
from .models import User

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "last_name", "first_name", "token_dnevnik")
        model = User

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        if 'token_dnevnik' in request.json:
            user.token_dnevnik = request.json['token_dnevnik']
        db.session.commit()
        return user_schema.dump(user)

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')