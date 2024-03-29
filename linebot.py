from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from microsofttranslator import Translator
import pandas as pd
import os
from flask import request
import requests
import json
import re
from datetime import datetime
import random
import mojimoji


LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINEBOT_API_IMAHE_VIDEO = 'https://trialbot-api.line.me/v1/bot/message/'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':'1469904360', # Channel ID
    'X-Line-ChannelSecret':'cadb3352a866e7811c1a5d8d655e3f91', # Channel secre
    'X-Line-Trusted-User-With-ACL':'u48d6abf59024909b4a3eae290539188e' # MID (of Channel)
}
LINEBOT_API_PROFILE = 'https://trialbot-api.line.me/v1/profiles?mids='

def post_event( to, content):
    msg = {
        'to': [to],
        'toChannel': 1383378250, # Fixed  value
        'eventType': "138311608800106203", # Fixed value
        'content': content
    }
    print(content)
    r = requests.post(LINEBOT_API_EVENT, headers=LINE_HEADERS, data=json.dumps(msg))

# http://line.github.io/line-bot-api-doc/ja/api/message_content/get.html
def save_image(messageId):
    image_endpoint = LINEBOT_API_IMAHE_VIDEO+messageId+'/content'
    binary_img_response = requests.get(image_endpoint, headers=LINE_HEADERS)
    print(image_endpoint)

def get_user_name(to):
    profile_endpoint = LINEBOT_API_PROFILE+to
    profile = json.loads(requests.get(profile_endpoint, headers=LINE_HEADERS).text)
    print(profile_endpoint)
    print(profile)
    return profile['contacts'][0]['displayName']

def post_sticker( to,STKID,STKPKGID,STKVER):
    print("post_sticker")
    msg ={
        'to':[to],
        'toChannel':1383378250, # Fixed  value
        'eventType':'138311608800106203', # Fixed  value
        'contentTyoe': 8,
        'toType': 1,
        'contentMetadata':{
            'STKID':STKID,
            'STKPKGID':STKPKGID,
            'STKVER':STKVER
        }
    }
    r = requests.post(LINEBOT_API_EVENT, headers=LINE_HEADERS, data=json.dumps(msg))

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


def post_yes_no_rich(to):
    MARKUP_JSON = {
                    "scenes": {
                      "scene1": {
                        "listeners": [
                          {
                            "type": "touch",
                            "action": "action0",
                            "params": [0, 0, 520, 130]
                          },
                          {
                            "type": "touch",
                            "action": "action1",
                            "params": [520, 0, 520, 130]
                          }
                        ],
                        "draws": [
                          {
                            "h": 130,
                            "w": 1040,
                            "y": 0,
                            "x": 0,
                            "image": "image1"
                          }
                        ]
                      }
                    },
                    "actions": {
                      "action1": {
                        "params": {
                          "text": "B"
                        },
                        "type": "sendMessage"
                      },
                      "action0": {
                        "params": {
                          "text": "A"
                        },
                        "type": "sendMessage"
                      }
                    },
                    "images": {
                      "image1": {
                        "h": 130,
                        "w": 1040,
                        "y": 0,
                        "x": 0
                      }
                    },
                    "canvas": {
                      "height": 130,
                      "width": 1040,
                      "initialScene": "scene1"
                    }
                  }
    content = {
        'contentType':12,
        'toType':1,
        'contentMetadata': {
            'DOWNLOAD_URL': 'https://translate-application.herokuapp.com/static/image_ab',
            'SPEC_REV': '1',
            'ALT_TEXT': 'リッチメッセージが送信されました。',
            'MARKUP_JSON':json.dumps(MARKUP_JSON)

            }
        }
    post_event(to,content)

