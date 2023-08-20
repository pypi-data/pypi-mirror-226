import json
import pprint

def to_dict(apispec_object):
    string_object = json.dumps(apispec_object)
    return json.loads(string_object)
