
# 경제 - 부동산 뉴스기사 URL
BASE_URL = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=260&sid1=101&date={}&page={}'
# date 양식 20230805
# page 양식 2

import scrapy

from datetime import datetime, timedelta
class NaverNewsSpider(scrapy.Spider):
    name = "naver_news"

    def start_requests(self):
        urls = []
        # 날짜 관리 (10일치만 크롤링)
        date_today = datetime.now()
        for day in range(10):
            target_day = date_today - timedelta(days=day)
            # # 2 페이지만 크롤링 (날짜별로)
            # for page in range(1, 3): # 1, 2
            url = BASE_URL.format(target_day.strftime('%Y%m%d'), 1)
            urls.append(url)
            yield scrapy.Request(url=url, callback=self.news_list, cb_kwargs={
                'target_day': target_day,
                'page': 1
            })

        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse, )

    def news_list(self, response, target_day, page):
        # BeautifulSoup(response.html, 'html.parser')
        
        description = response.css('.lede::text').get()
        print(target_day.strftime('%Y-%m-%d'), page, end='\t')
        print(description)

        # if 페이지 끝에 도달했으면:
        #     return 
        if page == 10:
            return
        detail_urls = response.css('dd > a::attr(href)').get()
        
        for detail_url in detail_urls:
            yield scrapy.Request(url=detail_url, callback=self.news_detail)

        yield scrapy.Request(url=BASE_URL.format(target_day.strftime('%Y%m%d'), page+1), 
                             callback=self.news_list, cb_kwargs={
                                'target_day': target_day,
                                'page': page+1
                            })
        
    def news_detail(self, response):
        temp = response.css('a::text').get()
        print(temp)

