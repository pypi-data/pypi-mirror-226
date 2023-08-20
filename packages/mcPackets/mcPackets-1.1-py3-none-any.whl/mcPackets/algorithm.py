import json
import os

from mcPackets.packetFile import Recipes

def find_nearest_number(numbers: list, target: int):
    """
    数组临近算法
    """
    nearest_number = None
    min_difference = float('inf')

    for number in numbers:
        difference = abs(number - target)
        if difference < min_difference:
            min_difference = difference
            nearest_number = number

    return nearest_number


def createFile(path: str, data, mode='w'):
    """

    """
    try:
        if os.path.isdir(os.path.dirname(path)) != True:
            os.makedirs(os.path.dirname(path))

        with open(path , mode=mode, encoding='utf-8') as F:
            F.write(data)

        return True, True
    except Exception as f:
        return False, f


def create_folder_with_json_file(file_tree, path_root=''):
    def _(file_tree, path_root=''):
        for folder_name, folder_content in file_tree.items():
            path = os.path.join(path_root, folder_name).replace('\\', '/')
            if type(folder_content) != dict:
                try:
                    content = json.loads(folder_content.replace("'", '"'))
                    content = json.dumps(content, indent=4)
                except Exception as f:
                    content = folder_content

                with open(path, mode='w', encoding='utf-8') as f:
                    f.write(content)  # 写入格式化的json内容

            else:
                if not os.path.exists(path):
                    os.makedirs(path)

                _(folder_content, path_root=path)

    try:
        _(file_tree, path_root)
        return True, True
    except FileNotFoundError as f:
        return False, [FileNotFoundError, "文件错误!", f]
        # raise Exception("文件错误!")


def Recipes_rootLabel(*args):
    def get_label(S: str):
        label_dict = Recipes.label_dict()
        _ = label_dict.get(S)
        return {S: _} if not _ == None else False

    result_dict = {}  # 存储结果的字典
    for arg in args:
        result_dict = {
            **result_dict,
            **get_label(arg)
        }

    return result_dict


def circulate_plate(*args):
    get_label = Recipes.plate

    result_dict = {}  # 存储结果的字典
    for arg in args:
        result_dict = {
            **result_dict,
            **get_label(arg)
        }

    return result_dict

def crafting_catching(func):
    # 声名
    def wrapper(*args, **kwargs):
        result: dict = {
            **func(*args, **kwargs),
            **Recipes.crafting,
            **Recipes_rootLabel('result')
        }

        return result
    return wrapper



def reorder_dict(keys: list, dictionary: dict):
    result = {}
    for key in keys:
        result = {
            **result,
            **dictionary.get(key)
        }
        del dictionary[key]

    return {
        **result,
        **dictionary
    }


def parse_string(string: str, S: str, suffix='.mcfunction'):
    """
    输入: "name/top/mcpot",
    返回
    {
        "name": {
            "top": {
                "mcpot": S
            }
        }
    }
    :param string:
    :param S:
    :return:
    """
    result = {}
    parts = string.split('/')
    current_dict = result

    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            current_dict[f"{part}{suffix}"] = S if S else {}
        else:
            current_dict[part+''] = {}
            current_dict = current_dict[part]

    return result
