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
    # allow_origins=["*"],
    allow_origins=[
        "https://api.tomoaki-ohkawa.com",
        "https://api.tomoaki-ohkawa.com/chat1",
        "https://api.tomoaki-ohkawa.com/chat2",
        "https://api.tomoaki-ohkawa.com/chat3",
        "https://api.tomoaki-ohkawa.com/chat4",
        "https://api.tomoaki-ohkawa.com/chat5",
        "https://api.tomoaki-ohkawa.com/chat5/",
        "https://api.tomoaki-ohkawa.com/chat6",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class Question(BaseModel):
    # user: str
    question: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask")
def ask_question(question: Question):
    ans = get_ans(question)
    ans = re.sub(r'\);.*$', '', ans)
    print(ans)
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    data = {"user": "tomo", "question": question.question, "answer": ans}

    c.execute('''
        INSERT INTO questions (user, question, answer)
        VALUES (:user, :question, :answer)
    ''', data)

    conn.commit()
    conn.close()
    
    return {"answer": ans}

@app.get("/asuka")
async def get_imges():
    image_path = "./data/asuka.png"
    return FileResponse(image_path, media_type="image/png") 
