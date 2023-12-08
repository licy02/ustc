import os
import json

def get_file_length(file_path):
    with open(file_path,"r",encoding="UTF-8") as f:
        data=json.load(f)
        length=len(data)
        return length

def display_length(dir):
    filelist=os.listdir(dir)
    for item in filelist:
        filepath=dir+"/"+item
        filelength=get_file_length(filepath)
        print(item+"的数据条数是：%d\n"%filelength)

if __name__ == "__main__":
    display_length(dir="C:\\Users\\tjufe\\Desktop\\dachuang\\ustc\\data\\abstract")