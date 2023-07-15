# KDDI-Hacks2023-v2
公開してある[KDDI-Hacks2023のGitHub](https://github.com/tomo-cps/KDDI-Hacks2023)をオープンキャンパス用に改良しました．

### ハッカソンとの差分
- デプロイしました！
  - nginx，proxy_passの設定など
- Azure OpenAI APIの代わりにサイバーエージェント LLM を使ってなんとか代用しました
- バックエンドはGPUマシンで計算させ，フロントはCPUマシンで動いています．
  - マイクロサービス化
- データベース(sqlite3)との連携
  - リダイレクト先，ユーザ名，質問，回答，WordCLoudのパスを保存
```
sqlite> .schema
CREATE TABLE user_table (
        path TEXT,
        user TEXT,
        question TEXT,
        answer TEXT,
        wc_path TEXT
    );
 ```

- リダイレクト先，ユーザ名，質問，回答に対して，動的に WordCloud として出力できるようにしました
  - [聴講者] 質問活性化の狙い => 質の高い質問が生まれるようになる
  - [発表者] どのような質問が多かったか視覚的にわかる => 発表の改善につながる
- Chat 画面をコンポーネント化し，管理しやすくしました
- エンターで質問できないようにしました
- 質問内容が空の時，送信ボタンの色が変わるようにしました

### デモ

![デモ動画gif](./demo/sample_v2.gif)


## Frontend
### How to run

```
docker build -t vuejs-docker .
```

```
docker run -it -p 8080:8080 --rm --name dockerize-vuejs-app-1 vuejs-docker
```

## Backend
### How to run
```
bash run.sh
```
