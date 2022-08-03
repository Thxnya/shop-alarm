import sys
import io
from bs4 import BeautifulSoup
import requests
import schedule
import time
import telegram

count = 1

def job():
    global count
    count += 1

    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')

    token = 'token'
    bot = telegram.Bot(token = token)
    BASE_URL = "URL"
    chat_id = "chat"

    with requests.Session() as s:
        res = s.get(BASE_URL)
        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, 'html.parser')
            stock_a = soup.find("div", class_="type reservation soldOut")

            if stock_a == None:
                return bot.sendMessage(chat_id=chat_id, text="구매 가능")
            else:
                if count % 120 == 0:
                    return bot.sendMessage(chat_id=chat_id, text="품절 상태")
                else:
                    print("60분에 1번만 알림 가도록 설정")
            
            #if article == None or cartExist or wishBtn:
            #    bot.sendMessage(chat_id=chat_id, text="구매 가능")
            #else:
            #    if count % 6 == 0:
            #        bot.sendMessage(chat_id=chat_id, text="품절 상태")
            #    else:
            #        print("60분에 1번만 알림 가도록 설정")

# 30초 마다 실행
schedule.every(30).seconds.do(job)

print("Start App")

# 파이선 스케줄러
while True:
    schedule.run_pending()
    time.sleep(1)