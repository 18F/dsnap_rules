import json

from functools import wraps


def json_request(view_func):
    @wraps(view_func)
    def wrapper_json_request(request, *args, **kwargs):
        if request.content_type == 'application/json':
            request.json = json.loads(request.body)
        else:
            request.json = None
        return view_func(request, *args, **kwargs)
    return wrapper_json_request
