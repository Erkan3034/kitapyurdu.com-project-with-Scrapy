import scrapy

class KitapYurduSpider(scrapy.Spider):
    name = 'kitap_yurdu'
    allowed_domains = ['kitapyurdu.com']
    start_urls = ['https://www.kitapyurdu.com/']

    def parse(self, response):
        pass

    def parse_book(self, response):
        pass

    def parse_author(self, response):
        pass
        

        