from sentence_transformers import SentenceTransformer

model = SentenceTransformer('D:\\project1\\knowledge_augment\\model\\bge-large-zh-v1.5')



def get_embedding(sentences):
   return model.encode(sentences)


