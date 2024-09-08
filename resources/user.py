from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

from utils import hash_password
from models.user import User


class UserListResource(Resource):
    @jwt_required()
    def get(self):
        id = get_jwt_identity()
        user = User.get_by_id(id)
        return user.data(), HTTPStatus.OK
        
        
    def post(self):
        json_data = request.get_json()

        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')
        group = json_data.get('group')
        password = hash_password(non_hash_password)


        if User.get_by_username(username):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST


        if User.get_by_email(email):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST


        user = User(
            username=username,
            email=email,
            password=password
        )
        
        if group:
            if len(group)>1:
                for g in group:
                    user.add_to_group(g)
            else:
                user.add_to_group(group[0])

        user.save()

        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
        return data, HTTPStatus.CREATED
