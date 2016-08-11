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

help_text="1.翻訳(英->日)\n[使い方]「翻訳」という文字の後に翻訳した英文をいれてください\n2.「メモ見る」\n3.「メモ作成」"

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/pre-registration'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    user_id = db.Column(db.String(80), unique=True)

    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def __repr__(self):
        return '<User %r>' % self.username

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(80))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


    def __init__(self, tasks, user_id):
        self.task = task
        self.user_id = user_id

    def __repr__(self):
        return '<Task %r>' % self.tasks


@app.route("/callback", methods=['POST'])
def callback():


    msgs = request.json['result']

    for msg in msgs:

        sender = msg['content']['from']
        if not db.session.query(User).filter(User.user_id == sender).count():
            reg = User('user_'+str(sender), sender)
            db.session.add(reg)
            db.session.commit()
            print("ユーザー登録完了",str(sender))

        else:
            print("ユーザー登録済み")
        text = msg['content']['text']

        if re.compile("翻訳|translate|訳し|訳す|ほんやく").match(text):

            pre_translate_text=text.replace("翻訳","")
            print("翻訳に反応")
            print(pre_translate_text)
            post_text(msg['content']['from'],get_translate(pre_translate_text))
        elif re.compile("メモ作成").match(text):

            text=text.replace("メモ登録","")
            user_id= db.session.query(User).filter(User.user_id == sender).first().id
            # DB追加
            task = Task(text, user_id)
            db.session.add(task)
            db.session.commit()
            print("メモに登録完了")
            post_text(msg['content']['from'],"メモに登録しました")
        elif re.compile("メモ見る").match(text):
            print("メモを参照")
            text=text.replace("メモ見る","")
            user_id= User.query.filter_by(User.user_id == sender).first().id
            tasks = Task.query.filter_by(Task.user_id == user_id).first().task
            memo_text=""

            post_text(msg['content']['from'],"メモを参照"+str(tasks))
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
