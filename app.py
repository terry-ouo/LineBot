from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, app, render_template,request
from flask.helpers import url_for

app = Flask(__name__)

line_bot_api = LineBotApi('dbbCXNIvFeRtDbFWSx0Ba3neQTyfRl1b8c0iVeFNNYsjE4lTsSV+LnhNhGB+VjiaANDfyFHM5058Ny59l4TzE/1PASiSijDKPIlW5RKA/NTj6zhCZGm/8dXOGdzM8n/WTlKMejIrZYcPnsX/eqF9jAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('04fa00fd847749a6e3dbf463fa515371')

credits = credentials.Certificate("ServiceKey.json")
firebase_admin.initialize_app(credits)
db = firestore.client()

@app.route("/")
def index():
    home = "<a href=/spider>蜘蛛</a>"
    return home

# 監聽所有來自 /callback 的 Post Request
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()

#網頁爬蟲
@app.route("/spider")
def spider():
#網址
    url = "https://tw.hjwzw.com/"
    data = request.get(url)
    data.encoding = "utf-8"
    sp = BeautifulSoup(data.txt, "html.parser")
    result = sp.find("title",)
    
    for item in result:
        doc={
            "title" : item
        }

        doc_ref = db.collection("小說")
        doc_ref.set(doc)

    return "已經上傳完畢"

if __name__ == "__main__":
    app.run()
