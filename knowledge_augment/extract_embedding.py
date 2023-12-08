import torch
from transformers import AutoTokenizer, AutoModel

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained('D:/project/ustc/knowledge_augment/model/paraphrase-multilingual-v2', cache_dir='./model')
model = AutoModel.from_pretrained('D:/project/ustc/knowledge_augment/model/paraphrase-multilingual-v2', cache_dir='./model').to(device)


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


def get_embedding(sentences,is_insert, batch_size=10):
    if is_insert:
        res_embeddings = []
        for i in range(0,len(sentences), batch_size):
            batch = sentences[i:i + batch_size]
            encoded_input = tokenizer(batch, padding=True, truncation=True,
                                  max_length=512, return_tensors='pt').to(device)
            with torch.no_grad():
                model_output = model(**encoded_input)
            # Perform pooling. In this case, mean pooling.
            sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
            sentence_embeddings_norm = sentence_embeddings / sentence_embeddings.norm(p=2, dim=-1, keepdim=True)
            #sentence_embeddings_norm = sentence_embeddings_norm.squeeze(0)
            sentence_embeddings_norm = sentence_embeddings_norm.cpu().detach().numpy().tolist()
            res_embeddings.extend(sentence_embeddings_norm)
        return res_embeddings
    else:
        encoded_input = tokenizer(sentences, padding=True, truncation=True,
                                 max_length=512, return_tensors='pt').to(device)
        with torch.no_grad():
            model_output = model(**encoded_input)
        # Perform pooling. In this case, mean pooling.
        sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
        sentence_embeddings_norm = sentence_embeddings / sentence_embeddings.norm(p=2, dim=-1, keepdim=True)
        sentence_embeddings_norm = sentence_embeddings_norm.squeeze(0)
        sentence_embeddings_norm = sentence_embeddings_norm.cpu().detach().numpy().tolist()
        return sentence_embeddings_norm
