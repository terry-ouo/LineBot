from bs4 import BeautifulSoup
import requests
import config


def spider():
    data = requests.get(config.weather_url)
    data.encoding = "utf-8"
    sp = BeautifulSoup(data.text, "html.parser")
    result = sp.select("div.wrapper div.row div.tab-content #country")
    print(result)


spider()
