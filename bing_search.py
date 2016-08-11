from flask import Flask, render_template, request
from microsofttranslator import Translator
import pandas as pd
from flask import request
import requests
import json
import re

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':'1469904360', # Channel ID
    'X-Line-ChannelSecret':'cadb3352a866e7811c1a5d8d655e3f91', # Channel secre
    'X-Line-Trusted-User-With-ACL':'u48d6abf59024909b4a3eae290539188e' # MID (of Channel)
}

def post_event( to, content):
    msg = {
        'to': [to],
        'toChannel': 1383378250, # Fixed  value
        'eventType': "138311608800106203", # Fixed value
        'content': content
    }
    r = requests.post(LINEBOT_API_EVENT, headers=LINE_HEADERS, data=json.dumps(msg))

def post_text( to, text ):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)


commands = (
    (re.compile('ラッシャー', 0), lambda x: 'テメエコノヤロウ'),
    (re.compile('ダンカン', 0), lambda x:'バカヤロコノヤロウ'),
)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', message="翻訳したい文章を入力してください")

@app.route('/', methods=['POST'])
def post_request():
    # request.formにPOSTデータがある
    source = request.form["source"]
    df=pd.read_csv("secret_bing_translate.csv", header=None)
    NAME_TRANS = df[0][0]
    KEY_TRANS = df[0][1]
    translator = Translator(NAME_TRANS, KEY_TRANS)
    to_lang = request.form["to_lang"]
    from_lang = request.form["from_lang"]
    result = translator.translate(source, to_lang, from_lang)
    global firstevent
    histories[source] = result
    return render_template('index.html', message="翻訳結果", source = source, result=result, histories = histories)

@app.route("/callback", methods=['POST'])
def hello():
    msgs = request.json['result']
    for msg in msgs:
        text = msg['content']['text']
        for matcher, action in commands:
            if matcher.search(text):
                response = action(text)
                break
        else:
            response = 'コマネチ'

        post_text(msg['content']['from'],response)

    return ''

if __name__ == '__main__':
    histories = {}
    app.run()
