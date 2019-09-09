import scrapy
import json

# Scraping infinit scrolling pages:
# https://blog.scrapinghub.com/2016/06/22/scrapy-tips-from-the-pros-june-2016

class BrickSetSpider(scrapy.Spider):
    name = "news_scraper"
    base_url = 'https://falkor-cda.bastian.globo.com/tenants/g1/instances/1b9deafa-9519-48a2-af13-5db036018bad/posts/page/%s'
    start_urls = [base_url % 1]

    def parse(self, response):
        data = json.loads(response.body)
        for item in data.get('items', []):
            if item.get('content', {}).get('section') == 'Política':
                yield response.follow(item.get('content', {}).get('url'), callback=self.parse_article)
        if int(data.get('nextPage')) != 2000:
            yield scrapy.Request(self.base_url % (int(data.get('nextPage')) + 1))
         

    def parse_article(self, response):
        for brickset in response.css('main'):
            yield {
                'title': brickset.css('.content-head__title ::text').get(),
                'date': brickset.css('time[itemprop="datePublished"] ::text').get(),
                'text': brickset.css('.content-text__container ::text').getall()
            }