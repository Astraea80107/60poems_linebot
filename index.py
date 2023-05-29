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

import requests
import time

def search_map(location):

    api_key = "AIzaSyBWPCrm2QF-ocBbTSXd7rrltDi3liuHUIs"

    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query" : location,
        "language" : "zh-TW",
        "key" : api_key
    }

    results = []

    while True:
        response = requests.get(url,params = params)
        data = response.json()

        if "results" in data:
            results.extend(data["results"])

        if not "next_page_token" in data:
            break

        time.sleep(5)

        params["pagetoken"] = data["next_page_token"]

    for result in results:
        name = result["name"]
        address = result["formatted_address"]
        lat = result["geometry"]["location"]["lat"]
        lng = result["geometry"]["location"]["lng"]

        print("地點名稱: "+name ,"地址: "+address ,"座標: "+f"https://www.google.com/maps/dir/{lat}+{lng}","-"*70,sep = "\n")

    print(f"合計{len(results)}項")
    print("以下空白")

location = input("請輸入要查詢的地點: ")
search_map(location)

app = Flask(__name__)

line_bot_api = LineBotApi('30fHYzc70eBZEscXrgWyuW0QQMPVGPd4R+CLHhdJAeokJrgn5OlH+TxOcfAzdvxErPxRtvmc6kDr5gvrrm31urWPPayGhThQvwbZ0E79cWH+8M2pjXbtiAgzvwoHX+BcHRnozscUh8i6LIZaUU1zZAdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('b2a58c0974beadd965204bda652ced11')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(search_map(event.message.text)))


if __name__ == "__main__":
    app.run()
