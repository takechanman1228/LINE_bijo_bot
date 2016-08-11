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

help_text="1.翻訳(英->日)\n2.メモ\n"

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():


    msgs = request.json['result']
    # log_df = pd.DataFrame(logs_list, columns=["logs"])
    # log_df.to_csv( 'logs_test.csv', index=False)

    for msg in msgs:
        text = msg['content']['text']
        # logs_list.append(text)
        # for matcher, action in commands:
        #     if matcher.search(text):
        #         response = action(text)
        #         break
        # else:
        #     response = 'コマネチ'
        if re.compile("翻訳|translate|訳し|訳す|ほんやく").match(text):
        # if text.replace("翻訳|translate|訳し|訳す|ほんやく","",1):

            pre_translate_text=text.replace("翻訳","")
            # pre_translate_text=text.translate(None, '翻訳')
            print("翻訳に反応")
            print(pre_translate_text)
            post_text(msg['content']['from'],get_translate(pre_translate_text))
        elif re.compile("メモに登録").match(text):
            print("メモに登録")
            post_text(msg['content']['from'],"メモに登録しました")
        elif re.compile("メモ").match(text):
            print("メモを参照")
            post_text(msg['content']['from'],"メモを参照")
        else:
            post_text(msg['content']['from'],help_text)

        # 翻訳
        # df=pd.read_csv("secret_bing_translate.csv", header=None)
        # NAME_TRANS = df[0][0]
        # KEY_TRANS = df[0][1]
        # translator = Translator(NAME_TRANS, KEY_TRANS)
        # # to_lang = request.form["to_lang"]
        # # from_lang = request.form["from_lang"]
        # translated_text = translator.translate(text, 'ja', 'en')
        # post_text(msg['content']['from'],translated_text)

        # log_df = pd.DataFrame(logs_list, columns=["logs"])
        # log_df.to_csv( 'logs.csv', index=False)
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
