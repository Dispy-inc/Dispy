import json
import os

def load_json_data(file_name):
    """Load JSON data from a file with error handling."""
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

# Usage
intents = load_json_data('intents.json')
errors = load_json_data('errors.json')