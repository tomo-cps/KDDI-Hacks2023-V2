## uvicorn main_fastapi:app --host 0.0.0.0 --port 8085
import os
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("cyberagent/open-calm-small", device_map="auto", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained("cyberagent/open-calm-small")

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
        "https://api.tomoaki-ohkawa.com/chat6",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ask")
def ask_question(question: Question):
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
        
    output = tokenizer.decode(tokens[0], skip_special_tokens=True)
    # response = index.query(llm=llm, question=question.question)
    # res = llm(response+"/n"+"/n"+"上のテキスト情報の出力がキリが悪いので，キリをよくしてください.なお，高校生でもわかりやすい出力をしてください")
    # max_length = 200  # 任意の最大文字数を設定
    # shortened_response = response[:max_length]
    return {"answer": output}
    # return {"answer": res}
