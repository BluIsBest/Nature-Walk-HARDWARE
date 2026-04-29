import json
import os

def append_to_json(file_path, new_entry):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
    else:
        data = []

    data.append(new_entry)

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
