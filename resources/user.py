from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.user import UserSchema
from marshmallow import ValidationError

user_schema = UserSchema(exclude=('created_at', 'updated_at', 'is_active'))
user_public_schema = UserSchema(exclude=('email', 'is_active'))


class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()

        try:
            data = user_schema.load(data= json_data)
        except ValidationError as error:
            return {
                'message': 'Validation error',
                'errors': error.messages
            }, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST
        
        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        
        
        user = User(**data) 

        user.save()     

        return {}, HTTPStatus.CREATED 