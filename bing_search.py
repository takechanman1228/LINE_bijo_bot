from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
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
        # 'to': u7d8c4b981b6d3b93ff38bb89f6d1c5ae,
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

def get_translate(text):

    df=pd.read_csv("secret_bing_translate.csv", header=None)
    NAME_TRANS = df[0][0]
    KEY_TRANS = df[0][1]
    translator = Translator(NAME_TRANS, KEY_TRANS)
    translated_text = translator.translate(text, 'ja', 'en') #japanese to english
    return translated_text

def get_memo(text):

    df=pd.read_csv("secret_bing_translate.csv", header=None)
    NAME_TRANS = df[0][0]
    KEY_TRANS = df[0][1]
    translator = Translator(NAME_TRANS, KEY_TRANS)
    translated_text = translator.translate(text, 'ja', 'en') #japanese to english
    return translated_text

def set_memo(text):

    df=pd.read_csv("secret_bing_translate.csv", header=None)
    NAME_TRANS = df[0][0]
    KEY_TRANS = df[0][1]
    translator = Translator(NAME_TRANS, KEY_TRANS)
    translated_text = translator.translate(text, 'ja', 'en') #japanese to english
    return translated_text

help_text="1.翻訳(英->日)\n[使い方]翻訳したい文字の前後に「翻訳」という文字を入れてください\n2.メモ\n"

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)



@app.route("/callback", methods=['POST'])
def callback():


    msgs = request.json['result']

    # me = User('user_'+str(msg['content']['from']), msg['content']['from'])
    # db.session.add(me)
    # db.session.commit()

    for msg in msgs:
        text = msg['content']['text']

        if re.compile("翻訳|translate|訳し|訳す|ほんやく").match(text):

            pre_translate_text=text.replace("翻訳","")
            print("翻訳に反応")
            print(pre_translate_text)
            post_text(msg['content']['from'],get_translate(pre_translate_text))
        elif re.compile("メモ").match(text):
            print("メモに登録")
            text=text.replace("メモ","")
            # DB追加
            task = Task(text, msg['content']['from'])
            db.session.add(task)
            db.session.commit()
            post_text(msg['content']['from'],"メモに登録しました")
        elif re.compile("メモ見る").match(text):
            print("メモを参照")
            post_text(msg['content']['from'],"メモを参照")
        else:
            post_text(msg['content']['from'],help_text)

        print(msgs)
        print(msg['content']['from'])
        print(pre_translate_text)



    return ''
    # return render_template('logs.html', message=msgs)

if __name__ == '__main__':
    # list=['main_test']
    # df = pd.DataFrame(list, columns=["logs"])
    # df.to_csv( 'logs_main.csv', index=False)
    app.run(host = '0.0.0.0', port = 443, threaded = True, debug = True)
