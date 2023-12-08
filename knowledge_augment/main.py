from search_db import GeneratePrompt
from chat_glm import GeneratorAnswer, LoadModel
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()


class chatItem(BaseModel):
    query: str


@app.post('/chat')
def chat(item: chatItem):
    prompt = GeneratePrompt(item.query, 1)
    answer_result = GeneratorAnswer(model, tokenizer, prompt)
    return(answer_result)


if __name__ == "__main__":
    model, tokenizer = LoadModel()
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)