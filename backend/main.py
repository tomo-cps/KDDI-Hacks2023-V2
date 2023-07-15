## uvicorn main:app --host 0.0.0.0 --port 8000
## uvicorn main_fastapi:app --host 0.0.0.0 --port 8085
import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from fastapi.responses import FileResponse
import sqlite3
import re
import base64
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
from datetime import datetime

# model = AutoModelForCausalLM.from_pretrained("cyberagent/open-calm-small", device_map="auto", torch_dtype=torch.float16)
# tokenizer = AutoTokenizer.from_pretrained("cyberagent/open-calm-small")

model = AutoModelForCausalLM.from_pretrained("cyberagent/open-calm-7b", device_map="auto", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained("cyberagent/open-calm-7b")

class CreateWordCloud():
    def __init__(self, path, user, question):
        self.question = question
        self.path = path
        self.user = user
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        query = """
        SELECT question, answer
        FROM user_table
        WHERE path = :path AND user = :user
        """
        cursor.execute(query, (path, user))
        self.user_data = cursor.fetchall()

        current_time = datetime.now()
        self.wc_path = "wordclouds/output/"+path+"_"+user+"_"+current_time.strftime("%Y%m%d_%H%M%S")+".png"
    
    def get_ans(self, question):
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

    def extract_nouns(self, text):
        nouns = []
        t = Tokenizer()
        tokens = t.tokenize(text)
        for token in tokens:
            if token.part_of_speech.split(',')[0] == '名詞':
                nouns.append(token.surface)
        return nouns
    
    def preprocess_text(self, text):
        processed_text = re.sub(r'[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\s]', '', text)
        processed_text = re.sub(r'[a-zA-Z]', '', processed_text)
        processed_text = re.sub(r'[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\s\d]', '', processed_text)
        processed_text = re.sub(r'\d', '', processed_text)
        return processed_text
    
    def save_data(self, s_path, s_user, s_question, s_answer, s_wc_path):
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        data = {
            "path": s_path,
            "user": s_user,
            "question": s_question,
            "answer": s_answer,
            "wc_path": s_wc_path
            }

        c.execute('''
            INSERT INTO user_table (path, user, question, answer, wc_path)
            VALUES (:path, :user, :question, :answer, :wc_path)
        ''', data)

        conn.commit()
        conn.close()
        return s_wc_path

    
    def main(self):
        answer = self.get_ans(self.question)
        answer = re.sub(r'\);.*$', '', answer)
        user_data = self.user_data
        user_data.append((self.question, answer))
        
        noun_lst = []
        for tupe in user_data:
            text = tupe[0]+tupe[1]
            processed_text = self.preprocess_text(text)
            nouns = self.extract_nouns(processed_text)
            for noun in nouns:
                noun_lst.append(noun)

        # WordCloudを生成
        font_path = "./wordclouds/font/SourceHanSerifK-Light.otf"
        wordcloud = WordCloud(width=800, height=400, font_path=font_path, background_color='white').generate(' '.join(noun_lst))

        # WordCloudを表示または保存
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(self.wc_path)

        s_wc_path = self.save_data(self.path, self.user, self.question, answer, self.wc_path)
        return answer, s_wc_path

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
    path = question.path
    name = question.name
    question = question.question

    output = CreateWordCloud(path, name, question)
    ans, wc_path = output.main()

    with open(wc_path, "rb") as f:
        image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")
    return {"answer": ans, "wordcloud": encoded_image}
