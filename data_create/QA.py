import re
import time
import openai
import json
import os
import numpy as np

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
def main(k=0):
    openai.api_key = " "

    file = " "
    docu = " "
    data_path = file + "/" + docu
    with open(data_path, "r", encoding="utf-8") as f:
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
    i = 0
    while True:
        save_path = file + "/QA/" + docu
        dirs = file + "/QA"
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        if not os.path.exists(save_path):
            with open(save_path, mode='w', encoding='utf-8') as ff:
                json.dump([], ff, ensure_ascii=False)
        with open(save_path, mode='r', encoding='utf-8') as s:
            size = os.path.getsize(save_path)
            if size == 0:
                new_data = []
            else:
                new_data = json.load(s)
        while len(new_data) >= sum_len[i]:
            i += 1
            if i == len(data):
                break
        info = data[i]["content"]
        prompt = f"依据{info}中的信息，提问群号并给出回答，所有问题的答案都必须存在于给出的信息中。格式为”问：“， ”答“"
        message = [{"role": "assistant", "content": prompt}]
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
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
            if split_response[2*j][:2] == "问：" and split_response[2*j + 1][:2] == "答：":
                with open(save_path, "r", encoding="utf-8") as s:
                    size = os.path.getsize(save_path)
                    if size == 0:
                        new_data = []
                    else:
                        new_data = json.load(s)
                with open(save_path, "w", encoding="utf-8") as save:
                    if len(new_data) < sum_len[i]:
                        new_data.append({"问": split_response[2*j][2:], "答": split_response[2*j + 1][2:], "相关信息": info})
                    print(f"共成功写入{len(new_data)}条")
                    json.dump(new_data, save, indent=1, ensure_ascii=False)
        # 停顿时间
        time.sleep(30)


if __name__ == "__main__":
    main(k=1)