def post_4col_rich_message(to):
    MARKUP_JSON4 = {
                    "scenes": {
                      "scene1": {
                        "listeners": [
                          {
                            "type": "touch",
                            "action": "action0",
                            "params": [0, 0, 520, 520]
                          },
                          {
                            "type": "touch",
                            "action": "action1",
                            "params": [520, 0, 520, 520]
                          },
                          {
                            "type": "touch",
                            "action": "action2",
                            "params": [0, 520, 520, 520]
                          },
                          {
                            "type": "touch",
                            "action": "action3",
                            "params": [520, 520, 520, 520]
                          }
                        ],
                        "draws": [
                          {
                            "h": 1040,
                            "w": 1040,
                            "y": 0,
                            "x": 0,
                            "image": "image1"
                          }
                        ]
                      }
                    },
                    "actions": {
                      "action1": {
                        "params": {
                          "text": "1"
                        },
                        "type": "sendMessage"
                      },
                      "action0": {
                        "params": {
                          "text": "2"
                        },
                        "type": "sendMessage"
                      },
                        "action2": {
                        "params": {
                          "text": "3"
                        },
                        "type": "sendMessage"
                      },
                      "action3": {
                        "params": {
                          "text": "4"
                        },
                        "type": "sendMessage"
                      }
                    },
                    "images": {
                      "image1": {
                        "h": 1040,
                        "w": 1040,
                        "y": 0,
                        "x": 0
                      }
                    },
                    "canvas": {
                      "height": 1040,
                      "width": 1040,
                      "initialScene": "scene1"
                    }
                  }
    content = {
        'contentType':12,
        'toType':1,
        'contentMetadata': {
            'DOWNLOAD_URL': 'https://translate-application.herokuapp.com/static/9',
            'SPEC_REV': '1',
            'ALT_TEXT': 'リッチメッセージが送信されました。',
            'MARKUP_JSON':json.dumps(MARKUP_JSON9)

            }
        }
    post_event(to,content)


# 日英翻訳
def get_translate(text):
    df=pd.read_csv("secret_bing_translate.csv", header=None)
    NAME_TRANS = df[0][0]
    KEY_TRANS = df[0][1]
    translator = Translator(NAME_TRANS, KEY_TRANS)
    translated_text = translator.translate(text, 'ja', 'en') #japanese to english
    return translated_text


def post_woman_rich_from_url(to, url):
    MARKUP_JSON9 = {
                "scenes": {
                  "scene1": {
                    "listeners": [
                      {
                        "type": "touch",
                        "action": "action0",
                        "params": [0, 0, 346, 346]
                      },
                      {
                        "type": "touch",
                        "action": "action1",
                        "params": [346, 0, 346, 346]
                      },
                      {
                        "type": "touch",
                        "action": "action2",
                        "params": [692, 0, 346, 346]
                      },
                      {
                        "type": "touch",
                        "action": "action3",
                        "params": [0, 346, 346, 346]
                      },
                      {
                        "type": "touch",
                        "action": "action4",
                        "params": [346, 346, 346, 346]
                      },
                      {
                        "type": "touch",
                        "action": "action5",
                        "params": [692, 346, 346, 346]
                      },
                      {
                        "type": "touch",
                        "action": "action6",
                        "params": [0, 692, 346, 346]
                      },
                      {
                        "type": "touch",
                        "action": "action7",
                        "params": [346, 692, 346, 346]
                      },
                      {
                        "type": "touch",
                        "action": "action8",
                        "params": [692, 692, 346, 346]
                      }
                    ],
                    "draws": [
                      {
                        "h": 1040,
                        # "h": 700,
                        "w": 1040,
                        # "w": 700,
                        "y": 0,
                        "x": 0,
                        "image": "image1"
                      }
                    ]
                  }
                },
                "actions": {
                  "action1": {
                    "params": {
                      "text": "中上にタッチ"
                    },
                    "type": "sendMessage"
                  },
                  "action0": {
                    "params": {
                      "text": "左上にタッチ"
                    },
                    "type": "sendMessage"
                  },
                    "action2": {
                    "params": {
                      "text": "右上にタッチ"
                    },
                    "type": "sendMessage"
                  },
                  "action3": {
                    "params": {
                      "text": "左中にタッチ"
                    },
                    "type": "sendMessage"
                  },
                  "action4": {
                    "params": {
                      "text": "真ん中にタッチ"
                    },
                    "type": "sendMessage"
                  },
                  "action5": {
                    "params": {
                      "text": "右中にタッチ"
                    },
                    "type": "sendMessage"
                  },
                    "action6": {
                    "params": {
                      "text": "左下にタッチ"
                    },
                    "type": "sendMessage"
                  },
                  "action7": {
                    "params": {
                      "text": "中下にタッチ"
                    },
                    "type": "sendMessage"
                  },
                  "action8": {
                    "params": {
                      "text": "右下にタッチ"
                    },
                    "type": "sendMessage"
                  }
                },
                "images": {
                  "image1": {
                    "h": 1040,
                    # "h": 700,
                    "w": 1040,
                    "y": 0,
                    "x": 0
                  }
                },
                "canvas": {
                  "height": 1040,
                #   "height": 700,
                  "width": 1040,
                  "initialScene": "scene1"
                }
              }

    content = {
        'contentType':12,
        'toType':1,
        'contentMetadata': {
            'DOWNLOAD_URL': url,
            'SPEC_REV': '1',
            'ALT_TEXT': 'リッチメッセージが送信されました。',
            'MARKUP_JSON':json.dumps(MARKUP_JSON9)

            }
        }
    post_event(to,content)

