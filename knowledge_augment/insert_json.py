from get_embedding import get_embedding
import json
import os
import sys
import numpy as np
def write_list_to_json(list, json_file_name, json_file_save_path):
    """
    将list写入到json文件
    :param list:
    :param json_file_name: 写入的json文件名字
    :param json_file_save_path: json文件存储路径
    :return:
    """
    os.chdir(json_file_save_path)
    with open(json_file_name, 'w',encoding='utf-8') as  f:
        json.dump(list, f,indent=4, ensure_ascii=False)


def get_all_files_in_folder(folder_path):
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    return file_paths


folder_path = "D:\\project2\\摘要数据集（清洗） - 副本"
file_paths = get_all_files_in_folder(folder_path)


def Insert_to_json(filepath,divide_length):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        to_json=[]
        target_key = 'abstract'

        for i in data:
            if len(i["content"]) >= 1600:
                    to_json.append({"embedding": get_embedding(i["content"][:1600]).tolist(), "content": i["content"][:1600],"id":i["id"]})
            else:
                    to_json.append({"embedding": get_embedding(i["content"]).tolist(), "content": i["content"],"id":i["id"]})
                  # if len(i["content"]) > 1600:
                  #     to_json.append({"abstract": i["name"], "embedding": get_embedding(i["name"]).tolist(),
                  #                     "content": i["content"][:1600], "id": i["id"]})
                  # else:
                  #     to_json.append({"abstract": i["name"], "embedding": get_embedding(i["name"]).tolist(),
                  #                     "content": i["content"], "id": i["id"]})
    return to_json

data=[]

for path in file_paths:
    data=data+Insert_to_json(path,200)
write_list_to_json(data, "bge-large-zh-v1.5_embedding_content_4.json", "D:\\project2\\daima 1")
print("完成")