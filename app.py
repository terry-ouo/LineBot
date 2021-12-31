from typing import Collection
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
import requests
from flask import Flask, app, render_template, request
from flask.helpers import url_for
import random
import config

app = Flask(__name__)

line_bot_api = LineBotApi(config.line_bot_key)
handler = WebhookHandler(config.handler_key)
cred = credentials.Certificate(config.cred_name)
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route("/")
def index():
    home = "<a href=/spider>蜘蛛</a>"
    home += "<a href=/try>try</a>"
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
    message = event.message.text
    if message[:4].upper() == "LIST":
        res = novel_list()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=res))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Fail"))


def novel_list():
    info = ""
    collection_ref = db.collection("小說")
    docs = collection_ref.order_by("title").get()
    docs_new = collection_ref.order_by("new chapter").get()
    docs_update_time = collection_ref.order_by("update time").get()
    for time in range(10):
        num = random.randrange(len(docs))
        info += "Title: " + docs[num].to_dict()["title"] + "\n"
        # info += "New Chapter: " + docs_new[num].to_dict()["new chapter"] + "\n"
        # info += "Update Time: " + docs_update_time[num].to_dict()["update time"] + "\n"
    return info


def find_update(url):
    data = requests.get(url)
    data.encoding = "utf-8"
    sp = BeautifulSoup(data.text, "html.parser")
    results = sp.find_all("a")
    for res in results:
        title = res.get('title')
        if title is not None:
            if "章節名" in title:
                print(title)
                info = title.split("章節名")[-1].split("更新時間")
                chapter = info[0].strip()
                update_time = info[1].strip()
                dic = {"chapter": chapter, "time": update_time}

                return dic


# 網頁爬蟲
@app.route("/spider")
def spider():
    # 網址
    url = "https://tw.hjwzw.com/#"
    data = requests.get(url)
    data.encoding = "utf-8"
    sp = BeautifulSoup(data.text, "html.parser")
    results = sp.select("a")

    for result in results:
        title = result.get("title")
        if title is not None:
            if "小說名" in title:
                book_link = "https://tw.hjwzw.com" + result.get("href")
                part = title.split("作者:")
                novel_name = part[0].replace("小說名:", "")
                novel_author = part[1].replace("TXT下載 手打", "")
                # 找最新章節
                update = find_update(book_link)
                doc = {
                    "book link": book_link,
                    "title": novel_name,
                    "author": novel_author,
                    "new chapter": update["chapter"],
                    "update time": update["time"]
                }
                doc_ref = db.collection("小說").document(result.get("href").replace("/", "").replace("Book", ""))
                doc_ref.set(doc)

    return "已經上傳完畢"


@app.route("/try")
def try_page():
    return "ok"


if __name__ == "__main__":
    app.run()
