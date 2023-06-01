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

app = Flask(__name__)

import twstock

twstock.realtime.mock = False

def realtime(stock_id):    
    stock_info = twstock.realtime.get(stock_id)

    if stock_info['success'] == True:
        best_bid_price = stock_info['realtime']['best_bid_price']
        best_bid_volume = stock_info['realtime']['best_bid_volume']
        best_ask_price = stock_info['realtime']['best_ask_price']
        best_ask_volume = stock_info['realtime']['best_ask_volume']

        msg = (f"""{stock_id}即時股價資訊

股票名稱: {stock_info['info']['name']}
股票代碼: {stock_info['info']['code']}
資料時間: {stock_info['info']['time']}
當前股價: {stock_info['realtime']['latest_trade_price']}
開盤價: {float(stock_info['realtime']['open']):.2f}
最高價: {float(stock_info['realtime']['high']):.2f}
最低價: {float(stock_info['realtime']['low']):.2f}
當前交易量: {stock_info['realtime']['trade_volume']}
累積交易量: {stock_info['realtime']['accumulate_trade_volume']}
當前5筆成交價: {float(best_bid_price[0]):.2f}, {float(best_bid_price[1]):.2f}, {float(best_bid_price[2]):.2f}, {float(best_bid_price[3]):.2f}, {float(best_bid_price[4]):.2f}
當前5筆成交量: {int(best_bid_volume[0])}, {int(best_bid_volume[1])}, {int(best_bid_volume[2])}, {int(best_bid_volume[3])}, {int(best_bid_volume[4])}
最佳5筆成交價: {float(best_ask_price[0]):.2f}, {float(best_ask_price[1]):.2f}, {float(best_ask_price[2]):.2f}, {float(best_ask_price[3]):.2f}, {float(best_ask_price[4]):.2f}
最佳5筆成交量: {int(best_ask_volume[0])}, {int(best_ask_volume[1])}, {int(best_ask_volume[2])}, {int(best_ask_volume[3])}, {int(best_ask_volume[4])}
""")

        return msg
    else:
        error = "Data not found"

        return error

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
        TextSendMessage(text=realtime(stock_id)(event.message.text)))

if __name__ == "__main__":
    app.run()