def set_user_status(user_obj, status):
    user_obj.user_status=status
    db.session.add(user_obj)
    db.session.commit()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    user_code = db.Column(db.String(80), unique=True)
    user_status = db.Column(db.Integer)
    user_completed_status = db.Column(db.Integer)
    nanmonme = db.Column(db.Integer)
    waiting = db.Column(db.Integer)
    is_long = db.Column(db.Integer)
    is_black = db.Column(db.Integer)

    def __init__(self, username, user_code):
        self.username = username
        self.user_code = user_code
        self.user_status = 0
        self.user_completed_status = 0
        self.nanmonme = 0
        self.is_long = 0
        self.is_black = 0

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


# Yes/Noの問題
class Problem2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(80))
    answer= db.Column(db.Integer)

    def __init__(self, problem, answer):
        self.problem = problem
        self.answer = answer

    def __repr__(self):
        return '<Problems2 %r>' % self.problem2

class Woman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    womanurl = db.Column(db.String(120))
    comment1 = db.Column(db.String(120))
    comment2 = db.Column(db.String(120))
    comment3 = db.Column(db.String(120))
    comment4 = db.Column(db.String(120))
    comment5 = db.Column(db.String(120))
    comment6 = db.Column(db.String(120))
    comment7 = db.Column(db.String(120))
    comment8 = db.Column(db.String(120))
    comment9 = db.Column(db.String(120))
    # MARKUP_JSON9 = db.Column(db.String(120))

    def __init__(self,username,womanurl):
        self.username = username
        self.womanurl = womanurl
        self.comment1 = "location_1"
        self.comment2 = "location_2"
        self.comment3 = "location_3"
        self.comment4 = "location_4"
        self.comment5 = "location_5"
        self.comment6 = "location_6"
        self.comment7 = "location_7"
        self.comment8 = "location_8"
        self.comment9 = "location_9"

    def __repr__(self):
        return '<Woman %r>' % self.username

