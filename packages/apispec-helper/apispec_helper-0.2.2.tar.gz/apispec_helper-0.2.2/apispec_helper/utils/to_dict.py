import json

def to_dict(apispec_object):
    return json.loads(json.dumps(apispec_object))
