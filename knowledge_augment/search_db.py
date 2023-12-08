from pymilvus import connections, Collection
from extract_embedding import get_embedding

connections.connect("default", host="localhost", port="19530", user='root', password='Milvus')
collection_name = 'ustc'
collection = Collection(collection_name)

def SearchDb(query_str:str, topk=5):
    #输入问题，ai数据库中返回topk个相近的答案
    collection.load()
    search_params = {"metric_type": "IP", "params": {"nprobe": 64}}
    embedding = get_embedding(query_str,is_insert=False)
    results = collection.search(
        data=[embedding],
        anns_field="embedding",
        param=search_params,
        limit=topk,
        output_fields=["text"]
    )
    res = []
    for hits in results:
        for hit in hits:
            score = round(hit.distance, 3)
            if score >= 0.2:
                res.append({
                    "score": score,
                    "text": hit.entity.get('text')
                })
    print("Successfully searched similar texts!")
    return res

def GeneratePrompt(query: str,topk):
    # 基于上下文的prompt模版，请务必保留"{question}"和"{context}"
    related_docs = SearchDb(query, topk)
    if len(related_docs)>0:
        PROMPT_TEMPLATE = """已知信息：
        {context} 
    
        根据上述已知信息，来回答用户的问题。问题是：{question}"""
        context = "\n".join([doc['text'] for doc in related_docs])
        prompt = PROMPT_TEMPLATE.replace("{question}", query).replace("{context}", context)
    else:
        prompt = query
    return prompt
