from pathlib import Path

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes" # spider name
    quote_count = 1
    allowed_domains = ["quotes.toscrape.com"]

    # gidilecek sayfalar
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        # "https://quotes.toscrape.com/page/2/", (link takip etmek için bunu yoruma alıp quote__count ile sayfa sayısını bulabiliriz)
    ]


    # 2. yol
    """def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    """
    # parse fonksiyonu
    def parse(self, response):
        quotes = response.css("div.quote")
        with open("quotes.txt", "a", encoding="utf-8") as file:
            # her quote için
            for quote in quotes:
                text = quote.css("span.text::text").get()
                author = quote.css("small.author::text").get()
                tags = quote.css("div.tags a.tag::text").getall()
                
                # file.write(f"Text: {text}\n")
                file.write(f"Text: {text}\n")
                file.write(f"Author: {author}\n")
                file.write(f"Tags: {str(tags)}\n")
                file.write("************************************************************\n")
        
        # Sonraki sayfaya git
        next_page = response.css('li.next a::attr(href)').get() 
        if next_page:
            yield response.follow(next_page, self.parse) # next page'i takip et



# run the spider()