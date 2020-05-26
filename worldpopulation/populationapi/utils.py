import json

def valid_json(data):
    """
    This assumes the data is json and tries to convert to
    dictionary and return it if valid else return None
    """
    try:
        valid_data = json.loads(data)
    except ValueError:
        valid_data = None
    return valid_data