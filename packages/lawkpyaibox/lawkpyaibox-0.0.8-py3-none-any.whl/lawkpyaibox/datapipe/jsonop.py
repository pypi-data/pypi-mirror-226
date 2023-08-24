import json
from jsonpath import jsonpath
import os


def save_json(filepath, jdata, seperate_num=1, ensure_ascii=False):

    def dumpjson(filepath, jdata):
        with open(filepath, 'w') as file:
            json.dump(jdata, file, ensure_ascii=ensure_ascii)

    if seperate_num == 1:
        dumpjson(filepath, jdata)
    else:
        jsavedatas = []
        num = len(jdata) // seperate_num
        fileidx = 0
        filebasename = os.path.basename(filepath).split(".")[0]
        dirname = os.path.dirname(filepath)
        for idx, item in enumerate(jdata):
            jsavedatas.append(item)
            if idx % num == 0 and idx != 0:
                savepath = "{}/{}_{}.json".format(dirname, filebasename,
                                                  fileidx)
                dumpjson(savepath, jsavedatas)
                jsavedatas = []
                fileidx = fileidx + 1

        if len(jsavedatas) > 0:
            savepath = "{}/{}_{}.json".format(dirname, filebasename, fileidx)
            dumpjson(savepath, jsavedatas)


def load_json(filepath):
    with open(filepath, 'r') as file:
        jdata = json.load(file)
    return jdata


def load_json_line(filepath, process_callback, **kwargs):
    """_summary_: 按行读取json数据
        Example: 
            def process_callback(line, params):
                jdata = json.loads(line)
                print(jdata)
                input = jdata["input"].replace("user:", "")
                output = jdata["output"].replace("assistant:", "")
                instruction = jdata.get("instruction", "")
                system_preprompt = "你是一个智能助手。"
                messages = [{"user": input, "assistant": output}]
                jitem = {"system": system_preprompt + instruction, "messages": messages}
                return jitem

            filepath = "ChineseWebNovel/novelset.jsonl"
            jdatas = lawkpyaibox.load_json_line(filepath, process_callback, params={})
    Args:
        filepath (_type_): 数据文件路径
        process_callback (_type_): callback函数，用于处理每一行数据，需要返回
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
