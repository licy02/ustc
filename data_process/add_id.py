import json
import os

def add_id(number,college_dir,new_college_dir):
    dir_list=os.listdir(college_dir)
    for i in range(len(dir_list)):
        item = dir_list[i]
        file_path=college_dir+"\\"+item
        with open(file_path,'r',encoding='UTF-8') as f:
            data=json.load(f)
        new_file_path=new_college_dir+"\\"+item
        with open(new_file_path, 'w', encoding='UTF-8') as save:
            for j in range(len(data)):
                id='%d-%d-%d'%(number+1,i+1,j+1)
                data[j]['id']=id
            json.dump(data, save, indent=4, ensure_ascii=False)

def add_id_dir(dir,new_dir):
    college_dir_list=os.listdir(dir)
    for k in range(len(college_dir_list)):
        path=dir+'\\'+college_dir_list[k]
        new_path=new_dir+'\\'+college_dir_list[k]
        add_id(k,college_dir=path,new_college_dir=new_path)

if __name__ == "__main__":
    add_id_dir("C:\\Users\\86187\\PycharmProjects\\pythonProject6\\json","C:\\Users\\86187\\PycharmProjects\\pythonProject6\\new_json")








