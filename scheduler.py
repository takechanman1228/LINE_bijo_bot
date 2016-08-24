import schedule
import time
import linebot

def job():
    print("I'm working...")
    hello()
    post_text('u206d25c2ea6bd87c17655609a1c37cb8',"時報だよ")

schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(10)
