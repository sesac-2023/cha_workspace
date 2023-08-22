
# 무신사 URL
# 검색 조건 (goods: 일반, photo: 사진, style: 스타일, beauty: 뷰티)
# 체험단은 제외 (리뷰 1건)
search_type = ['goods', 'photo', 'style', 'beauty']
BASE_URL = 'https://www.musinsa.com/goods/reviews/lists?type={}&searchYear=2023&maxRt=2023&minRt=2009&page={}&sort=new&s_type=all'
# page 양식 2

import scrapy

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

# style의 width값을 가져오는데 그것을 1~5점 척도로 변환
width_to_score = {
    '100%': '5',
    '80%': '4',
    '60%': '3',
    '40%': '2',
    '20%': '1',
}

class MusinsaReviewSpider(scrapy.Spider):
    name = "musinsa"

    def start_requests(self):
        # 검색 조건별로
        for t in search_type:
            # 페이지 1~10페이지 (추후 +10하여 1 -> 11 -> 21 식으로 크롤링)
            for p in range(1, 11):
                url = BASE_URL.format(t, p)
                yield scrapy.Request(url=url, headers=headers, callback=self.parse, cb_kwargs={
                    'page':p,
                    'search_type':t
                })

    def parse(self, response, page, search_type):
        url = response.url.replace(f'page={page}', f'page={page+10}')
        # print(url)

        # review-list 클래스를 가지는 div박스를 하나하나씩 반복문으로 돌릴 예정
        review_list = response.css('.review-list')
        ratings = []
        reviews = []
        for review in review_list:
            # review 텍스트는 여러건이 나올 수 있기 때문에 줄바꿈기호로 join (scrapy 특성)
            reviews.append('\n'.join(review.css('.review-contents__text::text').getall()))
            # style 속성에서 width의 값 부분만 잘라서 5점척도로 변경 
            ratings.append(width_to_score[review.css('.review-list__rating__active::attr(style)').get().split()[-1]])

        # 파일에 입력 (리뷰, 평점, 페이지, 검색조건이 spliter라는 단어를 기준으로 join)
        # 나중에 spliter로 분리하여 사용
        with open('./musinsa_review', 'a', encoding='utf-8') as f:
            f.write('\n'.join(['spliter'.join(list(d)+[str(page), search_type]) for d in zip([review.replace('\n', '\t') for review in reviews], ratings)]) + '\n')

        # if page+10 > 200:
        #     return
        # 만약 리뷰 개수가 20개가 되지 않으면 -> 마지막 페이지 도달했거나 데이터가 없는 페이지면 종료
        if len(reviews) < 20:
            return
        
        # 현재 크롤링된 페이지에 10을 더한 페이지 크롤링
        # 페이지에 10 더해주는 이유는 start_requests에서 1~10 페이지까지 크롤링을 하도록함 
        # 각각 뒷자리가 0~9로 끝나기 때문에 여기에 10씩 더해서 서로 겹치지 않게한 것임. 
        # 그냥 page+1 해서 한페이지씩 추가해도 무방
        yield scrapy.Request(url=url, headers=headers, callback=self.parse, cb_kwargs={
            'page': page+10,
            'search_type': search_type
        })

