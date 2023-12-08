from transformers import AutoTokenizer, AutoModel
import pandas as pd
import torch
import gc
from typing import Optional, List

def LoadModel():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(
        "D:\model\chatglm2-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained(
        "D:\model\chatglm2-6b", trust_remote_code=True)\
        .half().quantize(4).to(device)
    model = model.eval()
    return model, tokenizer


def ClearTorchCache():
    #gc.collect()
    if torch.has_cuda:
        CUDA_DEVICE = "cuda:0"
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
    else:
        print("未检测到 cuda，暂不支持清理显存")


def GeneratorAnswer(model, tokenizer, prompt: str):
    history = []
    max_token = 2048
    top_p = 0.7
    temperature = 0.95
    response, history = model.chat(
        tokenizer,
        prompt,
        history=[],
        max_length=max_token,
        top_p=top_p,
        temperature=temperature
    )
        # history += [[prompt, response]]
        # answer_result = AnswerResult()
        # answer_result.history = history
        # answer_result.llm_output = response
    ClearTorchCache()
    return response
