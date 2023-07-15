import os
import sqlite3

# 既存のデータベースファイルが存在する場合は削除
if os.path.exists('user.db'):
    os.remove('user.db')

# SQLiteデータベースに接続
conn = sqlite3.connect('user.db')

# カーソルを作成
cursor = conn.cursor()

# テーブルを作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_table (
        path TEXT,
        user TEXT,
        question TEXT,
        answer TEXT,
        wc_path TEXT
    )
''')

# デモデータを追加
cursor.execute('''
    INSERT INTO user_table (path, user, question, answer, wc_path)
    VALUES ('chat5', 'とも', '機械学習ってなんですか', 'ニューラルネットワークを使っています．脳の構造を模したものです', '/path/to/wc')
''')
               
# 変更をコミットして接続を閉じる
conn.commit()
conn.close()