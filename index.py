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
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
