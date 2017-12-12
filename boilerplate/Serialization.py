import dicttoxml
import xmltodict

from models.WordFrequency import WordFrequency
from models.TfIdfResult import TfIdfResult


def get_dict(input):
    result = {}
    if hasattr(input, '__dict__'):
        result = input.__dict__
    elif isinstance(input, list):
        i = 0
        for item in input:
            result[str(i)] = get_dict(item)
            i += 1
        f = 10
        pass
    result["type"] = type(input).__name__
    return result


def process_dict(input):
    if not isinstance(input, str):
        type_attr = input["@type"]
        if type_attr:
            if type_attr == "dict":
                for key in input.keys():
                    input[key] = process_dict(input[key])
            elif type_attr == "float":
                return float(input["#text"])
            elif type_attr == "int":
                return int(input["#text"])
            elif type_attr == "str":
                return input["#text"]
    return input

def get_obj(input):
    type = input["type"]
    if not isinstance(type, str):
        type = type["#text"]
    if type == "list":
        result = []
        for key, value in input.items():
            if key == "type":
                continue
            result.append(get_obj(value))
    else:
        klass = globals()[type]
        result = klass()
        result.__dict__ = process_dict(input)

    return result


def serialize(sequence, file_path):
    dict = get_dict(sequence)
    xml = dicttoxml.dicttoxml(dict)
    with open(file_path, 'w') as file:
        file.writelines(str(xml,'utf-8'))


def deserialize(file_path):
    with open(file_path, 'rb') as file:
        # xml = file.read()
        # dict = xmltodict.parse(xml)["root"]
        dict = xmltodict.parse(file)["root"]
        return get_obj(dict)
