import json


def save_json(filepath, jdata, ensure_ascii=False):
    with open(filepath, 'w') as file:
        json.dump(jdata, file, ensure_ascii=ensure_ascii)


def load_json(filepath):
    with open(filepath, 'r') as file:
        jdata = json.load(file)
    return jdata


def load_json_line(filepath, process_callback, **kwargs):
    """_summary_
        Example: 
            def process_callback(line, jdatas):
                print(line)
                jdata = json.loads(line)
                item = jdata['translation']
                query = "user: " + item["input"]
                answer = "assistant: " + item["output"]
                jitem = {
                    "instruction": item["instruction"],
                    "input": query,
                    "output": answer
                }
                jdatas.append(jitem)
    Args:
        filepath (_type_): _description_
        process_callback (_type_): _description_
    """
    with open(filepath, 'r') as file:
        for line in file:
            process_callback(line, kwargs)