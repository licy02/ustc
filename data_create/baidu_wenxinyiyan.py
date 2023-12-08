import requests
import json
import csv
import os
import time
import re
import numpy as np

def get_access_token(api_key,secret_key):
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"%(api_key,secret_key)
    payload = ""
    headers = {'Content-Type': 'application/json','Accept': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    access_token = str(response.json().get("access_token"))
    return access_token

def query(prompt,api_key,secret_key):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token(api_key,secret_key)
    payload = json.dumps({"messages": [{"role": "user","content": prompt}]})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    result = str(response.json().get("result"))
    return result

def summary(api_key,secret_key, json_file_path,save_path,k=0):
    # fieldnames = ("course_name", "teacher", "comment")
    # csv_to_json(csv_file_path, json_file_path, fieldnames)

    with open(json_file_path, "r", encoding="UTF-8") as f:
        data = json.load(f)
        lens = []
        if k == 0:
            for j in range(len(data)):
                t = (int(len(data[j]["content"]) / 50) + 1) * 2
                if t > 10:
                    t = 10
                lens.append(t)
            sum_len = list(np.cumsum(lens))
        else:
            for j in range(len(data)):
                t = k
                lens.append(t)
            sum_len = list(np.cumsum(lens))
        for i in range(k, len(data)):
            info1 = data[i]["content"]
            info2 = data[i+1]["content"]
            info3 = data[i+2]["content"]

            prompt = f"根据{info1}、{info2}、{info3}这3条信息的共同相关内容进行提问,并给出回答。要求:1.所提问题必须与3条信息中的每一条都有关，且在这3条信息中能找到答案2.所有问题两两互不相同，禁止问题重复。格式为”问：“， ”答“"
            response = query(prompt,api_key,secret_key)
            print(f"response is {response}")
            if "\n\n" or "\n" in response:
                split_response = re.split("\n\n|\n", response)
            for j in range(int(len(split_response) / 2)):
                if split_response[2 * j][:2] == "问：" and split_response[2 * j + 1][:2] == "答：":
                    with open(save_path, "r", encoding="utf-8") as s:
                        size = os.path.getsize(save_path)
                        if size == 0:
                            new_data = []
                        else:
                            new_data = json.load(s)
                    with open(save_path, "w", encoding="utf-8") as save:
                        if len(new_data) < sum_len[i]:
                            new_data.append({"问": split_response[2 * j][2:], "答": split_response[2 * j + 1][2:],
                                             "相关信息1": info1, "相关信息2": info2, "相关信息3": info3,
                                             "id1": data[i]["id"], "id2": data[i + 1]["id"],
                                             "id3": data[i + 2]["id"], })
                        print(f"共成功写入{len(new_data)}条")
                        json.dump(new_data, save, indent=1, ensure_ascii=False)
                if i >= len(data)-1 and len(new_data) >= sum_len[i]:
                    flag = False
                    p += 1
                    i = 0
                elif i >= len(data)-1 and len(new_data) < sum_len[i]:
                    i -= 1
                    continue
            continue
if __name__ == '__main__':
    summary(api_key=" ",
            secret_key=" ",
            json_file_path=" ",
            save_path=" ",k= )

