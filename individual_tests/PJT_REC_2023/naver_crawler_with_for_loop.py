import scrapy
from datetime import date, datetime, timedelta
from user_agent import generate_user_agent
from urllib.parse import urljoin
import re
import requests
import json
from dateutil.relativedelta import relativedelta

'''
날짜 변경 _ 각자 본인이 맡은 연도로 수정
start_date = date(2015, 1, 1)
end_date = date.today()

scrapy 설치된 가상 환경 불러오기
crawler 있는 폴더로 이동 (ex. /naver_finance/naver_finance/spiders)
날짜 설정 후 scrapy 실행 코드: scrapy crawl {spider_name} -o {file_name} -t csv (ex. scrapy crawl finance -o test.csv -t csv)
'''

headers = {'User-Agent': generate_user_agent(os='win', device_type='desktop')}

class FinanceSpider(scrapy.Spider):

    name = "finance"
    allowed_domains = ["news.naver.com"]

    site = '네이버'
    category = '경제'
    sub_categories = {
        '259' : '금융',
        '258' : '증권',
        '261' : '산업/재계',
        '771' : '중기/벤처',
        '260' : '부동산',
        '262' : '글로벌 경제',
        '310' : '생활경제',
        '263' : '경제 일반'
    }

    def __init__(self, *args, **kwargs):
        super(FinanceSpider, self).__init__(*args, **kwargs)
        self.base_url = 'https://news.naver.com/main/list.naver?mode=LS2D&sid2={}&sid1=101&mid=shm&date={}&page={}'
        self.start_date = date(2023, 9, 13)
        self.end_date = self.start_date-relativedelta(days=1)
        self.current_page = 1
        self.previous_page_content = ""

    def start_requests(self):
        #크롤링 시작 url 생성
        date_str = self.start_date.strftime('%Y%m%d')
        for sub_category in self.sub_categories.keys():
            url = self.base_url.format(sub_category, date_str, self.current_page)
            yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={'sub_category' : sub_category})

    def parse(self, response):
        sub_category = response.meta['sub_category']
        current_page_content = response.css('.list_body.newsflash_body ul > li > dl > dt > a::text').getall()
        # 현재 페이지의 내용과 이전 페이지의 내용이 같으면, 해당 일자 크롤링 종료
        if current_page_content == self.previous_page_content:
            self.start_date -= timedelta(days=1)
            # 다음 날짜가 종료 날짜 이전일 경우 다시 parse 함수 실행
            if self.start_date >= self.end_date:
                self.current_page = 1
                date_str = self.start_date.strftime('%Y%m%d')
                url = self.base_url.format(date_str, self.current_page)
                yield scrapy.Request(url=url, callback=self.parse, headers=headers, meta={'sub_category' : sub_category})
            return
        # 현재 페이지의 내용과 이전 페이지의 내용이 다르면, 이전 페이지 내용을 현재 페이지로 업데이트
        else:
            self.previous_page_content = current_page_content

        # 기사 목록이 있을 경우 기사 url 크롤링 진행
        detail_urls = response.css('.list_body.newsflash_body ul > li > dl > dt > a::attr(href)').getall()
        for detail_url in detail_urls:
            yield scrapy.Request(url=detail_url, callback=self.parse_detail, headers=headers, meta={'sub_category' : sub_category})

        # 다음 페이지로 넘어감
        self.current_page += 1
        date_str = self.start_date.strftime('%Y%m%d')
        next_url = self.base_url.format(date_str, self.current_page)
        yield scrapy.Request(url=next_url, callback=self.parse, headers=headers, meta={'sub_category' : sub_category})

    #상세 뉴스 페이지 내용 크롤링(제목, 날짜, 본문, 신문사)
    def parse_detail(self, response):
        sub_category = response.meta['sub_category']
        url = response.url
        title = response.xpath('//*[@id="title_area"]/span/text()').get()
        report_date = response.xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div[1]/span/text()').get()
        edit_date = response.xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div[2]/span/text()').get()
        press = response.xpath('//*[@id="ct"]/div[1]/div[1]/a/img[1]/@alt').get()
        content = ' '.join([sent.strip() for sent in response.xpath('//*[@id="dic_area"]/text()').getall()])

        # 스티커(기사 반응) 크롤링
        sticker_url_param = re.split("[/?]", url)[5] + '_' + re.split("[/?]", url)[6]
        sticker_url = f'https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery331024024432313876654_1694675541323&q=JOURNALIST%5B73563(period)%5D%7CNEWS%5Bne_{sticker_url_param}%5D&isDuplication=false&cssIds=MULTI_MOBILE%2CNEWS_MOBILE&_=1694675541324'
        resp = requests.get(sticker_url, headers=headers)
        text = resp.text
        text = text[text.index('(')+1:] #jQuery17010485993748665368_1526170138101(
        text = text.replace(');','')
        text = text.encode('cp949', 'ignore').decode('cp949')

        reaction = {'wow': 0, 'useful': 0, 'touched':0, 'analytical':0, 'cheer': 0 }
        source = json.loads(text)['contents'][1]['reactions']
        for i in source:
            if i['reactionType'] in reaction.keys():
                reaction[i['reactionType']] = i['count']
    
        # 네이버 뉴스 댓글 크롤링
        temp=url.split('?')[0]
        oid_1 = temp.split('/')[-1]
        oid_2 = temp.split('/')[-2]
        page=1
        params={'ticket': 'news',
                'templateId': 'default_society',
                'pool': 'cbox5',
                'lang': 'ko',
                'country': 'KR',
                'objectId': f'news{oid_2},{oid_1}',
                'pageSize': '100',
                'indexSize': '10',
                'page': str(page),
                'currentPage': '0',
                'moreParam.direction': 'next',
                'moreParam.prev': '10000o90000op06guicil48ars',
                'moreParam.next': '1000050000305guog893h1re',
                'followSize': '100',
                'includeAllStatus': 'true',}
        custom_header = {
            'referer' : url,
            'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
        response=requests.get('https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json', params=params, headers=custom_header)
        response.encoding = "UTF-8-sig"
        res = response.text.replace("_callback(","")[:-2]
        temp=json.loads(res)
        
        comments = []
        for comment_data in temp['result']['commentList']:
            temp = {}
            for key, value in comment_data.items():
                if key in ["commentNo", "userIdNo", 'userName', "contents", "sympathyCount", "antipathyCount", "regTime"]:
                    temp[key] = value
            comments.append(temp)


        yield {
            'site' : '네이버', 
            'category' : '경제',
            'sub' : self.sub_categories[sub_category],
            'url': url,
            'date': report_date,
            'edit_date': edit_date,
            'title': title,
            'press': press,
            'content': content,
            'reaction': reaction,
            'comment' : comments
        }