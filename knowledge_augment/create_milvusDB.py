from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

connections.connect("default", host="localhost", port="19530", user='root', password='Milvus')
collection_name = 'ustc'
if utility.has_collection(collection_name):
    utility.drop_collection(collection_name)
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=5000)
]
schema = CollectionSchema(fields, collection_name)
collection = Collection(collection_name, schema)
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "IP",
    "params": {"nlist": 384},
}
collection.create_index(field_name="embedding", index_params=index_params)
collection.load()
print("success Create collection: ", collection_name)

