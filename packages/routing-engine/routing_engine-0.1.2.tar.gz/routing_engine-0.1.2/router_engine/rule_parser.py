import json
import jsonschema
import os


# Get the directory of the current Python file
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the JSON file
schema_file_path = os.path.join(current_directory, 'schema.json')

with open(schema_file_path) as f:
    schema = json.load(f)

def validate_json(json_data):
    try:
        jsonschema.validate(json_data, schema)
        print("JSON rules are valid")
        return True
    except Exception as e:
        print("JSON rules are not valid:", e)
        False

def load_rules_from_file(file_path='rules.json'):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        if validate_json(json_data):
            return json_data
        else:
            raise Exception("Invalid JSON file or schema mismatch")

def load_rules_from_json(json_data):
    if validate_json(json_data):
            return json_data
    else:
        raise Exception("Invalid JSON file or schema mismatch")
    


