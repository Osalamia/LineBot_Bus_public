
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests
from bus import get_token
import MyCommand
import json
import os
import logging
app = Flask(__name__)

try:
    with open("Tokens.json", "r") as file:
        CHANNEL_ACCESS_TOKEN = json.load(file).get("CHANNEL_ACCESS_TOKEN")
        CHANNEL_SECRET = json.load(file).get("CHANNEL_SECRET")
except FileNotFoundError:
    logging.warning("請先執行[第一次使用.exe]並輸入LINE CHANNEL資料")
    os._exit(0)


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

line_bot_api.push_message('U30838abc49d28474a3acf875481f7f6b', TextSendMessage(text='使用方式:\n1. 公車站 [出發公車站名]到[到達公車站名]\n2. 地點 [出發地點]到[到達地點]\n\n可利用command查找可用指令'))



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # message = TextSendMessage(text=event.message.text)
    client_id = event.source.user_id

    # 取得tdx_token失敗
    if tdx_token == None:
        line_bot_api.reply_message(event.reply_token,"取得tdx token 失敗")
        
    text = event.message.text
    message = TextSendMessage(MyCommand.cmd(text, tdx_token, client_id))
    line_bot_api.reply_message(event.reply_token,message)

if __name__ == "__main__":
    tdx_token = get_token()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)