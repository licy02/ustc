import json
import os
from get_dotlist import get_dotlist
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

def read_json_to_list(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        to_list = []
        for i in data:
            to_list.append({"embedding": np.array(i["embedding"]), "content": i["content"],"id":i["id"]})
    return to_list


def read_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def get_all_files_in_folder(folder_path):
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    return file_paths
def get_abs(dotlist,data,value):

        if value== 1000000:
            return "未找到"
        else:
            return data[dotlist[value]["num"]]["abstract"]



def get_value(dotlist,id,data):
    k=1000000
    for i in range(len(dotlist)):
        if id == data[dotlist[i]["num"]]["id"]:
             k=i
    return k

def judgement(QAdata,data):
    rank=[]
    #QAdata=read_json('C:/Users/13153/Desktop/json/领导QA')
    for i in range(len(QAdata)):
        dotlist=get_dotlist(data,QAdata[i]["问"])
        sentence=QAdata[i]["相关信息"]
        id=QAdata[i]["id"]
        value=get_value(dotlist,id,data)
        rank.append({"question":QAdata[i]["问"],"rank_num":value,"information":sentence,"id":id})
    return rank




if __name__ == "__main__":
    data = read_json_to_list('D:\\project2\\daima 1\\bge-large-zh-v1.5_embedding_content_4.json')
    QAdata = read_json("D:\\project2\\preparation\\training_2.json")
    rank=judgement(QAdata,data)
    write_list_to_json(rank,"bge-large-zh-v1.5_embedding_content_training_2.json",'D:\\project2\\results')
    bad_num=0
    bad=[]
    rank_counts = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        1000000: 0
    }

    for i in rank:
        rank_num = i["rank_num"]
        if rank_num in rank_counts:
            rank_counts[rank_num] += 1
        else:
            bad_num += 1
            print(i)
            bad.append(i)


    for rank_num, count in rank_counts.items():
        print(f"Rank {rank_num}: {count} occurrences")

    print(f"Bad ranks: {bad_num}")
    write_list_to_json(bad,"bad_bge-large-zh-v1.5_training_2.json",'D:\\project2\\results')


