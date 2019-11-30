# ししゃも
個人で使用するためのLINE Message APIを使用したBOT  
（masterへプッシュすると自動的にherokuにデプロイされるため注意）

### できること
  - 指定ユーザへのPush通知
  - 言葉のおうむ返し
  - ユーザIDの表示

### 環境
- heroku
- LINE Message API
- Python 3.7.0
- ライブラリ
  - Flask==1.1.1
  - line-bot-sdk==1.15.0
- 環境変数
  - LINE_CHANNEL_SECRET -> 鍵
  - LINE_CHANNEL_ACCESS_TOKEN -> トークン
  - USER_ID -> 自身のユーザID
  
### 使用例
ゴミ捨てを教えてくれるRESTと組み合わせてスケジューリングした。
https://github.com/machitomo/gomiSearch
![example](https://github.com/machitomo/ShisyamoLineBot/blob/image/image/sample.jpg)

