import json
from jsonpath import jsonpath


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
            def process_callback(line, result):
                jdata = json.loads(line)
                print(jdata)
                input = jdata["input"].replace("user:", "")
                output = jdata["output"].replace("assistant:", "")
                instruction = jdata.get("instruction", "")
                system_preprompt = "你是一个智能助手。"
                messages = [{"user": input, "assistant": output}]
                jitem = {"system": system_preprompt + instruction, "messages": messages}
                result jitem
    Args:
        filepath (_type_): _description_
        process_callback (_type_): _description_
    """
    datas = []
    with open(filepath, 'r') as file:
        for line in file:
            data = process_callback(line, kwargs)
            datas.append(data)
    return datas


def search_jsonkey(jdata, key):
    template = "$..{}".format(key)
    values = jsonpath(jdata, template)
    if values is False or len(values) == 0:
        return None
    return values
