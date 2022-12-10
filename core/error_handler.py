from . import app, jwt
from flask import jsonify

# Custom JWT Response
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'code': 401,
        'status': 'ERROR',
        'data': [
            {'error': 'The token has expired'}
        ]
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(invalid_token):
    return jsonify({
        'code': 422,
        'status': 'ERROR',
        'data': [
            {'error': 'Signature verification failed'}
        ]
    }), 422


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({
        'code': 413,
        'status': 'ERROR',
        'data': [
            {'error': 'File too large'}
        ]
    }), 413
