# https://python-telegram-bot.org/

with open('./secret', 'r') as f:
    secret = {l.split('=')[0]: l.split('=')[1].strip() for l in f.readlines()}

token = secret['TELEGRAM_TOKEN']
chat_id = secret['CHAT_ID']


## hello에 응답하기
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.last_name}')

async def myname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'My name is {update.effective_user.first_name}')
    await update.message.reply_photo(open('.\IMG_9079.JPG', 'rb')) 


## trip에 응답하기
fake_db = {
    '국내' : ['동해', '남해'],
    '해외' : ['아이슬란드', '덴마크']
}


async def trip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    print(update.message.chat_id)
    target = update.message.text.split()[-1]
    locations = []
    if target in fake_db:
        locations = fake_db[target]
        await update.message.reply_text(f'추천 여행지{str(locations)}')
    else:
        await update.message.reply_text(f'어떤 여행지를 추천해드릴까요? (국내, 해외)')


## 자동 메세지 발신 
import requests

message = "What's your ETA?"

def send_to_telegram(message):

    url = f'https://api.telegram.org/bot{token}/sendMessage'

    try:
        res = requests.post(url, 
                            json={'chat_id': chat_id, 'text':message})
        print(res.text)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    send_to_telegram(message=message)



app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("myname", myname))
app.add_handler(CommandHandler("trip", trip))

if __name__ == '__main__':
    # print(token)
    app.run_polling()



#======================= 위 : 수업 내용 / 아래 : 혼자 실습!

#===============================================================================
#          연습 - 네이버 뉴스(연합뉴스) 크롤링하고 "요청 시" 메세지 발신
#=============================================================================== 

import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {'User-Agent' :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
today = datetime.now().strftime('%Y%m%d')


async def naver_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=001&date={}&page={}'  #연합뉴스 : 001, 한국경제 : 015 등등 -> 추후 언론사별로 크롤링할 수 있을 듯 (뉴스-연합 맨시티)
    
    result = []
    for page_number in range(1, 6):  # 5페이지까지 크롤링
        response = requests.get(url.format(today, page_number), headers=headers) # 오늘 날짜로 크롤링
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.select('ul[class^="type06"] li')

        for news in news_items:
            title = news.select('dt')[-1].text.strip()
            item_url = news.select_one('a')['href']
            content = news.select_one('.lede').text.strip()

            result.append({
                '제목': title,
                '요약': content,
                '링크': item_url
            })    
    
    '''
    * 입력값 -> 세 가지 경우의 수로 나눠서 생각하기
    1. '뉴스'
    2. '뉴스 {숫자}'
    3. '뉴스 {문자}'
    '''
  
    input = update.message.text.split()
    target = input[-1]

    # '뉴스' 만 입력 시, 최근 기사 5개 발신
    if len(input) == 1: # and input[0] == 'news' 불필요함 
        content = [f"[{item['제목']}]\n{item['요약']}\n{item['링크']}" for item in result[:5]]
        message_to_send = "\n\n".join(content) # 5개의 뉴스를 메세지 한 개에 통합해서 보내기

    else: 
        try:                   
            if 1 <= int(target) <= len(result): # '뉴스 {숫자}' 입력 시, 최근 첫 번째 기사부터 입력값까지의 기사를 누적해서 보여주기
                content = [f"[{item['제목']}]\n{item['요약']}\n{item['링크']}" for item in result[:int(target)]] #'뉴스 0'이라고 입력 시, 출력되는 결과값 없음.
                message_to_send = "\n\n".join(content)
            else:
                message_to_send = '더 작은 숫자를 입력하세요'  # 크롤링한 뉴스 개수보다 큰 숫자를 입력한 경우
            
        except ValueError: # '뉴스 {문자}' 입력 시, 해당 키워드가 제목이나 요약에 포함될 경우
            content = [f"[{item['제목']}]\n{item['요약']}\n{item['링크']}" for item in result if target in item['제목'] or target in item['요약']]

            if content:
                max_items_to_send = 10
                num_items_to_send = min(max_items_to_send, len(content)) # 기사 수를 최대 10개로 제한하고 10개 보다 적을 경우, 존재하는 만큼만 발신하기 

                message_to_send = "\n\n".join(content[:num_items_to_send])
            else:
                message_to_send = "No matches found." # 해당 키워드에 부합하는 기사가 존재하지 않을 경우, 안내문 표시
    
    await update.message.reply_text(message_to_send, disable_web_page_preview=True)



#====================================================================
#                  네이버 야구 자동화 프로젝트
#==================================================================== 
"""----------------------------------------------------------------------------
     1. 네이버 야구 - 롯데 뉴스 크롤링하고 "요청 시" 메세지 발신 
----------------------------------------------------------------------------"""

import json

async def lotte_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = 'https://sports.naver.com/kbaseball/news/list?date={}&isphoto=N&type=team&isPhoto=N&team=LT' # -> 두산 : OB, 한화 : HH 등 추후 구단별로 크롤링 가능 


    response = requests.get(url.format('20230730'))  # 오늘 날짜로 크롤링하기 -> 월요일은 야구 안함. 일요일 날짜로 테스트
    data = json.loads(response.text)  # response.text (str) -> json으로 파싱 (dict으로 구성된 list)
    # print(type(response.text))
    # print(type(data))

    # for key, item in data.items():
    #     print(key,item)
    #     break        

    result = []
    for item in data['list']:
        title = item['title']
        item_url = f"https://sports.naver.com/news?oid={item['oid']}&aid={item['aid']}" # 파라미터 엮어서 링크 만들기

        result.append({
            '제목' : title,
            '링크' : item_url
        })

    '''
    * 입력값 -> 세 가지 경우의 수로 나눠서 생각하기
    1. '롯데'
    2. '롯데 {숫자}'
    3. '롯데 {문자}'
    '''

    input = update.message.text.split()
    target = input[-1]

    # '롯데' 만 입력 시, 최근 기사 5개 발신
    if len(input) == 1: 
        content = [f"{item['제목']}\n{item['링크']}" for item in result[:5]]
        message_to_send = "\n\n".join(content) # 5개의 뉴스를 메세지 한 개에 통합해서 보내기
 
    else:
        try:  
            if 1 <= int(target) <= len(result): # '롯데 {숫자} 입력 시, 최근 첫 번째 기사부터 입력값까지의 기사를 누적해서 보여주기
                content = [f"{item['제목']}\n{item['링크']}" for item in result[:int(target)]]
                message_to_send = "\n\n".join(content)
            else:
                message_to_send = "더 작은 숫자를 입력하세요" # 크롤링한 뉴스 개수보다 큰 숫자를 입력한 경우
        
        except ValueError: # '/롯데 {문자} 입력 시, 해당 키워드가 제목이나 요약에 포함될 경우
            content = [f"{item['제목']}\n{item['링크']}" for item in result if target in item['제목']]

            max_items_to_send = 10
            num_items_to_send = min(max_items_to_send, len(content)) # 기사 수를 최대 10개로 제한하고 10개 보다 적을 경우, 존재하는 만큼만 발신하기

            if content:
                message_to_send = "\n\n".join(content[:num_items_to_send])
            else:
                message_to_send = "No matches found." # 해당 키워드에 부합하는 기사가 없을 경우, 안내문 표시
    
    await update.message.reply_text(message_to_send, disable_web_page_preview=True)


app.add_handler(CommandHandler("news", naver_news))
app.add_handler(CommandHandler("lotte", lotte_news))

if __name__ == '__main__':
    # print(token)
    app.run_polling()