@app.route("/callback", methods=['POST'])
def callback():


    msgs = request.json['result']

    for msg in msgs:

        print(type(msg))
        # 友達追加
        if 'opType' in msg['content']:
            print("ontypeあり")
            onType = msg['content']['opType']
        else:
            onType = 0

        # アクションを起こしたユーザー
        if 'from' in msg['content']:
            print("fromあり")
            sender = msg['content']['from']
        else:
            sender = 0

        print(msg)
        if onType==4:
            print("友達追加")
            sender = msg['content']['params'][0]
            post_text(sender,"このbotはあなたのつらい朝をハッピーにするお手伝いをします。\n[使い方]\n「朝起きたい」,「時刻設定」と入力したら、起きたい時刻を設定出来ます。\n設定した時刻になったら，メッセージが来ます。\n あなたの好みを3回答えたら、お好みの美女が現れます。\nあとは、美女を触るも、起きて働くもあり！\n最高の一日にしましょう！\n")
            post_text(sender,"スタンプをおすか「ヘルプ」と送信するとヘルプを見ることができます。([デモ用]なにか話しかけると目覚ましがなり始めます)")

            user_obj = db.session.query(User).filter(User.user_code == sender).first()
            set_user_status(user_obj, 0)
            break


        # sender = msg['content']['from']
        content_id = msg['content']['id']
        content_type = msg['content']['contentType'] #1:text 2:image 3:video 10:友達追加
        # content_type = msg['content']['contentType']
        content_metadata = msg['content']['contentMetadata']
        text = msg['content']['text']
        # ユーザー名を取得
        print("ユーザーネーム")
        user_name = get_user_name(sender)
        print(user_name)


        if not db.session.query(User).filter(User.user_code == sender).count():
            reg = User('user_'+str(sender), sender)
            db.session.add(reg)
            db.session.commit()
            print("ユーザー登録完了",str(sender))

        else:
            print("ユーザー登録済み")


        # メッセージ送信者のユーザーid
        user_id= db.session.query(User).filter(User.user_code == sender).first().id
        print("content_id")
        print(content_id)

        # ユーザーの状態
        this_user = db.session.query(User).filter(User.user_code == sender).first()
        status = this_user.user_status
        completed_status = 0
        nanmonme = this_user.nanmonme
        waiting = this_user.waiting

        print("ユーザーの状態")
        print(status)

        text_hankaku=mojimoji.zen_to_han(text)


        if content_type == 8  or "ヘルプ" in text:
            print("スタンプ,ヘルプ")
            print(content_metadata)
            # print(content_metadata['STKID'])
            # print(content_metadata['STKPKGID'])
            post_text(sender,"このbotはあなたのつらい朝をハッピーにするお手伝いをします。\n[使い方]\n「朝起きたい」,「時刻設定」と入力したら、起きたい時刻を設定出来ます。\n設定した時刻になったら，メッセージが来ます。\n あなたの好みを3回答えたら、お好みの美女が現れます。\nあとは、美女を触るも、起きて働くもあり！\n最高の一日にしましょう！\n")
            post_text(sender,"スタンプをおすか「ヘルプ」と送信するとヘルプを見ることができます。([デモ用]なにか話しかけると目覚ましがなり始めます)")

            text=""
            set_user_status(this_user, 0)

        elif re.compile("翻訳|translate|訳し|訳す|ほんやく").match(text):

            pre_translate_text=text.replace("翻訳","")
            print("翻訳に反応")
            print(pre_translate_text)
            post_text(sender,get_translate(pre_translate_text))

        elif "タッチ" in text:
            print("タッチ受付")

            location_str=text.replace("にタッチ","")
            location_id=random.randint(1,9)
            print(location_str)
            woman_message=["早起きできる"+user_name+"さん、ステキです！",
                "早起き頑張った"+user_name+"さんの今日の運勢は大吉です",
                user_name+"さんに会えてよかった！今日も一日頑張って",
                user_name+"さん、いつも応援しています！",
                user_name+"さん、今日も輝いてるね",
                user_name+"さん，イキイキしてるね",
                user_name+"さん，意志が強いね",
                user_name+"さん，思い切りがいいね",
                user_name+"さん，決断力があるね"]
            random.shuffle(woman_message)
            post_text(sender,"美女:"+woman_message[location_id-1])

            this_user.user_completed_status=1
            db.session.add(this_user)
            db.session.commit()
            post_text(sender,"美女:"+"また明日も"+user_name+"さんに会えるといいな。明日も早起き応援してるよ！")
            post_text(sender,"[デモ用]なにか文字を入力すると，目覚ましの画面からスタートします")

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

        elif re.compile("朝起きたい|時刻設定").match(text):
            post_text(sender,"時間を入力してください（例:8:30）")

        elif re.search('\d+:\d\d$' , text_hankaku):
            print(text_hankaku)
            m = re.search('\d+:\d\d$' , text_hankaku)
            print(m.group(0))
            matched = m.group(0)
            post_text(sender,matched+"に起床時刻が設定されました")

        else:

            print("メイン")

            questions = ["A.大人っぽい B.幼い","A.癒やし B.元気","A.黒髪 B.茶髪","A.かわいい B.きれい","A.アウトドア B.インドア","A.ロング B.ショート"]
            reply_a = [
            "大人っぽい人いいですよね！",
            "癒やし分かります！",
            "黒髪いいですのう",
            "かわいいは正義",
            "アウトドア、健康ですね〜",
            "ロングいいですね〜"]

            reply_b = [
            "ロリいいですよね！",
            "元気が一番！",
            "ブラウン可愛いですよね",
            "ゴージャスですね！",
            "家の居心地最高〜〜",
            "ショート、似合う人本当に似合いますよね！"]

            if status ==0:

                post_text(sender,"じりりりりじりりりり\n8時です！起きてください！！！\n"+user_name+"さんが気持ちよく目覚めるのをサポートします．3つの質問に答えてください！")
                post_text(sender,"スタンプをおすか「ヘルプ」と送信するとヘルプを見ることができます。")
                post_text(sender,"一つ目。あなたの好みはどっち？？")
                post_text(sender,questions[nanmonme])
                post_yes_no_rich(sender)
                status=1
                this_user.user_status=status
                if nanmonme==5:
                    this_user.nanmonme=0
                else:
                    this_user.nanmonme=nanmonme+1
                db.session.add(this_user)
                db.session.commit()
                print("0->1 ")
            elif status==1:
                if text=="A":
                    post_text(sender,reply_a[nanmonme-1])
                elif text=="B":
                    post_text(sender,reply_b[nanmonme-1])

                post_text(sender,"二つ目，あなたの好みはどっち？？")
                post_text(sender,questions[nanmonme])
                post_yes_no_rich(sender)

                status = 2
                this_user.user_status=status
                if nanmonme==5:
                    this_user.nanmonme=0
                else:
                    this_user.nanmonme=nanmonme+1
                db.session.add(this_user)
                db.session.commit()
                print("1->2")
                print(status)

            elif status==2:
                if text=="A":
                    post_text(sender,reply_a[nanmonme-1])
                elif text=="B":
                    post_text(sender,reply_b[nanmonme-1])

                post_text(sender,"最後。今日の好みはどっち？？")
                post_text(sender,questions[nanmonme])
                post_yes_no_rich(sender)

                status =3
                this_user.user_status=status

                if nanmonme==5:
                    this_user.nanmonme=0
                else:
                    this_user.nanmonme=nanmonme+1
                db.session.add(this_user)
                db.session.commit()
                print("2->3")
                print(status)

            elif status==3:
                woman_class=random.randint(1,4)
                if nanmonme ==0:
                    print("ろんぐ/しょーと")
                    if text=="A":#ろんぐ
                        post_text(sender,reply_a[nanmonme-1])
                        woman_class=random.randint(1,2)
                    elif text=="B":#しょーと
                        post_text(sender,reply_b[nanmonme-1])
                        woman_class=random.randint(3,4)
                if nanmonme ==3:
                    print("黒/茶")
                    if text=="A":#くろ
                        post_text(sender,reply_a[nanmonme-1])
                        woman_class=random.randint(1,2)*2-1
                    elif text=="B": #ちゃ
                        post_text(sender,reply_b[nanmonme-1])
                        woman_class=random.randint(1,2)*2



                post_text(sender,user_name+"さんにぴったりの美女をご紹介します．")

                woman_all = db.session.query(Woman).all()
                woman_obj = woman_all[0]

                random_tekitou=random.randint(1,5)
                random_url="https://translate-application.herokuapp.com/static/4class"+"/"+str(woman_class)+"/"+str(random_tekitou)

                print(random_url)
                post_woman_rich_from_url(sender,random_url)
                post_text(sender,user_name+"さん、よく起きれたね")
                post_text(sender,"私の好きな場所をタッチしてね！場所に応じてあなたにメッセージをおくるよ！")

                set_user_status(this_user, 0)

        print(msgs)
        print(sender)





    return ''

if __name__ == '__main__':

    app.run(host = '0.0.0.0', port = 443, threaded = True, debug = True)
