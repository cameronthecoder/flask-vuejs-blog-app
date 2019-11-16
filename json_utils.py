from flask.json import JSONEncoder
from flask import g, request, redirect, url_for, jsonify
from datetime import date
from functools import wraps

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)



def verify_parameters(keys):
    "This function checks the JSON request keys and make's sure the required keys are in the body."
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.is_json:
                json = request.get_json()
                errors = []
                for key in keys:
                    if key not in json or len(json[key]) <= 0:
                        errors.append({f'{key.title()} is required'})
                if errors:
                    return jsonify({'errors': errors})
            return f(*args, **kwargs)
        return decorated_function
    return decorator