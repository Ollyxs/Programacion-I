from .. import jwt
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] == "admin":
            return fn(*args, **kwargs)
        else:
            return 'Only admins can access', 403
    return wrapper


def provider_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] == "proveedor":
            return fn(*args, **kwargs)
        else:
            return 'Only proveedor can access', 403
    return wrapper


def client_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] == "cliente":
            return fn(*args, **kwargs)
        else:
            return 'Only cliente can access', 403
    return wrapper


def admin_client_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] == "admin" or claims['role'] == "cliente":
            return fn(*args, **kwargs)
        else:
            return 'Only admins and clients can access', 403
    return wrapper


def admin_provider_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] == "admin" or claims['role'] == "proveedor":
            return fn(*args, **kwargs)
        else:
            return 'Only admins and providers can access', 403
    return wrapper


@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return usuario.id


@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        'role': usuario.role,
        'id': usuario.id,
        'email': usuario.email
    }
    return claims
