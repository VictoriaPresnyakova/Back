from app.dto.user_dto import UserDTO
from flask import Blueprint, jsonify, request
from app.services.user_service import UserService
from flasgger.utils import swag_from
from werkzeug.exceptions import NotFound, BadRequest

user_blueprint = Blueprint('user_routes', __name__)
service = UserService()
schema = UserDTO()



@user_blueprint.route("/users", methods=["GET"])
@swag_from({
    'tags': ['Users'],
    'responses': {
        200: {
            'description': 'Список пользователей',
            'schema': {
                'type': 'array',
                'items': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'email': {'type': 'string'},
                        'jwt_token': {'type': 'string'}
                    }
                }
            }
        },
        404: {'description': 'Пользователи не найдены'}
    }
})
def get_users():
    try:
        users = service.get_users()
        return jsonify(schema.dump(users, many=True))
    except NotFound as e:
        return jsonify({'error': str(e)}), 404


@user_blueprint.route("/users/<int:user_id>", methods=["GET"])
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID пользователя'
        }
    ],
    'responses': {
        200: {
            'description': 'Данные пользователя',
            'schema': {
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'jwt_token': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Пользователь не найден'}
    }
})
def get_user(user_id):
    try:
        user = service.get_user(user_id)
        return jsonify(schema.dump(user))
    except NotFound as e:
        return jsonify({'error': str(e)}), 404


@user_blueprint.route("/users", methods=["POST"])
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'jwt_token': {'type': 'string'}
                },
                'required': ['name', 'email']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Пользователь создан',
            'schema': {
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Невалидные данные'}
    }
})
def create_user():
    try:
        data = schema.load(request.json)
        user = service.create_user(data)
        return jsonify(schema.dump(user)), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400


@user_blueprint.route("/users/<int:user_id>", methods=["PUT"])
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID пользователя'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'jwt_token': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Данные пользователя обновлены',
            'schema': {
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'email': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Невалидные данные'},
        404: {'description': 'Пользователь не найден'}
    }
})
def update_user(user_id):
    try:
        data = schema.load(request.json)
        user = service.update_user(user_id, data)
        return jsonify(schema.dump(user))
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except NotFound as e:
        return jsonify({'error': str(e)}), 404


@user_blueprint.route("/users/<int:user_id>", methods=["DELETE"])
@swag_from({
    'tags': ['Users'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID пользователя'
        }
    ],
    'responses': {
        204: {'description': 'Пользователь удален'},
        404: {'description': 'Пользователь не найден'}
    }
})
def delete_user(user_id):
    try:
        service.delete_user(user_id)
        return '', 204
    except NotFound as e:
        return jsonify({'error': str(e)}), 404