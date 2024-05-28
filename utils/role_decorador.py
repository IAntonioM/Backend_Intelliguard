from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if 'rol' not in claims or role not in claims['rol']:
                return jsonify({"msg": "No tienes permiso para acceder a esta ruta"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator