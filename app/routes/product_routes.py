from flask import Blueprint, request, jsonify
from app.services.product_service import ProductService
from app.dto.product_dto import ProductDTO
from utils.decorators import jwt_required

product_blueprint = Blueprint('product_routes', __name__)
service = ProductService()
schema = ProductDTO()

from flask import jsonify, request
from flasgger import swag_from
from werkzeug.exceptions import NotFound, BadRequest

@product_blueprint.route("/products", methods=["GET"])
@swag_from({
    'tags': ['Products'],
    'responses': {
        200: {
            'description': 'Список продуктов',
            'schema': {
                'type': 'array',
                'items': {
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'amount': {'type': 'integer'},
                        'user_id': {'type': 'integer'}
                    }
                }
            }
        },
        404: {'description': 'Продукты не найдены'}
    }
})
@jwt_required
def get_products():
    try:
        products = service.get_products()
        return jsonify(schema.dump(products, many=True))
    except NotFound as e:
        return jsonify({'error': str(e)}), 404


@product_blueprint.route("/products/<int:product_id>", methods=["GET"])
@swag_from({
    'tags': ['Products'],
    'parameters': [
        {
            'name': 'product_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID продукта'
        }
    ],
    'responses': {
        200: {
            'description': 'Данные продукта',
            'schema': {
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'amount': {'type': 'integer'},
                    'user_id': {'type': 'integer'}
                }
            }
        },
        404: {'description': 'Продукт не найден'}
    }
})
@jwt_required
def get_product(product_id):
    try:
        product = service.get_product(product_id)
        return jsonify(schema.dump(product))
    except NotFound as e:
        return jsonify({'error': str(e)}), 404


@product_blueprint.route("/products", methods=["POST"])
@swag_from({
    'tags': ['Products'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'amount': {'type': 'integer'},
                    'user_id': {'type': 'integer'}
                },
                'required': ['name', 'amount', 'user_id']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Продукт создан',
            'schema': {
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'amount': {'type': 'integer'}
                }
            }
        },
        400: {'description': 'Невалидные данные'}
    }
})
@jwt_required
def create_product():
    try:
        data = schema.load(request.json)
        product = service.create_product(data)
        return jsonify(schema.dump(product)), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400


@product_blueprint.route("/products/<int:product_id>", methods=["PUT"])
@swag_from({
    'tags': ['Products'],
    'parameters': [
        {
            'name': 'product_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID продукта'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'name': {'type': 'string'},
                    'amount': {'type': 'integer'},
                    'user_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Данные продукта обновлены',
            'schema': {
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'amount': {'type': 'integer'}
                }
            }
        },
        400: {'description': 'Невалидные данные'},
        404: {'description': 'Продукт не найден'}
    }
})
@jwt_required
def update_product(product_id):
    try:
        data = schema.load(request.json)
        product = service.update_product(product_id, data)
        return jsonify(schema.dump(product))
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except NotFound as e:
        return jsonify({'error': str(e)}), 404


@product_blueprint.route("/products/<int:product_id>", methods=["DELETE"])
@swag_from({
    'tags': ['Products'],
    'parameters': [
        {
            'name': 'product_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID продукта'
        }
    ],
    'responses': {
        204: {'description': 'Продукт удален'},
        404: {'description': 'Продукт не найден'}
    }
})
@jwt_required
def delete_product(product_id):
    try:
        service.delete_product(product_id)
        return '', 204
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
