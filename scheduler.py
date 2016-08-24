import schedule
import time
import linebot

def job():
    print("I'm working...")
    print(LINE_HEADERS)

schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(10)
