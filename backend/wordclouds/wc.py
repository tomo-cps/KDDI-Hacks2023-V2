import sqlite3
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer
import matplotlib.pyplot as plt
import re
from datetime import datetime

class CreateWordCloud():
    def __init__(self, path, user):
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        query = """
        SELECT question, answer
        FROM user_table
        WHERE path = :path AND user = :user
        """
        cursor.execute(query, (path, user))
        self.data = cursor.fetchall()
        print(self.data)

        current_time = datetime.now()
        self.save_path = "wordclouds/output/"+path+"_"+user+"_"+current_time.strftime("%Y%m%d_%H%M%S")+".png"

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
    
    def main(self):
        noun_lst = []
        for tupe in self.data:
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
        plt.savefig(self.save_path)
        return self.save_path

# output = CreateWordCloud("chat5", "せん")
# output.main()