import time
import openai
import json
import os
import csv
import re

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)  # for exponential backoff

@retry(
    retry=retry_if_exception_type((openai.error.APIError, openai.error.APIConnectionError, openai.error.RateLimitError, openai.error.ServiceUnavailableError, openai.error.Timeout)),
    wait=wait_random_exponential(multiplier=1, max=60),
    stop=stop_after_attempt(10)
)

def csv_to_json(csv_file_path,json_file_path,fieldnames):
    csv_file=open(csv_file_path,'r',encoding='UTF-8')
    json_file=open(json_file_path,'w',encoding='UTF-8')
    reader=csv.DictReader(csv_file,fieldnames)
    out=json.dumps([row for row in reader],ensure_ascii=False, indent=4)
    json_file.write(out)

def summary(api_key,json_file_path,summary_file_path,k=0):
    openai.api_key = api_key
    fieldnames=("course_name","teacher","comment")
    # csv_to_json(csv_file_path,json_file_path,fieldnames)
    with open(json_file_path,"r",encoding="UTF-8") as f:
        data=json.load(f)
        for i in range(k,len(data),4):
            text_1=data[i]["content"]
            text_2=data[i+1]["content"]
            text_3 = data[i+2]["content"]
            text_4 = data[i + 3]["content"]
            if len(text_3)*len(text_4)!=0:
                prompt = f"你是一个提问者，根据{text_1}、{text_2}、{text_3}、{text_4}这4条与教师有关的信息，用一个问题提问这4个老师的办公电话，要求提问中包含4个老师的姓名，并给出回答。格式为“问”，”答“"
                message = [{"role": "assistant", "content": prompt}]
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=message,
                    temperature=0.8,
                    max_tokens=800,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=1.0
                )
                response = completion.choices[0].message["content"]
            print(f"response is {response}")
            if "\n\n" or "\n" in response:
                split_response = re.split("\n\n|\n", response)
            for j in range(int(len(split_response) / 2)):
                if split_response[2 * j][:2] == "问：" and split_response[2 * j + 1][:2] == "答：":
                    save=open(summary_file_path,'w',encoding='utf-8')
                    with open(summary_file_path, "r", encoding="utf-8") as s:
                        size = os.path.getsize(summary_file_path)
                        if size == 0:
                            new_data = []
                        else:
                            new_data = json.load(s)
                        new_data.append({"问": split_response[2 * j][2:], "答": split_response[2 * j + 1][2:],
                                         "相关信息1": text_1, "相关信息2": text_2,"相关信息3": text_3, "相关信息4": text_4,"id1": data[i]["id"],
                                        "id2": data[i + 1]["id"],"id3": data[i + 2]["id"],"id4": data[i + 3]["id"]})
                        print(f"共成功写入{len(new_data)}条")
                        json.dump(new_data, save, indent=1, ensure_ascii=False)
            time.sleep(10)
if __name__ == "__main__":
    summary(api_key=" ",json_file_path=" ",summary_file_path=" ")

