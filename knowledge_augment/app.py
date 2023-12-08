from transformers import AutoModel, AutoTokenizer
import streamlit as st
from streamlit_chat import message
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from search_db import GeneratePrompt
import torch

connections.connect("default", host="localhost", port="19530", user='root', password='Milvus')
collection_name = 'ustc'
collection = Collection(collection_name)

st.set_page_config(
    page_title="智慧校园 演示",
    page_icon=":robot:",
    layout='wide'
)


@st.cache_resource
def get_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(
        "D:\model\chatglm2-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained(
        "D:\model\chatglm2-6b", trust_remote_code=True) \
        .half().quantize(4).to(device)
    model = model.eval()
    return tokenizer, model


def new_click():
    st.session_state['show_history'] = []
    st.session_state['input_history'] = []
    st.session_state['past_key_values'] = None


tokenizer, model = get_model()

st.title("USTC-GPT")

max_length = st.sidebar.slider(
    'max_length', 0, 32768, 8192, step=1
)
# top_p = st.sidebar.slider(
#     'top_p', 0.0, 1.0, 0.8, step=0.01
# )
top_k = st.sidebar.slider(
    'top_k', 0, 5, 1, step=1
)
temperature = st.sidebar.slider(
    'temperature', 0.0, 1.0, 0.8, step=0.01
)

if 'show_history' not in st.session_state:
    st.session_state.show_history = []

if 'input_history' not in st.session_state:
    st.session_state.input_history = []

if 'past_key_values' not in st.session_state:
    st.session_state.past_key_values = None

button2 = st.button("重新发起对话", key="delete")
if button2:
    new_click()


for i, (query, response) in enumerate(st.session_state.show_history):
    with st.chat_message(name="user", avatar="user"):
        st.markdown(query)
    with st.chat_message(name="assistant", avatar="assistant"):
        st.markdown(response)

with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()

prompt_text = st.text_area(label="用户输入",
                           height=100,
                           placeholder="请在这儿输入您的问题")



button1 = st.button("发送", key="predict")

if button1:
    input_placeholder.markdown(prompt_text)
    input_history, show_history, past_key_values = st.session_state.input_history, st.session_state.show_history,\
        st.session_state.past_key_values
    if len(show_history) == 0:
        query = GeneratePrompt(prompt_text, top_k)
        print(query)
    else:
        query = prompt_text
        print(query)
    i = 0
    top_p = 0.8
    # for response, input_history, past_key_values in model.stream_chat(tokenizer, query, input_history,
    #                                                             past_key_values=past_key_values,
    #                                                             max_length=max_length, top_p=top_p,
    #                                                             temperature=temperature,
    #                                                             return_past_key_values=True):
    out = model.stream_chat(tokenizer, query, input_history,
                                                                past_key_values=past_key_values,
                                                                max_length=max_length, top_p=top_p,
                                                                temperature=temperature,
                                                                return_past_key_values=True)
    for response, input_history, past_key_values in out:
        message_placeholder.markdown(response)
        i += 1
    # print(type(past_key_values))
    # print(past_key_values)
    st.session_state.input_history = input_history
    st.session_state.show_history = show_history + [(prompt_text, input_history[-1][1])]
    st.session_state.past_key_values = past_key_values

