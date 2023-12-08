import os
import json


folder1_path = 'C:\\Users\\tjufe\\Desktop\\数据\\json'


folder2_path = 'C:\\Users\\tjufe\\Desktop\\数据\\QA'

def compare_filepath(path1,path2):
    len1, len2 = len(path1), len(path2)
    min_len = min(len1, len2)
    similarity = sum([1 for i in range(min_len) if path1 == path2]) / min_len
    return similarity >= 0.85

def compare_content(json1, json2):
    content1 = json1['content']
    content2 = json2['相关信息']
    if not content1 or not content2:
        return False
    len1, len2 = len(content1), len(content2)
    if len1 == 0 or len2 == 0:
        return False
    min_len = min(len1, len2)
    similarity = sum([1 for i in range(min_len) if content1[i] == content2[i]]) / min_len
    return similarity >= 0.85

for root, dirs, files in os.walk(folder1_path):
    for file in files:
        if file.endswith('.json'):
            file1_path = os.path.join(root, file)
            with open(file1_path, 'r', encoding = 'UTF-8') as f:
                data1 = json.load(f)
            
            for root2, dirs2, files2 in os.walk(folder2_path):
                for file2 in files2:
                    if file2.endswith('.json'):
                        file2_path = os.path.join(root2, file2)
                        with open(file2_path, 'r', encoding='UTF-8') as f:
                            data2 = json.load(f)

                        
                        for obj1 in data1:
                            for obj2 in data2:
                                if compare_filepath(file1_path,file2_path):
                                    if compare_content(obj1, obj2):
                                        obj2['id'] = obj1['id']


                        with open(file2_path, 'w',encoding='UTF-8') as f:
                            json.dump(data2, f, indent = 4, ensure_ascii = False)
