import sys
import io
import requests
import schedule
import time
import telegram

goods_list = []
text_pr = ''

def job():
    global goods_list, text_pr

    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')

    token = 'token'
    bot = telegram.Bot(token = token)
    BASE_URL = ['URL']
    chat_id = "chat"
    
    with requests.Session() as s:
        for i in BASE_URL:
            index_ = 0
            res = s.get(i)
            if res.status_code == requests.codes.ok:
                goods = res.text
                
                while index_ < len(goods):
                    index_ = goods.find('"goodsName"', index_)
                    index2 = goods.find('"goodsCode"', index_)
                    if index_ == -1:
                        break
                    goods_list.append(goods[index_+12 : index2-1])
                    goods_list.append(goods[index2+19 : index2+24])
                    index_ += 11
                text_ = '\n\n'.join(goods_list)
        
        if text_ != text_pr:
            bot.sendMessage(chat_id=chat_id, text=text_)
        text_pr = (text_ + '.')[:-1]
        goods_list = []
        print('1분에 한번씩 정상 실행중')
        
            #if article == None or cartExist or wishBtn:
            #    bot.sendMessage(chat_id=chat_id, text="구매 가능")
            #else:
            #    if count % 6 == 0:
            #        bot.sendMessage(chat_id=chat_id, text="품절 상태")
            #    else:
            #        print("60분에 1번만 알림 가도록 설정")

# x분 마다 실행
schedule.every(1).minutes.do(job)

print("Start App")

# 파이선 스케줄러
while True:
    schedule.run_pending()
    time.sleep(1)