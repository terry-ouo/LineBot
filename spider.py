from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, app, render_template,request
from flask.helpers import url_for

credits = credentials.Certificate()
firebase_admin.initialize_app(credits)
db = firestore.client()

@app.route("/")
def index():
    homepage = "test"
    return homepage

#網頁爬蟲
@app.route("/spider")
def spider():
#網址
    url = "https://tw.hjwzw.com/"
    data = request.get(url)
    data.encoding = "utf-8"
    sp = BeautifulSoup(data.txt, "html.parser")
    
