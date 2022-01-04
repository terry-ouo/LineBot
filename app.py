from typing import Collection
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
)
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from flask import Flask, app, request
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
    home = "<a href=/spider>蜘蛛</a><br>"
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
    # 判斷呼叫的方法
    if message == "小說":
        res = novel_list()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=res))
    elif message == "行事曆":
        image_message = ImageSendMessage(
            original_content_url=config.schedule,
            preview_image_url=config.pre_schedule
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    elif message == "地圖":
        image_message = ImageSendMessage(
            original_content_url=config.map,
            preview_image_url=config.map
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    elif message == "主顧聖母堂":
        image_message = ImageSendMessage(
            original_content_url=config.providence,
            preview_image_url=config.providence
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    elif message == "小遊戲":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="小遊戲:猜拳! \n請輸入 剪刀 or 石頭 or 布"))
    elif message == "布":
        result = finger_guess_game_judge(0)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    elif message == "剪刀":
        result = finger_guess_game_judge(1)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    elif message == "石頭":
        result = finger_guess_game_judge(2)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result))
    elif message[:4].upper() == "HELP":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=config.help_information))
    elif message[:6].upper() == "REPORT":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=config.report))
    elif message.upper() == "EDITOR":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=config.can_editor))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=config.error))


# 用戶端呼叫LIST，執行，出現10本隨機小說
def novel_list():
    info = ""
    collection_ref = db.collection("小說")
    docs = collection_ref.order_by("title").get()
    for time in range(5):
        num = random.randrange(len(docs))
        info += "Title: " + docs[num].to_dict()["title"] + "\n"
        info += "New Chapter: " + docs[num].to_dict()["new chapter"] + "\n"
        info += "Update Time: " + docs[num].to_dict()["update time"] + "\n\n"
    return info


# 尋找資料的最新章節還有更新日期
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


# 抓取小說資料，不分類
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


# 猜拳遊戲
def finger_guess_game_player(event):
    hand = ["paper", "剪刀", "石頭"]
    player = hand[event - 1]
    return player


def finger_guess_game_pc():
    choice = random.randrange(3)
    hand = ["布", "剪刀", "石頭"]
    pc = hand[choice]
    return pc


def finger_guess_game_judge(even):
    player = finger_guess_game_player(even)
    pc = finger_guess_game_pc()
    if pc == player:
        return pc + "\n\ntie!ಠ_ರೃ"
    if pc == "布" and player == "剪刀":
        return pc + "\n\nplayer win!(｡◝‿◜｡)"
    elif pc == "布" and player == "石頭":
        return pc + "\n\npc win!(;´Д`)×"
    if pc == "剪刀" and player == "布":
        return pc + "\n\npc win!⁽͑˙˚̀⚐˚́˙⁾̉"
    elif pc == "剪刀" and player == "石頭":
        return pc + "\n\nplayer win!(´︶｀)"
    if pc == "石頭" and player == "paper":
        return pc + "\n\nplayer win!(≧◡≦)"
    elif pc == "石頭" and player == "剪刀":
        return pc + "\n\npc win!(╯︵╰,)"


if __name__ == "__main__":
    app.run()
