import scrapy
import pandas as pd
from user_agent import generate_user_agent
from scrapy.spiders import CrawlSpider

headers = {'User-Agent': generate_user_agent(os='win', device_type='desktop')}


class MySpider(scrapy.Spider):
    name = 'naver_writer'
    download_delay = 0.1

    df = pd.read_csv('./naver_economy_final.csv', usecols=['url'])
    urls = df['url'].tolist()

    def start_requests(self):
        for url in self.urls[550000:]:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response):
        writer = response.xpath('//*[@id="ct"]/div[1]/div[3]/div[2]/a/em/text()').get()

        yield {
            'url': response.url,
            'writer': writer}
