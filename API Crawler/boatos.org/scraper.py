import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "news_scraper"
    start_urls = ['https://www.boatos.org/category/politica']

    def parse(self, response):
        for url in response.css('.entry-title a::attr("href")').extract():
            yield response.follow(url, callback=self.parse_article)
        older_posts = response.css('.previous a ::attr("href")').extract_first()
        if older_posts is not None:
            yield response.follow(older_posts, callback=self.parse)


    def parse_article(self, response):
        for brickset in response.css('#content'):
            yield {
                'title': brickset.css('h1 ::text').get(),
                'date': brickset.css('.entry-date ::text').get(),
                'text': brickset.css('.entry-content > p span[style="color: #ff0000;"] ::text').getall() + brickset.css('.entry-content > blockquote ::text').getall() 
            }