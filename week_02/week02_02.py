import json
from functools import wraps


def to_json(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)

        return json.dumps(result)

    return wrapped


@to_json
def get_data():
    return {
        'data': 42
    }


if __name__ == '__main__':
    get_data()
