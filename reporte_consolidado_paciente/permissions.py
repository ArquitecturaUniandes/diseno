from functools import wraps
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request


def funcionario_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("is_funcionario", False):
                return fn(*args, **kwargs)
            else:
                return dict(msg="Acceso denegado!"), 403

        return decorator

    return wrapper
