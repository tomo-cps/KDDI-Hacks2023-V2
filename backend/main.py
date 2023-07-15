## uvicorn main:app --host 0.0.0.0 --port 8000
## uvicorn main_fastapi:app --host 0.0.0.0 --port 8085
import os
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from fastapi.responses import FileResponse
import sqlite3
import re
import base64
from wordclouds import wc

model = AutoModelForCausalLM.from_pretrained("cyberagent/open-calm-small", device_map="auto", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained("cyberagent/open-calm-small")

# model = AutoModelForCausalLM.from_pretrained("cyberagent/open-calm-7b", device_map="auto", torch_dtype=torch.float16)
# tokenizer = AutoTokenizer.from_pretrained("cyberagent/open-calm-7b")

def get_ans(question):
    inputs = tokenizer(str(question), return_tensors="pt").to(model.device)
    with torch.no_grad():
        tokens = model.generate(
            **inputs,
            max_new_tokens=64,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.05,
            pad_token_id=tokenizer.pad_token_id,
        )
        
    ans = tokenizer.decode(tokens[0], skip_special_tokens=True)
    return ans
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://gmc.cps.akita-pu.ac.jp/",
        "https://gmc.cps.akita-pu.ac.jp/chat1",
        "https://gmc.cps.akita-pu.ac.jp/chat2",
        "https://gmc.cps.akita-pu.ac.jp/chat3",
        "https://gmc.cps.akita-pu.ac.jp/chat4",
        "https://gmc.cps.akita-pu.ac.jp/chat5",
        "https://gmc.cps.akita-pu.ac.jp/chat6",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class Question(BaseModel):
    name: str
    path: str
    question: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask")
def ask_question(question: Question):
    name = question.name
    path = question.path
    question = question.question
    output = wc.CreateWordCloud(path, name)
    wc_path = output.main()
    print(wc_path)

    ans = get_ans(question)
    ans = re.sub(r'\);.*$', '', ans)
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    data = {
        "path": path,
        "user": name,
        "question": question,
        "answer": ans,
        "wc_path": wc_path
        }

    c.execute('''
        INSERT INTO user_table (path, user, question, answer, wc_path)
        VALUES (:path, :user, :question, :answer, :wc_path)
    ''', data)

    conn.commit()
    conn.close()
    with open(wc_path, "rb") as f:
        image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
    return {"answer": ans, "wordcloud": encoded_image}
