import schedule
import time
import linebot
import requests
import json
import re
from datetime import datetime
from linebot import User
from flask_sqlalchemy import SQLAlchemy
import os



# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

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


def post_text( to, text ):
    content = {
        'contentType':1,
        'toType':1,
        'text':text,
    }
    post_event(to, content)

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
            'DOWNLOAD_URL': 'https://translate-application.herokuapp.com/static/',
            'SPEC_REV': '1',
            'ALT_TEXT': 'Please visit our homepage and the item page you wish.',
            'MARKUP_JSON':json.dumps(MARKUP_JSON)

            }# end copy
        }
    post_event(to,content)


def job():

    print("I'm working...")

    # hello()
    users=User.query.all()
    now = datetime.now()
    now_string=str(now.hour+9)+"時"+str(now.minute)+"分"
    for user in users:

        user_id=user.user_code
        print(user_id)
        post_text(user_id,now_string+"です．東工大志望のおきなくんは数学を勉強しているよ！")
        post_rich_message(user_id)




schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(10)
