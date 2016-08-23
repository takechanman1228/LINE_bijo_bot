from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from microsofttranslator import Translator
import pandas as pd
import os
from flask import request
import requests
import json
import re

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINEBOT_API_IMAHE_VIDEO = 'https://trialbot-api.line.me/v1/bot/message/'
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
    print(content)
    r = requests.post(LINEBOT_API_EVENT, headers=LINE_HEADERS, data=json.dumps(msg))

# http://line.github.io/line-bot-api-doc/ja/api/message_content/get.html
def get_image(messageId):
    image_endpoint = LINEBOT_API_IMAHE_VIDEO+messageId+'/content'
    binary_img_response = requests.get(image_endpoint, headers=LINE_HEADERS)
    print(image_endpoint)

    # binary dataをjpegにする必要あり



def post_image( to, originalContentUrl, previewImageUrl):
    msg = {
      'to':[to],
      'toChannel':1383378250, # Fixed  value
      'eventType':"138311608800106203", # Fixed  value
      'content':{
        'contentType':2, # 画像は2
        'toType':1,
        'originalContentUrl':originalContentUrl,
        'previewImageUrl':previewImageUrl
      }
    }
    print("oumu_image")
    print(msg)
    r = requests.post(LINEBOT_API_EVENT, headers=LINE_HEADERS, data=json.dumps(msg))

def post_text( to, text ):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)



def post_rich_text(to):
    content = {
        'contentType':12,
        'toType':1,
        "contentMetadata": {
            "DOWNLOAD_URL": "http://example.com/bot/images/12345",
            "SPEC_REV": "1",
            "ALT_TEXT": "Please visit our homepage and the item page you wish.",
            "MARKUP_JSON":
            {
              "canvas": {
                "width": 1040,
                "height": 1040,
                "initialScene": "scene1"
              },
              "images": {
                "image1": {
                  "x": 0,
                  "y": 0,
                  "w": 1040,
                  "h": 1040
                }
              },
              "actions": {
                "openHomepage": {
                  "type": "web",
                  "text": "Open our homepage.",
                  "params": {
                    "linkUri": "http://your.server.name/"
                  }
                },
                "sayHello": {
                  "type": "sendMessage",
                  "text": "Say hello.",
                  "params": {
                    "text": "Hello, Brown!"
                  }
                }
              },
              "scenes": {
                "scene1": {
                  "draws": [
                    {
                      "image": "image1",
                      "x": 0,
                      "y": 0,
                      "w": 1040,
                      "h": 1040
                    }
                  ],
                  "listeners": [
                    {
                      "type": "touch",
                      "params": [0, 0, 1040, 350],
                      "action": "openHomepage"
                    },
                    {
                      "type": "touch",
                      "params": [0, 350, 1040, 350],
                      "action": "sayHello"
                    }
                  ]
                }
              }
            }# end copy
        }
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

help_text="1.翻訳(英->日)\n[使い方]「翻訳」という文字の後に翻訳した英文をいれてください\n2.「メモ見る」+メモの内容\n3.「メモ作成」\n4.「メモけす」+メモの番号\n"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    user_code = db.Column(db.String(80), unique=True)

    def __init__(self, username, user_code):
        self.username = username
        self.user_code = user_code

    def __repr__(self):
        return '<User %r>' % self.username

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


    def __init__(self, task, user_id):
        self.task = task
        self.user_id = user_id

    def __repr__(self):
        return '<Task %r>' % self.task


@app.route("/callback", methods=['POST'])
def callback():


    msgs = request.json['result']

    for msg in msgs:

        sender = msg['content']['from']
        content_id = msg['content']['id']
        if not db.session.query(User).filter(User.user_code == sender).count():
            reg = User('user_'+str(sender), sender)
            db.session.add(reg)
            db.session.commit()
            print("ユーザー登録完了",str(sender))

        else:
            print("ユーザー登録済み")
        text = msg['content']['text']


        # メッセージ送信者のユーザーid
        user_id= db.session.query(User).filter(User.user_code == sender).first().id
        print("content_id")
        print(content_id)

        if text == "text":
            image = msg['content']['text']
            print("image")
            print(image)

        elif re.compile("翻訳|translate|訳し|訳す|ほんやく").match(text):

            pre_translate_text=text.replace("翻訳","")
            print("翻訳に反応")
            print(pre_translate_text)
            post_text(sender,get_translate(pre_translate_text))
        elif re.compile("メモ作成").match(text):

            text=text.replace("メモ作成","")
            # DB追加
            task = Task(text, user_id)
            db.session.add(task)
            db.session.commit()
            print("メモに登録完了")
            post_text(sender,"メモに登録しました")
        elif re.compile("メモ見る").match(text):
            print("メモを見る")
            text=text.replace("メモ見る","")
            text_task=""
            tasks = db.session.query(Task).filter(Task.user_id == user_id)
            for idx, task_obj in enumerate(tasks):
                text_task+=(str(idx+1) +":"+task_obj.task+"\n")

            print(text_task)
            post_text(sender,"メモの検索結果\n"+str(text_task))
        elif re.compile("メモけす").match(text):
            print("メモけす")
            task_num_to_delete=int(text.replace("メモけす",""))

            task_to_delete = db.session.query(Task).filter(Task.user_id == user_id)[task_num_to_delete-1]
            task_deleted=task_to_delete.task
            db.session.delete(task_to_delete)
            db.session.commit()

            print(task_to_delete)
            post_text(sender,"メモを消去しました\n"+str(task_deleted))
        else:

            # post_rich_text(sender) #TODO:リッチテキスト
            print("該当なし")
            get_image('4804782161918')
            post_image(sender, 'https://pbs.twimg.com/media/Ce3x_joUIAASsCo.jpg', 'https://pbs.twimg.com/media/Ce3x_joUIAASsCo.jpg')


        print(msgs)
        print(sender)



    return ''

if __name__ == '__main__':

    app.run(host = '0.0.0.0', port = 443, threaded = True, debug = True)
