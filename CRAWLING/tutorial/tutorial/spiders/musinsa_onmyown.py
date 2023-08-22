# 무신사 리뷰 URL

import scrapy

class MusinsaReviews(scrapy.Spider):
    BASE_URL = ['https://www.musinsa.com/goods/reviews/lists?type=style&searchYear=2023&maxRt=2023&minRt=2009&searchKeyword=&hashId=&page=1']
    name = "musinsa_review"

    def parse(self, response):
        # brand = response.xpath("//div[@class='review-goods-information__item']/a/text()").extract()
        # item = response.xpath("//div[@class='review-goods-information__item']/a[2]/text()").extract()
        review = response.css('.review-contents__text::text').extract()

        for item in zip(review):
            scraped_info = {
                # 'brand' : item[0].strip(),
                # 'item' : item[1].strip(),
                'review' : item[1].strip()
            }
            yield scraped_info