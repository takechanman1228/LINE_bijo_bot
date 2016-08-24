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


def job():

    print("I'm working...")

    # hello()
    users=User.query.all()
    for user in users:

        user_id=user.user_code
        print(user_id)
        post_text(user_id,"時間です．姿勢にきをつけましょう")



schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(10)
