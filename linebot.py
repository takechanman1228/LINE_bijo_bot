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

LINEBOT_API_EVENT ='https://trialbot-api.line.me/v1/events'
LINEBOT_API_IMAHE_VIDEO = 'https://trialbot-api.line.me/v1/bot/message/'
LINE_HEADERS = {
    'Content-type': 'application/json; charset=UTF-8',
    'X-Line-ChannelID':'1475553245', # Channel ID
    'X-Line-ChannelSecret':'e1142eedb58469b23f0a4a881df4c95e', # Channel secre
    'X-Line-Trusted-User-With-ACL':'u779a6f828f45684ec738c32bbdbd44ac' # MID (of Channel)
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
def save_image(messageId):
    image_endpoint = LINEBOT_API_IMAHE_VIDEO+messageId+'/content'
    binary_img_response = requests.get(image_endpoint, headers=LINE_HEADERS)
    print(image_endpoint)

    # binary dataをjpegにする必要あり

def post_sticker( to,STKID,STKPKGID,STKVER):
      msg ={
        'to':[to],
        'toChannel':1383378250, # Fixed  value
        'eventType':"138311608800106203", # Fixed  value
        "contentMetadata":{
          "STKID":STKID,
          "STKPKGID":STKPKGID,
          "STKVER":STKVER
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

# 検索してきて，画像を取得
def post_query_image(to, query):

    post_image(to, )

def post_text( to, text ):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)


def post_vote_message(to):
    MARKUP_JSON={
                  'scenes': {
                    'scene1': {
                      'listeners': [
                        {
                          'type': 'touch',
                          'action': 'action1',
                          'params': [
                            0,
                            0,
                            520,
                            1040
                          ]
                        }
                      ],
                      'draws': [
                        {
                          'h': 520,
                          'w': 1040,
                          'y': 0,
                          'x': 0,
                          'image': 'image1'
                        }
                      ]
                    }
                  },
                  'actions': {
                    'action1': {
                      'params': {
                        'text': '投票！'
                      },
                      'type': 'sendMessage'
                    }
                  },
                  'images': {
                    'image1': {
                      'h': 520,
                      'w': 1040,
                      'y': 0,
                      'x': 0
                    }
                  },
                  'canvas': {
                    'height': 520,
                    'width': 1040,
                    'initialScene': 'scene1'
                  }
                }
    content = {
        'contentType':12,
        'toType':1,
        'contentMetadata': {
            'DOWNLOAD_URL': 'https://internship2016.herokuapp.com/static/vote',
            'SPEC_REV': '1',
            'ALT_TEXT': '美女がおたずねです',
            'MARKUP_JSON':json.dumps(MARKUP_JSON)

            }# end copy
        }
    post_event(to,content)

def post_rich_message(to):
    MARKUP_JSON={
                  'scenes': {
                    'scene1': {
                      'listeners': [
                        {
                          'type': 'touch',
                          'action': 'action1',
                          'params': [
                            0,
                            0,
                            1040,
                            1040
                          ]
                        }
                      ],
                      'draws': [
                        {
                          'h': 1040,
                          'w': 1040,
                          'y': 0,
                          'x': 0,
                          'image': 'image1'
                        }
                      ]
                    }
                  },
                  'actions': {
                    'action1': {
                      'params': {
                        'linkUri': 'http://www.google.com'
                      },
                      'type': 'web'
                    }
                  },
                  'images': {
                    'image1': {
                      'h': 1040,
                      'w': 1040,
                      'y': 0,
                      'x': 0
                    }
                  },
                  'canvas': {
                    'height': 1040,
                    'width': 1040,
                    'initialScene': 'scene1'
                  }
                }
    content = {
        'contentType':12,
        'toType':1,
        'contentMetadata': {
            'DOWNLOAD_URL': 'https://internship2016.herokuapp.com/static',
            'SPEC_REV': '1',
            'ALT_TEXT': 'Please visit our homepage and the item page you wish.',
            'MARKUP_JSON':json.dumps(MARKUP_JSON)

            }# end copy
        }
    post_event(to,content)

def post_yes_no_rich(to):
    MARKUP_JSON = {
                    "scenes": {
                      "scene1": {
                        "listeners": [
                          {
                            "type": "touch",
                            "action": "action0",
                            "params": [0, 0, 520, 1040]
                          },
                          {
                            "type": "touch",
                            "action": "action1",
                            "params": [520, 0, 520, 1040]
                          }
                        ],
                        "draws": [
                          {
                            "h": 520,
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
                          "text": "No"
                        },
                        "type": "sendMessage"
                      },
                      "action0": {
                        "params": {
                          "text": "Yes"
                        },
                        "type": "sendMessage"
                      }
                    },
                    "images": {
                      "image1": {
                        "h": 520,
                        "w": 1040,
                        "y": 0,
                        "x": 0
                      }
                    },
                    "canvas": {
                      "height": 520,
                      "width": 1040,
                      "initialScene": "scene1"
                    }
                  }

    content = {
        'contentType':12,
        'toType':1,
        'contentMetadata': {
            'DOWNLOAD_URL': 'https://internship2016.herokuapp.com/static/yn',
            'SPEC_REV': '1',
            'ALT_TEXT': 'Please visit our homepage and the item page you wish.',
            'MARKUP_JSON':json.dumps(MARKUP_JSON)

            }# end copy
        }
    post_event(to,content)


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

def post_9col_rich_message(to, json_custom):
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
                          "text": "2"
                        },
                        "type": "sendMessage"
                      },
                      "action0": {
                        "params": {
                          "text": "1"
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
                      },
                      "action4": {
                        "params": {
                          "text": "5"
                        },
                        "type": "sendMessage"
                      },
                      "action5": {
                        "params": {
                          "text": "6"
                        },
                        "type": "sendMessage"
                      },
                        "action6": {
                        "params": {
                          "text": "7"
                        },
                        "type": "sendMessage"
                      },
                      "action7": {
                        "params": {
                          "text": "8"
                        },
                        "type": "sendMessage"
                      },
                      "action8": {
                        "params": {
                          "text": "9"
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
            'DOWNLOAD_URL': 'https://internship2016.herokuapp.com/static/woman_test',
            'SPEC_REV': '1',
            'ALT_TEXT': 'Please visit our homepage and the item page you wish.',
            'MARKUP_JSON':json.dumps(json_custom)

            }# end copy
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
            'DOWNLOAD_URL': 'https://internship2016.herokuapp.com/static/9',
            'SPEC_REV': '1',
            'ALT_TEXT': 'Please visit our homepage and the item page you wish.',
            'MARKUP_JSON':json.dumps(MARKUP_JSON9)

            }# end copy
        }
    post_event(to,content)



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

def post_woman_rich_message(to, woman_obj):
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
                      "text": woman_obj.comment2
                    },
                    "type": "sendMessage"
                  },
                  "action0": {
                    "params": {
                      "text": woman_obj.comment1
                    },
                    "type": "sendMessage"
                  },
                    "action2": {
                    "params": {
                      "text": woman_obj.comment3
                    },
                    "type": "sendMessage"
                  },
                  "action3": {
                    "params": {
                      "text": woman_obj.comment4
                    },
                    "type": "sendMessage"
                  },
                  "action4": {
                    "params": {
                      "text": woman_obj.comment5
                    },
                    "type": "sendMessage"
                  },
                  "action5": {
                    "params": {
                      "text": woman_obj.comment6
                    },
                    "type": "sendMessage"
                  },
                    "action6": {
                    "params": {
                      "text": woman_obj.comment7
                    },
                    "type": "sendMessage"
                  },
                  "action7": {
                    "params": {
                      "text": woman_obj.comment8
                    },
                    "type": "sendMessage"
                  },
                  "action8": {
                    "params": {
                      "text": woman_obj.comment9
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
            'DOWNLOAD_URL': woman_obj.womanurl,
            'SPEC_REV': '1',
            'ALT_TEXT': 'Please visit our homepage and the item page you wish.',
            'MARKUP_JSON':json.dumps(MARKUP_JSON9)

            }
        }
    post_event(to,content)




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    user_code = db.Column(db.String(80), unique=True)
    user_status = db.Column(db.Integer)

    def __init__(self, username, user_code):
        self.username = username
        self.user_code = user_code
        self.user_status = 0

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

