from flask import jsonify
from http import HTTPStatus as status
from app import jwt


@jwt.unauthorized_loader
def no_token():
    return (
        jsonify({"message": "Authentication needed for this action"}),
        status.UNAUTHORIZED,
    )


@jwt.invalid_token_loader
def invalid_token(token):
    return (
        jsonify({"message": "Authentication needed for this action"}),
        status.UNAUTHORIZED,
    )


@jwt.expired_token_loader
def on_token_expired(exp_token):
    return (
        jsonify({"message": "Your session expired. Login again"}),
        status.UNAUTHORIZED,
    )
