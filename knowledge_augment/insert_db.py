from pymilvus import connections, Collection
# from pdf_load import extract_text_from_pdf
from extract_embedding import get_embedding
import json

connections.connect("default", host="localhost", port="19530", user='root', password='Milvus')
collection_name = 'ustc'
collection = Collection(collection_name)

def InsertDb_pdf(filepath):
    docs = extract_text_from_pdf(filepath)
    #sentences = [i.page_content for i in docs]
    embeddings = get_embedding(docs, is_insert=True, batch_size=10)
    mr = collection.insert([embeddings,docs])
    collection.flush()
    print('提取特征并存放ai数据库', mr.succ_count)


# def Insert_json(filepath):
#     with open(filepath, "r", encoding="utf-8") as f:
#         data = json.load(f)
#         temp = []
#         for i in data:
#             if len(i["content"]) != 0:
#                 temp.append(i["name"] + ":" + i["content"])
#             for j in i["subsections"]:
#                 if j["name"] in i["name"]:
#                     temp.append(j["name"] + ":" + j["content"])
#                 else:
#                     temp.append(i["name"] + j["name"] + ":" + j["content"])
#         embeddings = get_embedding(temp, is_insert=True, batch_size=10)
#         mr = collection.insert([embeddings, temp])
#         collection.flush()
#         print('提取特征并存放ai数据库', mr.succ_count)


def Insert_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        # a = 0
        # for i in data:
        #     if a < len(i["content"]):
        #         a = len(i["content"])
        # print(a)
        name = []
        content = []
        for i in data:
            name.append(i["name"])
            if len(i["content"]) > 1600:
                content.append((i["name"] + ":" + i["content"][:1600]))
            else:
                content.append(i["name"] + ":" + i["content"])
        embeddings = get_embedding(name, is_insert=True, batch_size=10)
        mr = collection.insert([embeddings, content])
        collection.flush()
        print('提取特征并存放ai数据库', mr.succ_count)


# InsertDb_pdf('中科大不完全入学指南.pdf')
Insert_json("./data/数学科学学院/数学科学学院_学院简介.json")