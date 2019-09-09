import scrapy

class BrickSetSpider(scrapy.Spider):
    name = "news_scraper"
    start_urls = ['https://brasil.elpais.com/tag/politica/']

    def parse(self, response):
        for url in response.css('.articulo-titulo a ::attr("href")').extract():
            yield response.follow(url, callback=self.parse_article)
        older_posts = response.css('.paginacion-siguiente a ::attr("href")').extract_first()
        if older_posts is not None:
            yield response.follow(older_posts, callback=self.parse)


    def parse_article(self, response):
        for brickset in response.css('.articulo'):
            yield {
                'title': brickset.css('.articulo-titulo ::text').get(),
                'date': brickset.css('.articulo-datos time a ::text').get(),
                'text': brickset.css('#cuerpo_noticia > p ::text').getall()
            }