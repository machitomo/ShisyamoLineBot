# -*- coding: utf-8 -*-
import json
import os
import sys
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

from docs import setting

app = Flask(__name__)

# Herokuの変数からトークンなどを取得
channel_secret = setting.SECRET
channel_access_token = setting.TOKEN
user_id = setting.USER_ID

# 環境変数の取得等が正常に行われているかを判定する
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

# LINEを使用するのに必要なハンドラー等の設定
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    """
    LINEからのWebhook
    :return:json
    """
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return json.dumps('OK. Hook Success.')


@app.route("/push", methods=['POST'])
def push():
    """
    プッシュ通知を送信する。
    :return: HTTPステータス
    """
    request_json = request.get_json()
    if 'message' not in request_json:
        abort(400)

    message_value = request_json['message']
    message = TextSendMessage(text=message_value)
    line_bot_api.push_message(user_id, messages=message)

    return json.dumps('OK. Sent your message.')


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合
    reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。
    第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
    :param event:
    :return:
    """
    if event.message.text == 'プロフィール':
        show_profile(event)

    else:
        # 入力された内容(event.message.text)に応じて返信する
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )


def show_profile(event):
    """
    プロフィールの表示を行う
    :param event:
    :return:
    """
    profile = line_bot_api.get_profile(event.source.user_id)

    messages = TextSendMessage(text=profile.user_id)

    line_bot_api.reply_message(
        event.reply_token,
        messages=messages
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
