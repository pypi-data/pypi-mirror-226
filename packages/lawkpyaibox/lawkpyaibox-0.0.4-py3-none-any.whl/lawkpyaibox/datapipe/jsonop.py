import json


def save_json(filepath, jdata, ensure_ascii=False):
    with open(filepath, 'w') as file:
        json.dump(jdata, file, ensure_ascii=ensure_ascii)


def load_json(filepath):
    with open(filepath, 'r') as file:
        jdata = json.load(file)
    return jdata


def load_json_line(filepath, process_callback: callable):
    with open(filepath, 'r') as file:
        for line in file:
            process_callback(json.loads(line))