# 数字の問題
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    problem = db.Column(db.String(80))
    answer= db.Column(db.Integer)

    def __init__(self, problem, answer):
        self.problem = problem
        self.answer = answer

    def __repr__(self):
        return '<Problems %r>' % self.problem

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

    def __init__(self,username,womanurl,comment1,comment2,comment3,comment4,comment5,comment6,comment7,comment8,comment9):
        self.username = username
        self.womanurl = womanurl
        self.comment1 = comment1
        self.comment2 = comment2
        self.comment3 = comment3
        self.comment4 = comment4
        self.comment5 = comment5
        self.comment6 = comment6
        self.comment7 = comment7
        self.comment8 = comment8
        self.comment9 = comment9

    def __repr__(self):
        return '<Woman %r>' % self.username

@app.route("/callback", methods=['POST'])
def callback():


    msgs = request.json['result']

    # 0:初期問痔をだす
    # 1:成功した
    # status=0

    for msg in msgs:

        sender = msg['content']['from']
        content_id = msg['content']['id']
        content_type = msg['content']['contentType'] #1:text 2:image 3:video
    if content_type == 8:
              post_sticker(sender,"100","1","100")
    else:
        if not db.session.query(User).filter(User.user_code == sender).count():
            reg = User('user_'+str(sender), sender)
            db.session.add(reg)
            db.session.commit()
            print("ユーザー登録完了",str(sender))
        else:
            print("ユーザー登録済み")
            text = msg['content']['text']
            # user_status=User.user_status



        # メッセージ送信者のユーザーid
        user_id= db.session.query(User).filter(User.user_code == sender).first().id
        print("content_id")
        print(content_id)

        # ユーザーの状態
        this_user = db.session.query(User).filter(User.user_code == sender).first()
        status = this_user.user_status
        # user_status=this_user.user_status
        print("ユーザーの状態")
        print(status)

        if text == "text":
            image = msg['content']['text']
            print("image")
            print(image)
        elif re.compile('rich').match(text):
            # rich message
            print('rich')
            post_rich_message(sender)
        elif re.compile("翻訳|translate|訳し|訳す|ほんやく").match(text):

            pre_translate_text=text.replace("翻訳","")
            print("翻訳に反応")
            print(pre_translate_text)
            post_text(sender,get_translate(pre_translate_text))

        elif re.compile("location_").match(text):
            location_id=int(text.replace("location_",""))
            post_text(sender,"よく起きれたね！すごいね！")

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

            print("メイン")
            promlems = db.session.query(Problem2).all()
            for idx, problem_obj in enumerate(promlems):
                print(problem_obj.problem)

            if status ==0:
                post_text(sender,promlems[0].problem)
                post_yes_no_rich(sender)
                status=1
                this_user.user_status=status
                db.session.add(this_user)
                db.session.commit()
                print("0->1 ")
            elif status==1:
                # if :
                post_text(sender,"いいですね")


                post_text(sender,promlems[1].problem)
                post_yes_no_rich(sender)

                status = 2
                this_user.user_status=status
                db.session.add(this_user)
                db.session.commit()
                print("1->2")
                print(status)

            elif status==2:
                post_text(sender,"いいですね")

                post_text(sender,promlems[2].problem)
                post_yes_no_rich(sender)

                status =3
                this_user.user_status=status
                db.session.add(this_user)
                db.session.commit()
                print("2->3")
                print(status)

            elif status==3:
                post_text(sender,"いいですね．美女をご紹介します．")
                post_text(sender,"好きな場所をタップしてください")
                woman_all = db.session.query(Woman).all()
                woman_obj = woman_all[0]
                for idx, problem_obj in enumerate(promlems):
                    print(problem_obj.problem)

                # post_9col_rich_message(sender, woman_obj.MARKUP_JSON9)
                post_woman_rich_message(sender, woman_obj)

                status =0
                this_user.user_status=status
                db.session.add(this_user)
                db.session.commit()
            # elif status==4:
                # TODO:ここでタップされた場所を表す投稿内容をうけとってそれに応じたメッセージ表示
                # post_text(sender,"よく起きれたね！すごいね！")
                #
                # status =0
                # this_user.user_status=status
                # db.session.add(this_user)
                # db.session.commit()


        print(msgs)
        print(sender)





    return ''

if __name__ == '__main__':

    app.run(host = '0.0.0.0', port = 443, threaded = True, debug = True)
    # global status
    # status = 0
