## QA.py

The corresponding **openai.api_key** should be used when using it, and unlimited api_key can be used in formal use.

Modifications are required:
**file** = "../knowledge_augment/data/学校"
**docu** = "QQ群（精简版）.json"
**prompt** = f "依据{info}中的信息，提问{lens[i]}并给出回答，所有问题的答案都必须存在于给出的信息中。格式为"问："，"答'"

**lens[i]** sets the number of times a question is asked

If the parameter in main() is 0, then t = (int(len(data[j]["content"]) / 50) + 1) * 2; if t > 10: t = 10;
If it is not 0, K Q&A questions are generated for each piece of data.

## QA_dir_only.py

To process multiple files of the same type in a folder at once.

Modifications are required:

openai.api_key and prompt are the same as before the update, and should be changed according to the actual situation

Added the following parameters:
In the last row, the parameter **dir="address"** in the main function, where address is the folder address

## abstract-create.py
Used to generate a data summary in the **abstract-content format**. Similar to generating a Q&A dataset, generate a summary of different datasets by adjusting prompts and file paths.

## summary.py

To generate the summary of data using csv_files.

Parameters to be changed:

In the last line **api_key** should be changed to your own api_key; **csv_file_path** should be changed to the path of the CSV file to be processed; **json_file_path** changed to a json file path (not essential); **summary_file_path** changed to the path of the generated summary file (an empty file with the same name as the summary_file_path,Chinese should be placed in advance under this path when running for the first time)

Parameters that can be added:

K can be added to the function parameter to read the CSV file and generate a summary starting from the K+1 data. By default, k=0.

## baidu_wenxinyiyan.py
Wenxin Yiyan interface, which is used to create data.
