# KDDI-Hacks2023-v2
公開してある[KDDI-Hacks2023のGitHub](https://github.com/tomo-cps/KDDI-Hacks2023)をオープンキャンパス用に改良しました．

### ハッカソンとの差分
- デプロイしました！
  - nginx，proxy_passの設定など
- 質問と回答を動的に取得し，WordCloudとして出力できるようにしました
  - [聴講者] 質問活性化の狙い => 質の高い質問が生まれるようになる
  - [発表者] どのような質問が多かったか視覚的にわかる => 発表の改善につながる
- Chat画面をコンポーネント化し，管理しやすくしました
- エンターで質問できないようにしました
- 質問内容が空の時，送信ボタンの色が変わるようにしました

### デモ

![デモ動画gif](./demo/sample_v2.gif)



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
pip install -r requirements.txt
```

```
uvicorn main:app --port 8000
```
